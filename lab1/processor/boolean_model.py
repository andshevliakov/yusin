import os
import string
from processor.processor import Processor
from utils.utils import read_docs


class BooleanModel(Processor):

    def __init__(self, terms_file: str, documents_dir: str) -> None:
        super().__init__(documents_dir=documents_dir)
        self.clauses = []
        self.terms = []

        with open(terms_file, 'r', encoding="UTF-8") as file:
            lines = file.readlines()
            for line in lines:
                self.terms.extend(self.__manipulate_terms_sting(line))

        self.__create_table()

    def make_query(self, query: str) -> dict:

        self.__read_dnf(query)
        docs = self.__get_doc_colissions()
        return read_docs(docs)

    def __get_doc_colissions(self) -> set:
        query = set()
        for clause_str in self.clauses:
            clause = []
            is_negative = False
            result_set = set()
            clause = str(clause_str[0]).split(" AND ")

            if len(clause) > 1:
                for _, predicate in enumerate(clause):
                    is_negative = False
                    actual_pred = predicate.lower()
                    if predicate.find("NOT ") != -1:
                        is_negative = True
                        actual_pred = predicate.split("NOT ")[1].lower()
                    if not self.__check_term_existance(actual_pred):
                        continue
                    if len(result_set) == 0:
                        if is_negative:
                            result_set = set(self.documents).difference(
                                self.table[actual_pred])
                        else:
                            result_set = self.table[actual_pred]
                    else:
                        if is_negative:
                            result_set = result_set.difference(
                                self.table[actual_pred])
                        else:
                            result_set = result_set.intersection(
                                self.table[actual_pred])
            else:
                if clause[0].find("NOT") != -1:
                    is_negative = True
                    clause[0] = clause[0].split("NOT ")[1].lower()
                if not self.__check_term_existance(clause[0].lower()):
                    continue
                if is_negative:
                    result_set = set(self.documents).difference(
                        self.table[clause[0]])
                else:
                    result_set = self.table[clause[0].lower()]

            if len(query) == 0:
                query = result_set
            else:
                query = query.union(result_set)
        return query

    def __check_term_existance(self, term: str) -> bool:
        return True if term in self.table else False

    def __create_table(self) -> None:
        table = {}
        for term in self.terms:
            table[term] = set()
            for doc in self.documents:
                with open(doc, "r", encoding="UTF-8") as file:
                    for line in file:
                        if term in line.lower():
                            table[term].add(doc)
                            break
        self.table = table

    def __manipulate_terms_sting(self, terms_str: str) -> list[str]:

        terms_list = []
        terms_str = terms_str.lower()
        punct = string.punctuation
        translator = str.maketrans("", "", punct)
        terms_str = terms_str.translate(translator)
        terms_list = terms_str.split()
        terms_list = list(set(terms_list))
        return terms_list

    def __read_dnf(self, dnf_str: str) -> None:

        self.clauses = []
        clauses_str = dnf_str.split(" OR ")
        for clause_str in clauses_str:
            clause = []
            # extract literals from brackets
            literal_start_index = clause_str.find("(")
            while literal_start_index != -1:
                literal_end_index = clause_str.find(")", literal_start_index)
                clause.append(
                    clause_str[literal_start_index+1:literal_end_index])
                literal_start_index = clause_str.find("(", literal_end_index)
            # if no brackets in the clause, extract literals without brackets
            if not clause:
                clause.append(clause_str)
            self.clauses.append(clause)
