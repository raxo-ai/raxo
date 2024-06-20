 # Raxo
[![GitHub](https://img.shields.io/badge/GitHub-raxo-blue?logo=github)](https://github.com/raxo-ai/raxo)

# 🔍 Raxo: Transform Natural Language into SQL Queries with RAG

Raxo is an MIT-licensed open-source Python framework for text-to-SQL generation using Retrieval-Augmented Generation (RAG). It simplifies the process of generating SQL queries from natural language input, making it easier to interact with databases using plain English.

## Key Features:
- 🚀 Seamlessly convert natural language queries into SQL statements
- 🔧 Customize query generation to suit your specific database schema and query requirements
- 📊 Access and analyze user data efficiently with generated SQL queries
- 💻 Simple integration into existing Python projects and data pipelines
- 📚 Comprehensive documentation and examples for easy adoption and implementation

Get started with Raxo today and unlock the power of transforming text into actionable SQL queries for your data needs.

### Installation
```sh
# PyPI
pip install raxo
```

### Getting started
#### Refer to documentation to know more options
```python
# Importing necessary modules
from raxo.models import OpenAIChat
from raxo.embeddings import OpenAiEmbeddings
from raxo.vector import ChromaStore
from raxo import Raxo

open_ai = OpenAIChat(api_key="<API_KEY>", model="<MODEL_NAME>")
embed = OpenAiEmbeddings(api_key="<API_KEY>",
                         model="<MODEL_NAME>")
chroma = ChromaStore(em_function=embed)
# passing the required functions to create a raxo object
raxo = Raxo(llm=open_ai, vector_db=chroma, em_function=embed)
```

### Training Raxo
#### If you want to train the raxo [optional]
```python
raxo.train(ddl="""
CREATE TABLE Customer (
    CustomerID INT,
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    Email VARCHAR(255),
    Phone VARCHAR(20),
    PRIMARY KEY (CustomerID)
)""")

```
#### You can add raxo by adding relevant documentation.

```python
raxo.train(documentation="The table contains records of customers of a store")
```

#### Train by adding valid SQL's
```python
raxo.train(sql="SELECT DISTINCT FirstName FROM Customer")
```

### Generating SQL
```python
sql = raxo.ask("what are my region sales")
print(sql)
```
#### You will get the output
```sql
SELECT SUM(Sales), Region FROM sales_data GROUP BY Region ORDER BY SUM(sales);
```