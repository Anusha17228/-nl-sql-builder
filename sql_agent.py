from groq import Groq
import streamlit as st

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)


def generate_sql(user_query, schema):
    prompt = f"""
You are an expert SQLite SQL generator.

Database schema:
{schema}

Rules:
1. Only SELECT queries
2. Never use INSERT/UPDATE/DELETE/DROP
3. Use JOIN if required
4. Use LIMIT 100 by default
5. Return only SQL

User question:
{user_query}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    sql = response.choices[0].message.content.strip()
    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    return sql


def explain_sql(sql, question):
    prompt = f"""
Explain this SQL query simply.

Question:
{question}

SQL:
{sql}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()