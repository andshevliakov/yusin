from processor.processor import Processor
from processor.vector_model import VectorSpaceModel
from processor.boolean_model import BooleanModel


def boolean_model():
    terms_file = input("Input terms file location: ")
    documents_dir = input("Input documents directory location: ")
    try:
        boolean_mod = BooleanModel(terms_file=terms_file,
                              documents_dir=documents_dir)
    except FileNotFoundError:
        print("Docs or files not found.")
        return
    except Exception as error:
        print("While processing docs and files, error occurred:", error)
        return

    while True:
        dnf_string = input("Input query in dnf format(q for exit): ")
        if dnf_string.lower() == "quit":
            break
        elif dnf_string.lower() == "q":
            break
        else:
            response = boolean_mod.make_query(dnf_string)
            if not response:
                print("Empty result")
            iterator = 1
            for key, val in response.items():
                print(f"\n{iterator}. {key}\n{val}")
                iterator += 1


def vector_model():
    documents_dir = input("Input documents directory location: ")
    try:
        vector_mod = VectorSpaceModel(documents_dir=documents_dir)
    except FileNotFoundError:
        print("Docs not found.")
        return
    except Exception as error:
        print("While processing docs, error occurred:", error)
        return

    while True:
        query_string = input("Input query (q for exit): ")
        if query_string.lower() == "quit":
            break
        elif query_string.lower() == "q":
            break
        else:
            response = vector_mod.make_query(query_string)
            if not response:
                print("Empty result")
            iterator = 1
            for key, val in response.items():
                print(f"\n{iterator}. {key}\n{val}")
                iterator += 1
