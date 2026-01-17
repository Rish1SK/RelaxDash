from groq import Groq
import os
import re
import sqlite3
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from pandas import DataFrame
import mysql.connector

load_dotenv()

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Lunarcy@1214", 
    "database": "relaxdash"
}

GROQ_MODEL = os.getenv('GROQ_MODEL')

client_sql = Groq()

sql_prompt = """You are an expert in understanding the database schema and generating SQL queries for a natural language question asked
pertaining to the data you have. The schema is provided in the schema tags. 
<schema> 
table: menu_items 

fields: 
id - integer (unique identifier for each product)
restaurant_id - integer (unique identifier for the restaurant)
restaurant_name - string (name of the restaurant)
name - string (name of the product)
description - string (description of the product)
price - float (price of the product in USD)
category - string (category of the product, e.g., plate, bowl, pizza, skewers, wrap, snack, salad, sandwich)
ingredients - string (list of ingredients in the product)
dietary_type - string (has only these values: vegan, veg, non-veg)


</schema>
The query should have all the fields in SELECT clause (i.e. SELECT *)
If a specific dish in the menu is asked, try to map it to the name field in the table.
If a specific category(bowl, pizza) is asked, map it to the category field in the table.
For example, if the question is "Show me all the bowls", then the SQL query should have a WHERE clause with category = 'bowl'. with %LIKE% operato
If the question is about ingredients, make sure to use the ingredients field in the WHERE clause with %LIKE% operator.
if the question is about a specific restaurant, use the restaurant_name field in the WHERE clause.
If the question is about price, make sure to use the price field in the WHERE clause with appropriate comparison operators.
If the question is about dietary type, use the dietary_type field in the WHERE clause. Remember if Veg is requested, it includes both 'veg' and 'vegan' values in the dietary_type field.
If the question is about dietary preferences or flavor profiles, make sure to use the description or ingredients field with %LIKE% operato
If you are not sure about how to filter, just use the %LIKE% operator with relevant keywords. Or just return all the items with SELECT * without any WHERE clause. 
Create a single SQL query for the question provided. 
If multiple filters are needed, use AND operator to combine them in the WHERE clause.

Just the SQL query is needed, nothing more. Always provide the SQL in between the <SQL></SQL> tags."""


comprehension_prompt = """You are an expert in understanding the context of the question and replying based on the data pertaining to the question provided. You will be provided with Question: and Data:. The data will be in the form of an array or a dataframe or dict. Reply based on only the data provided as Data for answering the question asked as Question. Do not write anything like 'Based on the data' or any other technical words. Just a plain simple natural language response.
The Data would always be in context to the question asked. So make sure the response is curated with the question and data. Make sure to note the column names to have some context, if needed, for your response.
There can also be cases where you are given an entire dataframe in the Data: field. Always remember that the data field contains the answer of the question asked. All you need to do is to always reply in the following format when asked about a product: 
Dish Name, Restaurant Name, description, dietary_type, price in dollars, . Take care that all the dishes are listed in list format, one line after the other. Not as a paragraph.
If there are more than 5 items, just show the top 5 items in your response.
For example:
1. Vegan Delight Bowl, Green Garden, A colorful mix of fresh veggies and grains, Vegan, 9.99 dollars.
2. Chilli Paneer Skewers, Spice Hub, Spicy paneer cubes grilled on skewers, Veg 7.99 dollars.

"""


def generate_sql_query(question):
    chat_completion = client_sql.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": sql_prompt,
            },
            {
                "role": "user",
                "content": question,
            }
        ],
        model=os.environ['GROQ_MODEL'],
        temperature=0.2,
        #max_tokens=1024
    )

    return chat_completion.choices[0].message.content


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def run_query(query):
    if query.strip().upper().startswith('SELECT'):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        df = pd.DataFrame(results)
        cursor.close()
        conn.close()
        return df
        


def data_comprehension(question, context):
    chat_completion = client_sql.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": comprehension_prompt,
            },
            {
                "role": "user",
                "content": f"QUESTION: {question}. DATA: {context}",
            }
        ],
        model=os.environ['GROQ_MODEL'],
        temperature=0.2,
        # max_tokens=1024
    )

    return chat_completion.choices[0].message.content



def sql_chain(question):
    sql_query = generate_sql_query(question)
    pattern = "<SQL>(.*?)</SQL>"
    matches = re.findall(pattern, sql_query, re.DOTALL)

    if len(matches) == 0:
        return "Sorry, LLM is not able to generate a query for your question"

    print(matches[0].strip())

    response = run_query(matches[0].strip())
    if response is None:
        return "Sorry, there was a problem executing SQL query"

    context = response.to_dict(orient='records')

    answer = data_comprehension(question, context)
    return answer


if __name__ == "__main__":
    # question = "All shoes with rating higher than 4.5 and total number of reviews greater than 500"
    # sql_query = generate_sql_query(question)
    # print(sql_query)
    question = "I want some veg spicy dish"
    # question = "Show me 3 running shoes for woman"
    # question = "sfsdfsddsfsf"
    answer = sql_chain(question)
    print(answer)
