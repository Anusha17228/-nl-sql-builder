import os
import re

import streamlit as st
from groq import Groq


def get_api_key():
    try:
        return st.secrets.get("GROQ_API_KEY")
    except Exception:
        return os.getenv("GROQ_API_KEY")


api_key = get_api_key()

if api_key:
    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        client = None
        st.error(f"Failed to initialize Groq client: {e}")
else:
    client = None
    st.warning(
        "GROQ_API_KEY not set. Add it to .streamlit/secrets.toml or set the environment variable to enable AI features."
    )


def generate_sql(user_query, schema):
    if client is None:
        return "Please configure GROQ_API_KEY to enable SQL generation."

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": f"You are an SQL expert. Generate ONLY a SQL query for SQLite database. No explanations. Return ONLY the SQL code starting with SELECT.\n\nSchema:\n{schema}"
                },
                {
                    "role": "user",
                    "content": user_query
                }
            ]
        )
        
        sql_response = response.choices[0].message.content.strip()
        
        # Find the first SELECT statement
        select_match = re.search(r'SELECT\s+.*?(?=;|$)', sql_response, re.IGNORECASE | re.DOTALL)
        
        if select_match:
            sql_query = select_match.group(0).strip()
            return sql_query
        
        return sql_response
    except Exception as e:
        st.error(f"Error generating SQL: {str(e)}")
        return None


def explain_sql(sql_query):
    if client is None:
        return "Please configure GROQ_API_KEY to enable query explanations."

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Explain this SQL query in simple terms."
                },
                {
                    "role": "user",
                    "content": sql_query
                }
            ]
        )

        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error explaining SQL: {str(e)}")
        return None