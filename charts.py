import plotly.express as px


def create_chart(df):
    numeric_cols = df.select_dtypes(include="number").columns
    text_cols = df.select_dtypes(include="object").columns

    if len(text_cols) >= 1 and len(numeric_cols) >= 1:
        fig = px.bar(
            df,
            x=text_cols[0],
            y=numeric_cols[0],
            title="Bar Chart"
        )
        return fig

    if len(numeric_cols) >= 2:
        fig = px.scatter(
            df,
            x=numeric_cols[0],
            y=numeric_cols[1],
            title="Scatter Plot"
        )
        return fig

    return None