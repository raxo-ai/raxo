import json
import re
from abc import ABC, abstractmethod
from ..utils.exceptions import NoTextProvided
from src.raxo.utils.prompts import NLQ_SYSTEM_PROMPT, RELATED_QUESTION_SYSTEM_PROMPT
from ..models.llms import Llm


class Raxo(ABC):
    def __init__(self, llm: Llm, database, vector_db=None, execute_query=None):
        self.llm = llm
        self.database = database
        self.vector_db = vector_db
        self.execute_query = execute_query

    @abstractmethod
    def get_prompt(self, user_query, tables, database_type):
        system_prompt = NLQ_SYSTEM_PROMPT.format(database=database_type, table=tables)
        prompt = [{"role": "system", "content": system_prompt},
                  {"role": "user", "content": f"[QUESTION] {user_query} [/QUESTION]"}]
        return prompt

    @abstractmethod
    def extract_sql(self, response):
        sql = None
        try:
            sql = json.loads(response)["sql"]
        except Exception as e:
            print(e)
            pattern = r'\{.*\}'
            match = re.search(pattern, s)
            if match:
                sql = match.group(0)
        return sql

    @abstractmethod
    def generate_sql(self, user_query):
        tables = ""
        prompt = self.get_prompt(user_query, tables, self.database.dialect)
        response = self.llm.invoke_prompt(prompt)
        sql = self.extract_sql(response)
        return sql

    @abstractmethod
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
            result = self.database.recieve_query(sql)
        else:
            result = sql
        return result

    def get_follow_up_questions(self, sql_query, count=3):
        if not sql_query:
            raise NoTextProvided("Please provide a valid input!")
        questions = self.generate_related_question(sql_query, count)

        return questions
