import json

from ..utils.exceptions import NoTextProvided
from ..utils.prompts import NLQ_SYSTEM_PROMPT, RELATED_QUESTION_SYSTEM_PROMPT
from ..utils.sql_utils import extract_output
from ..models.llms import Llm
from ..vector.chroma_db import ChromaStore


class Raxo:
    def __init__(self, llm: Llm, database=None, vector_db=None, em_function=None, execute_query: bool = False):
        self.llm = llm
        self.database = database
        self.vector_db = vector_db or ChromaStore()
        self.execute_query = execute_query
        self.em_function = em_function
        self.dialect = self.database.dialect if self.database else "MySQL"

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
        prompt = self._get_prompt(user_query, ddl, self.dialect)

        response = self.llm.invoke_prompt(prompt)
        response = extract_output(response)
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
        sql, error = None, None
        if not query:
            raise NoTextProvided("Please provide a valid input!")
        response = self.generate_sql(query)
        if isinstance(response, dict):
            sql = response["sql"]
            error = response['error']
        if self.execute_query and sql:
            result = self.database.execute_query(sql)
        elif sql and not error:
            result = sql
        elif not sql and error:
            result = error
        else:
            result = f"something went wrong, Here is the LLM response -> {response}"
        return result

    def get_follow_up_questions(self, sql_query, count=3):
        if not sql_query:
            raise NoTextProvided("Please provide a valid input!")
        questions = self.generate_related_question(sql_query, count)

        return questions

    def train(self, question: str = None, sql: str = None, ddl: str = None, documentation: str = None):
        if ddl:
            embedding = self.em_function.create_embedding(ddl)
            return self.vector_db.add_ddl(ddl, embedding)
