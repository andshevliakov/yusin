import os
import numpy as np
from processor.processor import Processor
from utils.utils import read_docs_with_val, remove_string_punctuation, most_common_word_count_in_str, read_doc_string_formated

K = 0.01

class VectorSpaceModel(Processor):

    def __init__(self, documents_dir: str) -> None:
        super().__init__(documents_dir=documents_dir)

        self.terms = self.__create_terms()
        self.document_vectors = self.__create_doc_vectors()

    def make_query(self, query: str) -> dict:
        query = remove_string_punctuation(query).lower()
        query_vector = self.__create_vector(query)
        casine_sim = {}
        for doc_name in self.documents:
            euclidean_norm = np.linalg.norm(
                query_vector)*np.linalg.norm(self.document_vectors[doc_name])
            if euclidean_norm == 0:
                casine_sim[doc_name] = 0
                continue
            casine_sim[doc_name] = np.dot(
                query_vector, self.document_vectors[doc_name]) / euclidean_norm
        ranked_docs = self.__rank_documents(casine_sim)
        return read_docs_with_val(ranked_docs)

    def __rank_documents(self, casine_sim: dict) -> dict:
        return dict(sorted([(k, v) for k, v in casine_sim.items() if v > 0.2], key=lambda item: item[1], reverse=True))

    def __create_vector(self, target_str: str) -> np.ndarray:
        common_count_word = most_common_word_count_in_str(target_str)
        return np.array([self.__tf(target_str.split().count(
            word), common_count_word)*self.__idf(word) for word in self.terms])

    def __create_doc_vectors(self) -> dict:
        result = {}
        for doc_name in self.documents:
            doc_str = read_doc_string_formated(doc_name=doc_name)
            result[doc_name] = self.__create_vector(doc_str)
        return result

    def __create_terms(self) -> list[str]:
        result = list()
        for doc in self.documents:
            doc_str = read_doc_string_formated(doc_name=doc)
            result.extend(doc_str.split())
        return list(set(result))

    def __tf(self, term_count: int, max_term_count: int) -> float:
        return K+(1-K)*(term_count / max_term_count)

    def __idf(self, term: str) -> float:
        N = len(self.documents)
        doc_counter = 0
        for doc in self.documents:
            line = read_doc_string_formated(doc)
            if term in line:
                doc_counter += 1
        return np.log(N / (1+doc_counter)) + 1
