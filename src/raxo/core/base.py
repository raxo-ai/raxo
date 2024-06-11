from ..utils.exceptions import NoTextProvided
from src.raxo.utils.prompts import NLQ_SYSTEM_PROMPT, RELATED_QUESTION_SYSTEM_PROMPT
from ..models.llms import Llm
from ..vector.chroma_db import ChromaStore


class Raxo:
    def __init__(self, llm: Llm, database, vector_db=None, em_function=None, execute_query: bool = False):
        self.llm = llm
        self.database = database
        self.vector_db = vector_db or ChromaStore()
        self.execute_query = execute_query
        self.em_function = em_function

    @staticmethod
    def _get_prompt(user_query, tables, database_type):
        system_prompt = NLQ_SYSTEM_PROMPT.format(database=database_type, table=tables)
        prompt = [{"role": "system", "content": system_prompt},
                  {"role": "user", "content": f"{user_query}"}]
        return prompt

    def generate_sql(self, user_query):
        embedding = self.em_function.create_embedding(user_query)
        ddl = self.vector_db.get_ddl(embedding)

        # Extracting documents only
        ddl = ddl['documents'][0]

        prompt = self._get_prompt(user_query, ddl, self.database.dialect)

        response = self.llm.invoke_prompt(prompt)

        return response

    def generate_related_question(self, query, follow_up_count):
        prompt = RELATED_QUESTION_SYSTEM_PROMPT.format(n=follow_up_count)
        tables = ""
        prompt = [{"role": "system", "content": prompt},
                  {"role": "user", "content": f"""Previous_question - {query}
                                            Tables - {tables}"""}]
        response = self.llm.invoke_prompt(prompt)
        return response

    def ask(self, query):
        if not query:
            raise NoTextProvided("Please provide a valid input!")
        sql = self.generate_sql(query)
        if self.execute_query:
            result = self.database.execute_query(sql)
        else:
            result = sql
        return result

    def get_follow_up_questions(self, sql_query, count=3):
        if not sql_query:
            raise NoTextProvided("Please provide a valid input!")
        questions = self.generate_related_question(sql_query, count)

        return questions

    def train(self, question: str = None, sql: str = None, ddl: str = None, documentation: str = None):
        if ddl:
            embedding = self.em_function.create_embedding(ddl)
            print(embedding)
            return self.vector_db.add_ddl(ddl, embedding)
