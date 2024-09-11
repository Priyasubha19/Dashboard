import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import firebase_admin
from firebase_admin import credentials, db
import collections

# Initialize Firebase
cred = credentials.Certificate(r'D:\unity\fir-tounity-bdec9-firebase-adminsdk-ugkj9-349b15c4b1.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fir-tounity-bdec9-default-rtdb.firebaseio.com/'
})

# Function to retrieve data from Firebase
def get_status_data():
    ref = db.reference('status')
    data = ref.get()
    print("Retrieved data from Firebase:", data)
    return data

# Store the last N data points to plot
buffer_size = 10
x_data = collections.deque(maxlen=buffer_size)
y_data = collections.deque(maxlen=buffer_size)
z_data = collections.deque(maxlen=buffer_size)
timestamps = collections.deque(maxlen=buffer_size)

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout
app.layout = dbc.Container(
    [
        # Main heading
        dbc.Row(
            dbc.Col(
                html.H1("Firebase Real-time Data Graphs", className="text-center mt-4 mb-4")
            )
        ),
        dcc.Interval(
            id='interval-component',
            interval=5*1000,  # in milliseconds, here it's 5 seconds
            n_intervals=0
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='x-graph'), md=4),
                dbc.Col(dcc.Graph(id='y-graph'), md=4),
                dbc.Col(dcc.Graph(id='z-graph'), md=4),
            ]
        )
    ],
    fluid=True
)

# Callback to update all graphs with real-time data
@app.callback(
    [Output('x-graph', 'figure'),
     Output('y-graph', 'figure'),
     Output('z-graph', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_graphs(n):
    # Fetch data from Firebase
    status_data = get_status_data()

    # Extract x_pos, y_pos, z_pos from Firebase data
    if status_data:
        x = status_data.get('x_pos', 0)
        y = status_data.get('y_pos', 0)
        z = status_data.get('z_pos', 0)

        # Add to the deque buffers
        x_data.append(x)
        y_data.append(y)
        z_data.append(z)
        timestamps.append(n)  # Use the interval count as a pseudo-timestamp

    # Plot X-axis data
    x_trace = go.Scatter(
        x=list(timestamps),
        y=list(x_data),
        mode='lines+markers',
        name='X-axis'
    )
    x_layout = go.Layout(
        title="X Axis Data",
        xaxis=dict(title="Update Interval"),
        yaxis=dict(title="X Values")
    )
    x_figure = go.Figure(data=[x_trace], layout=x_layout)

    # Plot Y-axis data
    y_trace = go.Scatter(
        x=list(timestamps),
        y=list(y_data),
        mode='lines+markers',
        name='Y-axis'
    )
    y_layout = go.Layout(
        title="Y Axis Data",
        xaxis=dict(title="Update Interval"),
        yaxis=dict(title="Y Values")
    )
    y_figure = go.Figure(data=[y_trace], layout=y_layout)

    # Plot Z-axis data
    z_trace = go.Scatter(
        x=list(timestamps),
        y=list(z_data),
        mode='lines+markers',
        name='Z-axis'
    )
    z_layout = go.Layout(
        title="Z Axis Data",
        xaxis=dict(title="Update Interval"),
        yaxis=dict(title="Z Values")
    )
    z_figure = go.Figure(data=[z_trace], layout=z_layout)

    return x_figure, y_figure, z_figure

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, port=8051)
