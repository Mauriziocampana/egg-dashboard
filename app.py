df = pd.read_csv("merged_data.csv", parse_dates=['date'])
df.set_index('date', inplace=True)

# Append weekly April–May data
weekly_data = pd.DataFrame({
    'date': pd.to_datetime([
        '2025-04-04', '2025-04-11', '2025-04-18', '2025-04-25',
        '2025-05-02', '2025-05-09'
    ]),
    'Price_Received_USD_Dozen': [3.26, 3.08, 3.13, 3.15, 3.29, 3.36]
})

# Optional: estimate production as NaN (or assign placeholder if available)
weekly_data['Egg_Production_Count'] = None  # or use placeholder values

# Merge into main DataFrame
weekly_data.set_index('date', inplace=True)
df = pd.concat([df, weekly_data])
df = df.sort_index()

# Calculate outbreak intensity columns
outbreak_cols = [
    'Birds_Killed',
    'Egg Producing Birds_Killed',
    'Chickens_Killed',
    'Non Chickens_Killed'
]

for col in outbreak_cols:
    if col in df.columns:
        intensity_col = f"{col}_Intensity"
        df[intensity_col] = df[col] / df[col].max()

# Rolling production columns
rolling_cols = {
    "Actual Production": "Egg_Production_Count",
    "3-Month Rolling": "Prod_Rolling3",
    "6-Month Rolling": "Prod_Rolling6",
    "9-Month Rolling": "Prod_Rolling9",
    "12-Month Rolling": "Prod_Rolling12"
}

for label, col in rolling_cols.items():
    if col not in df.columns:
        df[col] = df['Egg_Production_Count'].rolling(window=int(label.split('-')[0])).mean()

# Initialize Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H2("Wholesale vs. Egg Production with Outbreak Intensity"),

    html.Label("Select Production Metric:"),
    dcc.Dropdown(
        id='production-select',
        options=[{'label': k, 'value': v} for k, v in rolling_cols.items()],
        value='Egg_Production_Count'
    ),

    html.Label("Show Outbreak Shading for:"),
    dcc.Checklist(
        id='outbreak-checklist',
        options=[
            {'label': 'Total Birds Killed', 'value': 'Birds_Killed'},
            {'label': 'Egg Producers', 'value': 'Egg Producing Birds_Killed'},
            {'label': 'Chickens Killed', 'value': 'Chickens_Killed'},
            {'label': 'Non-Chickens', 'value': 'Non Chickens_Killed'}
        ],
        value=[]
    ),

    dcc.Graph(id='egg-production-graph')
])

@app.callback(
    Output('egg-production-graph', 'figure'),
    Input('production-select', 'value'),
    Input('outbreak-checklist', 'value')
)
def update_figure(selected_prod_col, selected_outbreaks):
    fig = go.Figure()

    # Price trace
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Price_Received_USD_Dozen'],
        name="Wholesale ($/Dozen)",
        yaxis="y1",
        line=dict(color="blue", width=2)
    ))

    # Selected production trace
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df[selected_prod_col],
        name=selected_prod_col,
        yaxis="y2",
        line=dict(color="orange", width=2)
    ))

    # Outbreak shading
    for col in selected_outbreaks:
        intensity_col = f"{col}_Intensity"
        if intensity_col in df.columns:
            for i in range(len(df) - 1):
                if df[col].iloc[i] > 0:
                    alpha = min(0.85, max(0.05, df[intensity_col].iloc[i]))
                    fig.add_shape(
                        type="rect",
                        x0=df.index[i],
                        x1=df.index[i + 1],
                        y0=0,
                        y1=1,
                        xref="x",
                        yref="paper",
                        fillcolor="red",
                        opacity=alpha,
                        line_width=0,
                        layer="below"
                    )

    # Add vertical marker for start of weekly data
    fig.add_shape(
        type="line",
        x0="2025-04-01", x1="2025-04-01",
        y0=0, y1=1,
        xref='x',
        yref='paper',
        line=dict(color="gray", dash="dot", width=1)
    )

    fig.add_annotation(
        x="2025-04-01",
        y=1,
        xref="x",
        yref="paper",
        text="Weekly Data Starts",
        showarrow=False,
        font=dict(size=12, color="gray"),
        xanchor='left',
        yanchor='bottom'
    )

    # Layout settings
    fig.update_layout(
        xaxis=dict(title="Date"),
        yaxis=dict(title="Wholesale ($/Dozen)", side='left', color='blue'),
        yaxis2=dict(title="Production", side='right', overlaying='y', color='orange'),
        height=700,
        margin=dict(l=50, r=50, t=60, b=50),
        plot_bgcolor='white',
        legend=dict(x=0.01, y=0.99)
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True, port=8051)

df = pd.read_csv("merged_data.csv", parse_dates=['date'])
df.set_index('date', inplace=True)

# Append weekly April–May data
weekly_data = pd.DataFrame({
    'date': pd.to_datetime([
        '2025-04-04', '2025-04-11', '2025-04-18', '2025-04-25',
        '2025-05-02', '2025-05-09'
    ]),
    'Price_Received_USD_Dozen': [3.26, 3.08, 3.13, 3.15, 3.29, 3.36]
})

# Optional: estimate production as NaN (or assign placeholder if available)
weekly_data['Egg_Production_Count'] = None  # or use placeholder values

# Merge into main DataFrame
weekly_data.set_index('date', inplace=True)
df = pd.concat([df, weekly_data])
df = df.sort_index()

# Calculate outbreak intensity columns
outbreak_cols = [
    'Birds_Killed',
    'Egg Producing Birds_Killed',
    'Chickens_Killed',
    'Non Chickens_Killed'
]

for col in outbreak_cols:
    if col in df.columns:
        intensity_col = f"{col}_Intensity"
        df[intensity_col] = df[col] / df[col].max()

# Rolling production columns
rolling_cols = {
    "Actual Production": "Egg_Production_Count",
    "3-Month Rolling": "Prod_Rolling3",
    "6-Month Rolling": "Prod_Rolling6",
    "9-Month Rolling": "Prod_Rolling9",
    "12-Month Rolling": "Prod_Rolling12"
}

for label, col in rolling_cols.items():
    if col not in df.columns:
        df[col] = df['Egg_Production_Count'].rolling(window=int(label.split('-')[0])).mean()

# Initialize Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H2("Wholesale vs. Egg Production with Outbreak Intensity"),

    html.Label("Select Production Metric:"),
    dcc.Dropdown(
        id='production-select',
        options=[{'label': k, 'value': v} for k, v in rolling_cols.items()],
        value='Egg_Production_Count'
    ),

    html.Label("Show Outbreak Shading for:"),
    dcc.Checklist(
        id='outbreak-checklist',
        options=[
            {'label': 'Total Birds Killed', 'value': 'Birds_Killed'},
            {'label': 'Egg Producers', 'value': 'Egg Producing Birds_Killed'},
            {'label': 'Chickens Killed', 'value': 'Chickens_Killed'},
            {'label': 'Non-Chickens', 'value': 'Non Chickens_Killed'}
        ],
        value=[]
    ),

    dcc.Graph(id='egg-production-graph')
])

@app.callback(
    Output('egg-production-graph', 'figure'),
    Input('production-select', 'value'),
    Input('outbreak-checklist', 'value')
)
def update_figure(selected_prod_col, selected_outbreaks):
    fig = go.Figure()

    # Price trace
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Price_Received_USD_Dozen'],
        name="Wholesale ($/Dozen)",
        yaxis="y1",
        line=dict(color="blue", width=2)
    ))

    # Selected production trace
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df[selected_prod_col],
        name=selected_prod_col,
        yaxis="y2",
        line=dict(color="orange", width=2)
    ))

    # Outbreak shading
    for col in selected_outbreaks:
        intensity_col = f"{col}_Intensity"
        if intensity_col in df.columns:
            for i in range(len(df) - 1):
                if df[col].iloc[i] > 0:
                    alpha = min(0.85, max(0.05, df[intensity_col].iloc[i]))
                    fig.add_shape(
                        type="rect",
                        x0=df.index[i],
                        x1=df.index[i + 1],
                        y0=0,
                        y1=1,
                        xref="x",
                        yref="paper",
                        fillcolor="red",
                        opacity=alpha,
                        line_width=0,
                        layer="below"
                    )

    # Add vertical marker for start of weekly data
    fig.add_shape(
        type="line",
        x0="2025-04-01", x1="2025-04-01",
        y0=0, y1=1,
        xref='x',
        yref='paper',
        line=dict(color="gray", dash="dot", width=1)
    )

    fig.add_annotation(
        x="2025-04-01",
        y=1,
        xref="x",
        yref="paper",
        text="Weekly Data Starts",
        showarrow=False,
        font=dict(size=12, color="gray"),
        xanchor='left',
        yanchor='bottom'
    )

    # Layout settings
    fig.update_layout(
        xaxis=dict(title="Date"),
        yaxis=dict(title="Wholesale ($/Dozen)", side='left', color='blue'),
        yaxis2=dict(title="Production", side='right', overlaying='y', color='orange'),
        height=700,
        margin=dict(l=50, r=50, t=60, b=50),
        plot_bgcolor='white',
        legend=dict(x=0.01, y=0.99)
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True, port=8051)