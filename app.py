import pandas as pd
from pathlib import Path
import dash
from dash import dcc, html
import plotly.express as px

# Load data
DATA_PATH = Path("data/pink_morsels_sales.csv")
df = pd.read_csv(DATA_PATH)

# Ensure correct data types
df["date"] = pd.to_datetime(df["date"])
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")

# Aggregate sales per day
daily_sales = (
    df.groupby("date", as_index=False)["sales"]
    .sum()
    .sort_values("date")
)

# Create Dash app
app = dash.Dash(__name__)

# Line chart
fig = px.line(
    daily_sales,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time (Price Increase on 15 Jan 2021)",
    labels={
        "date": "Date",
        "sales": "Total Sales ($)"
    }
)

# Add vertical line for price increase (NO annotation to avoid Plotly bug)
fig.add_vline(
    x=pd.to_datetime("2021-01-15"),
    line_dash="dash",
    line_color="red"
)

# App layout
app.layout = html.Div(
    children=[
        html.H1(
            "Pink Morsel Sales Visualiser",
            style={"textAlign": "center"}
        ),
        dcc.Graph(figure=fig)
    ]
)

# Run server
if __name__ == "__main__":
    app.run(debug=True)
