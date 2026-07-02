import io
from datetime import datetime

import pandas as pd
import streamlit as st

from charts import create_chart
from safety import validate_sql
from sql_agent import explain_sql, generate_sql
from utils import execute_query, extract_schema

st.set_page_config(
    page_title="NL → SQL Query Builder",
    layout="wide"
)

st.title("NL → SQL Query Builder for SQLite")

if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.header("Settings")
    theme = st.selectbox("Theme", ["Light", "Dark"], index=0)
    chart_type = st.selectbox(
        "Preferred chart type",
        ["Auto", "Bar", "Line", "Scatter", "Pie"],
        index=0
    )

    if st.button("Clear query history"):
        st.session_state.history = []
        st.success("Query history cleared.")

if theme == "Dark":
    st.markdown(
        "<style>body{background-color:#0e1117;color:#f5f5f5;} .stButton>button{color:#fff;}</style>",
        unsafe_allow_html=True
    )

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

        if sql_query:
            st.subheader("Generated SQL")
            st.code(sql_query)

            safe, message = validate_sql(sql_query)

            if not safe:
                st.error(f"⚠️ {message}")
            else:
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

                    st.markdown("#### Data Preview")
                    st.write(df.head(5))

                    st.subheader("Query Explanation")
                    explanation = explain_sql(sql_query)
                    st.write(explanation)

                    st.subheader("Visualization")
                    fig = create_chart(df, chart_type)

                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No suitable chart found for the selected data and chart type.")

                    csv = df.to_csv(index=False).encode("utf-8")
                    json_data = df.to_json(orient="records", force_ascii=False)
                    excel_buffer = io.BytesIO()
                    df.to_excel(excel_buffer, index=False, engine="openpyxl")
                    excel_buffer.seek(0)

                    st.markdown("### Export Results")
                    export_cols = st.columns(3)
                    with export_cols[0]:
                        st.download_button(
                            "Download CSV",
                            csv,
                            "results.csv",
                            "text/csv"
                        )
                    with export_cols[1]:
                        st.download_button(
                            "Download JSON",
                            json_data,
                            "results.json",
                            "application/json"
                        )
                    with export_cols[2]:
                        st.download_button(
                            "Download Excel",
                            excel_buffer,
                            "results.xlsx",
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

                    st.session_state.history.append({
                        "question": user_query,
                        "sql": sql_query,
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
        else:
            st.error("Failed to generate SQL query. Check your API key in Streamlit Cloud secrets.")

st.subheader("Query History")

if st.session_state.history:
    for item in reversed(st.session_state.history):
        with st.expander(f"{item['time']} — {item['question']}"):
            st.write("**SQL Query**")
            st.code(item["sql"])
else:
    st.info("No queries have been run yet.")