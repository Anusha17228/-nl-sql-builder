import streamlit as st
import pandas as pd

from utils import extract_schema, execute_query
from sql_agent import generate_sql, explain_sql
from safety import validate_sql
from charts import create_chart

st.set_page_config(
    page_title="NL → SQL Query Builder",
    layout="wide"
)

st.title("NL → SQL Query Builder for SQLite")

if "history" not in st.session_state:
    st.session_state.history = []

uploaded_file = st.file_uploader(
    "Upload SQLite Database",
    type=["db", "sqlite"]
)

if uploaded_file:
    db_path = "uploaded.db"

    with open(db_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("Database uploaded successfully.")

    schema = extract_schema(db_path)

    st.subheader("Detected Schema")
    st.json(schema)

    user_query = st.text_input(
        "Ask your question in plain English"
    )

    if user_query:
        with st.spinner("Generating SQL..."):
            sql_query = generate_sql(
                user_query,
                schema
            )

        st.subheader("Generated SQL")
        st.code(sql_query)

        safe, message = validate_sql(sql_query)

        if safe:
            rows, columns, error = execute_query(
                db_path,
                sql_query
            )

            if error:
                st.error(error)

            else:
                df = pd.DataFrame(
                    rows,
                    columns=columns
                )

                st.subheader("Query Results")
                st.dataframe(df)

                st.subheader("Query Explanation")

                explanation = explain_sql(sql_query)

                st.write(explanation)

                st.subheader("Visualization")

                fig = create_chart(df)

                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No suitable chart found.")

                st.download_button(
                    "Download CSV",
                    df.to_csv(index=False),
                    "results.csv",
                    "text/csv"
                )

                st.session_state.history.append({
                    "question": user_query,
                    "sql": sql_query
                })

        else:
            st.error(message)

st.subheader("Query History")

for item in st.session_state.history:
    st.write("Question:", item["question"])
    st.code(item["sql"])