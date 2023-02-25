from processor.processor import Processor

def menu():
    terms_file = input("Input terms file location: ")
    documents_dir = input("Input documents directory location: ")
    try:
        processor = Processor(terms_file=terms_file,
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
            response = processor.make_query(dnf_string)
            if not response:
                print("Empty result")
            iterator = 1
            for key, val in response.items():
                print(f"\n{iterator}. {key}\n{val}")
                iterator += 1
