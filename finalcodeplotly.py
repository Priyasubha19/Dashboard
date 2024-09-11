import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import firebase_admin
from firebase_admin import credentials, db
import collections
from twilio.rest import Client
from flask_mail import Mail, Message
from flask import Flask
import logging


# Initialize Firebase
cred = credentials.Certificate(r'D:\unity\fir-tounity-bdec9-firebase-adminsdk-ugkj9-349b15c4b1.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fir-tounity-bdec9-default-rtdb.firebaseio.com/'
})

# Twilio configuration
account_sid = 'AC6f65e347f3cc5d49a2d44255d11d733c'
auth_token = '77c697b2c5c223a18a77ed2285cfe6f8'
twilio_phone_number = '+16562230984'
to_phone_number = '+917603966072'
client = Client(account_sid, auth_token)

# Initialize Flask and Flask-Mail
server = Flask(__name__)
server.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='mupromill8000@gmail.com',
    MAIL_PASSWORD='bdxj dfsp rpqg rxxy',
    MAIL_DEFAULT_SENDER='mupromill8000@gmail.com'
)
mail = Mail(server)

# Function to send SMS
def send_sms(message):
    try:
        client.messages.create(
            body=message,
            from_=twilio_phone_number,
            to=to_phone_number
        )
        print("SMS sent successfully.")
    except Exception as e:
        print(f"Failed to send SMS: {e}")

# Function to send email
def send_email(subject, body):
    try:
        with server.app_context():
            msg = Message(subject, recipients=['recipient_email@gmail.com'])
            msg.body = body
            mail.send(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")        

# Function to retrieve data from Firebase
def get_data():
    ref = db.reference('status')
    data = ref.get()
    print("Retrieved data from Firebase:", data)  # Debugging: Print the retrieved data
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
        dbc.Row(
            dbc.Col(
                html.H2("INTELITEK PROMILL 8000", className="text-center mt-4 mb-4")
            )
        ),
        dcc.Interval(
            id='interval-component',
            interval=10*1000,
            n_intervals=0
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Coolant Temperature"),
                            dbc.CardBody(
                                dbc.Row(
                                    [
                                        dbc.Col(html.H4(id="coolant_temperature", className="card-title", style={"text-align": "left", "marginTop": "3px"})),
                                        dbc.Col(html.Img(src="https://icon-icons.com/icons2/571/PNG/512/thermometer-temperature-control-tool-weather-interface-symbol_icon-icons.com_54635.png", style={"width": "100%"}))
                                    ]
                                )
                            ),
                        ],
                        className="card-custom"
                    ),
                    md=2,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Door Status"),
                            dbc.CardBody(
                                dbc.Row(
                                    [
                                        dbc.Col(html.H4(id="door_status", className="card-title", style={"text-align": "left", "marginTop": "5px"})),
                                        dbc.Col(html.Img(src="https://cdn3.iconfinder.com/data/icons/real-estate-glyph-1/2048/637_-_Door-512.png", style={"width": "100%"}))
                                    ]
                                )
                            ),
                        ],
                        className="card-custom"
                    ),
                    md=2,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Coolant Level"),
                            dbc.CardBody(
                                dbc.Row(
                                    [
                                        dbc.Col(html.H4(id="coolant_level", className="card-title", style={"text-align": "left", "marginTop": "5px"})),
                                        dbc.Col(html.Img(src="https://th.bing.com/th/id/OIP.__dZPIC939uM2ghKIkt0egHaHa?w=597&h=597&rs=1&pid=ImgDetMain", style={"width": "100%"}))
                                    ]
                                )
                            ),
                        ],
                        className="card-custom"
                    ),
                    md=2,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Percentage"),
                            dbc.CardBody(
                                dbc.Row(
                                    [
                                        dbc.Col(html.H4(id="percentage", className="card-title", style={"text-align": "left", "marginTop": "5px"})),
                                        dbc.Col(html.Img(src="https://th.bing.com/th/id/R.c420f7860cc78af08d8d9dc0831cd9f2?rik=XiHaRwvDzr2jmQ&riu=http%3a%2f%2fwww.pngmart.com%2ffiles%2f7%2fPercentage-Transparent-PNG.png&ehk=AD%2bNWZkntNlrxfijt0%2fJY11CweJW2%2flbnIjYi9s1mJk%3d&risl=&pid=ImgRaw&r=0", style={"width": "100%"}))
                                    ]
                                )
                            ),
                        ],
                        className="card-custom"
                    ),
                    md=2,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Current"),
                            dbc.CardBody(
                                dbc.Row(
                                    [
                                        dbc.Col(html.H4(id="current_value", className="card-title", style={"text-align": "left", "marginTop": "5px"})),
                                        dbc.Col(html.Img(src="https://www.pngrepo.com/download/75634/electric-current-symbol.png", style={"width": "100%"}))
                                    ]
                                )
                            ),
                        ],
                        className="card-custom"
                    ),
                    md=2,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Operator Status"),
                            dbc.CardBody(
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.Div(
                                                [
                                                    html.H4(id="operatorStatus", className="card-title", style={"text-align": "left", "marginTop": "5px"}),
                                                    dbc.Button("Alert Operator", id="alert-button", color="danger", className="me-2", style={"display": "block", "margin": "5px auto"}),
                                                    html.Div(id="alert-output", style={"text-align": "center"})
                                                ]
                                            )
                                        ),
                                        dbc.Col(html.Img(src="https://static.vecteezy.com/system/resources/previews/016/009/835/original/the-human-icon-and-logo-vector.jpg", style={"width": "100%"}))
                                    ]
                                )
                            ),
                        ],
                        className="card-custom"
                    ),
                    md=2,
                ),

            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='x-graph'), md=4),
                dbc.Col(dcc.Graph(id='y-graph'), md=4),
                dbc.Col(dcc.Graph(id='z-graph'), md=4),
            ]
        ),
    ],
    fluid=True
)

# Define the callbacks for updating the cards and graphs
@app.callback(
    [
        Output("coolant_temperature", "children"),
        Output("door_status", "children"),
        Output("coolant_level", "children"),
        Output("current_value", "children"),
        Output("percentage", "children"),
        Output("operatorStatus", "children"),
        Output('x-graph', 'figure'),
        Output('y-graph', 'figure'),
        Output('z-graph', 'figure')
    ],
    [Input("interval-component", "n_intervals")]
)
def update_content(n):
    # Retrieve data from Firebase
    data = get_data()
    
    coolant_temp = data.get('coolant_temperature', 'N/A')
    door_Status = data.get('door_status', 'N/A')
    coolantLevel = data.get('coolant_level', 'N/A')
    current = data.get('current_value', 'N/A')
    Percentage = data.get('percentage', 'N/A')
    operator_Status = data.get('operatorStatus', '')

    # Check and handle if current is a tuple
    if isinstance(current, tuple):
        current = current[0]  # Extract the value from the tuple
    
    # Extract x_pos, y_pos, z_pos from Firebase data for graphs
    x = data.get('x_pos', 0)
    y = data.get('y_pos', 0)
    z = data.get('z_pos', 0)
    timestamp = data.get('timestamp', 'N/A')

    # Append data to deques for graph plotting
    x_data.append(x)
    y_data.append(y)
    z_data.append(z)
    timestamps.append(timestamp)

    # Create traces for graphs
    x_trace = go.Scatter(x=list(timestamps), y=list(x_data), mode='lines+markers', name='X Position')
    y_trace = go.Scatter(x=list(timestamps), y=list(y_data), mode='lines+markers', name='Y Position')
    z_trace = go.Scatter(x=list(timestamps), y=list(z_data), mode='lines+markers', name='Z Position')

    # Create figures for each axis
    x_fig = go.Figure(data=[x_trace], layout=go.Layout(title='X Position Over Time', xaxis=dict(title='Time'), yaxis=dict(title='X Position')))
    y_fig = go.Figure(data=[y_trace], layout=go.Layout(title='Y Position Over Time', xaxis=dict(title='Time'), yaxis=dict(title='Y Position')))
    z_fig = go.Figure(data=[z_trace], layout=go.Layout(title='Z Position Over Time', xaxis=dict(title='Time'), yaxis=dict(title='Z Position')))

    return coolant_temp, door_Status, coolantLevel, current, percentage, operator_Status, x_fig, y_fig, z_fig

# Setup logging
logging.basicConfig(level=logging.INFO)  

# Callback for alert button
@app.callback(
    Output("alert-output", "children"),
    [Input("alert-button", "n_clicks")]
)
def send_alert(n_clicks):
    if n_clicks:
        try:
            message = "Alert: Please check the machine."
            logging.info("Attempting to send SMS alert...")
            send_sms(message)
            logging.info("SMS alert sent successfully.")
            
            logging.info("Attempting to send email alert...")
            send_email("Operator Alert", message)
            logging.info("Email alert sent successfully.")
            
            return "Alert sent!"
        except Exception as e:
            logging.error(f"Failed to send alert: {e}")
            return "Failed to send alert. Check logs for details."
    return ""

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
