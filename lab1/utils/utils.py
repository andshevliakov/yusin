import string
from collections import Counter


def remove_string_punctuation(target_str: str) -> str:
    punct = string.punctuation
    translator = target_str.maketrans("", "", punct)
    format_line = target_str.translate(translator)
    target_str = format_line.replace('\n', ' ')
    return target_str


def read_doc_string_formated(doc_name: str) -> str:
    result = ""
    try:
        with open(doc_name, "r", encoding="UTF-8") as file:
            lines = file.read()
            result = remove_string_punctuation(lines)
    except Exception as error:
        print("Unable to retrieve doc list", error)

    return result.lower()


def most_common_word_count_in_str(target_str: str) -> float:
    _, count = Counter(target_str.split()).most_common(1)[0]
    return count


def read_docs(docs: set) -> dict:
    result = {}
    for doc in docs:
        with open(doc, "r", encoding="UTF-8") as file:
            lines = file.read()
        result[doc] = lines
    return result

def read_docs_with_val(docs: dict) -> dict:
    result = {}
    for doc, value in docs.items():
        with open(doc, "r", encoding="UTF-8") as file:
            lines = file.read()
        result[doc+" "+str(value)] = lines
    return result
