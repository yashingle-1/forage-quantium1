import pandas as pd
from pathlib import Path
import dash
from dash import dcc, html, Input, Output
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

# App layout
app.layout = html.Div(
    className="container",
    children=[
        html.H1("Pink Morsels Sales Dashboard", className="title"),

        html.Div(
            className="controls",
            children=[
                html.Label("Select Region:", className="label"),
                dcc.RadioItems(
                    id="region-radio",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    inline=True,
                    className="radio"
                ),
            ],
        ),

        dcc.Graph(id="sales-line-chart"),
    ],
)

# Callback to update graph
@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-radio", "value")
)
def update_chart(selected_region):

    if selected_region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["region"] == selected_region]

    fig = px.line(
        filtered_df,
        x="date",
        y="sales",
        title="Pink Morsels Sales Over Time",
        markers=True
    )

    fig.add_vline(
        x=("2021-01-15"),
        line_dash="dash",
        line_color="red",
        # annotation_text="Price Increase",
        # annotation_position="top right"
    )

    # Annotation added separately (SAFE)
    fig.add_annotation(
        x="2021-01-15",
        y=filtered_df["sales"].max(),
        text="Price Increase",
        showarrow=True,
        arrowhead=1,
        yanchor="bottom"
    )

    fig.update_layout(
        plot_bgcolor="#f9f9f9",
        paper_bgcolor="#f9f9f9",
        title_font_size=20,
        title_x=0.5
    )

    return fig

# # Line chart
# fig = px.line(
#     daily_sales,
#     x="date",
#     y="sales",
#     title="Pink Morsel Sales Over Time (Price Increase on 15 Jan 2021)",
#     labels={
#         "date": "Date",
#         "sales": "Total Sales ($)"
#     }
# )

# # Add vertical line for price increase (NO annotation to avoid Plotly bug)
# fig.add_vline(
#     x=pd.to_datetime("2021-01-15"),
#     line_dash="dash",
#     line_color="red"
# )

# # App layout
# app.layout = html.Div(
#     children=[
#         html.H1(
#             "Pink Morsel Sales Visualiser",
#             style={"textAlign": "center"}
#         ),
#         dcc.Graph(figure=fig)
#     ]
# )

# Run server
if __name__ == "__main__":
    app.run(debug=True)
