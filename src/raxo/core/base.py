

class Raxo(object):
    def __init__(self, llm, database, vector_db=None):
        self.llm = llm
        self.database = database
        self.vector_db = vector_db

    def ask(self, query):
        if query:
            self.llm.invoke(query)
