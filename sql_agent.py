from groq import Groq
import streamlit as st

# Get API key from Streamlit secrets
api_key = st.secrets.get("GROQ_API_KEY")

# Debug: Check if key is loaded
if not api_key:
    st.error("❌ GROQ_API_KEY not found in Streamlit secrets!")
    st.info("To fix this:")
    st.info("1. Go to your Streamlit Cloud app")
    st.info("2. Click ⚙️ (Settings) in the lower right")
    st.info("3. Click 'Secrets'")
    st.info("4. Add: GROQ_API_KEY = your_key_here")
    st.stop()

# Initialize Groq client
try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Failed to initialize Groq client: {e}")
    st.stop()


def generate_sql(user_query, schema):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": f"You are an SQL expert. Generate a SQL query for SQLite database with the following schema:\n{schema}"
                },
                {
                    "role": "user",
                    "content": user_query
                }
            ]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating SQL: {str(e)}")
        return None


def explain_sql(sql_query):
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