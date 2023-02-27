import os


class Processor:
    def __init__(self, documents_dir: str) -> None:
        self.documents = [os.path.join(documents_dir, file) for file in os.listdir(
            documents_dir) if os.path.isfile(os.path.join(documents_dir, file))]

    def make_query(self, query: str) -> dict:
        pass
