import plotly.express as px


def create_chart(df, preferred_type="Auto"):
    numeric_cols = df.select_dtypes(include="number").columns
    text_cols = df.select_dtypes(include="object").columns

    if preferred_type == "Auto":
        if len(text_cols) >= 1 and len(numeric_cols) >= 1:
            preferred_type = "Bar"
        elif len(numeric_cols) >= 2:
            preferred_type = "Scatter"
        elif len(numeric_cols) >= 1:
            preferred_type = "Line"
        else:
            return None

    if preferred_type == "Bar" and len(text_cols) >= 1 and len(numeric_cols) >= 1:
        return px.bar(
            df,
            x=text_cols[0],
            y=numeric_cols[0],
            title="Bar Chart"
        )

    if preferred_type == "Line" and len(numeric_cols) >= 1:
        x_col = text_cols[0] if len(text_cols) >= 1 else numeric_cols[0]
        y_col = numeric_cols[0]
        return px.line(
            df,
            x=x_col,
            y=y_col,
            title="Line Chart"
        )

    if preferred_type == "Scatter" and len(numeric_cols) >= 2:
        return px.scatter(
            df,
            x=numeric_cols[0],
            y=numeric_cols[1],
            title="Scatter Plot"
        )

    if preferred_type == "Pie" and len(text_cols) >= 1 and len(numeric_cols) >= 1:
        return px.pie(
            df,
            names=text_cols[0],
            values=numeric_cols[0],
            title="Pie Chart"
        )

    return None
