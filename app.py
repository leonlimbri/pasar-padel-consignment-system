"""app.py
Generate the Flask server and initialize the WebApp.
Store the login-page layout + initialization of the layout-page
"""

import os, dotenv, json
import dash_mantine_components as dmc
from dash import Dash, html, dcc, Output, Input, State, no_update, page_container
from flask import Flask, session
from header import page_header
from navbar import page_navbar

# Flask Server + Initialize App
# -----------------------------
dotenv.load_dotenv()
server = Flask(__name__)
server.secret_key = os.environ.get("SECRET_KEY")
USER_DETAILS = json.loads(os.environ.get("USER_DETAILS"))
app = Dash(
    __name__,
    server = server,
    use_pages = True,
    url_base_pathname = "/",
    suppress_callback_exceptions=True,
)
app.layout = dmc.MantineProvider(
    children=[
        dcc.Location(id="url", refresh=False),
        html.Div(id="protected-layout"),
    ]
)

# Login Page
# ----------
page_login = dmc.Center(
    dmc.Paper(
         [
            dmc.Title("Pasar Padel", order=2),
            dmc.TextInput(label="Username", id="input-login", placeholder="Masukkan username anda", mt="lg"),
            dmc.PasswordInput(label="Password", id="input-password", placeholder="Masukkan password anda", mt="sm"),
            dmc.Button("Login", id="button-login", fullWidth=True, mt="sm", size="sm"),
            dmc.Text(id="text-login-warning", size="xs", c="red")
        ],
        shadow="sm",
        p="xl",
        withBorder=True,
        style={"width": 350},
    ),
    style={"height": "100vh"}
)

# Page Layouts
# ------------
page_layout = dmc.AppShell(
    [
        page_header,
        page_navbar,
        page_container
    ],
    id="appshell-main",
    header={"height": 80},
    navbar={"width": 300, "breakpoint": "sm", "collapsed": {"mobile": True, "desktop": False}},
    padding="md",
)

# CALLBACKS to handle any login / displaying protected layouts
# ------------------------------------------------------------
@app.callback(
    Output("protected-layout", "children"),
    Input("url", "pathname"),
)
def display_protected_pages(pathname):
    if not session.get("logged_in") or pathname == "/logout":
        session["logged_in"], session["name"], session["role"] = False, None, None
        if pathname == "/login": return page_login
        return dcc.Location(href="/login", id="redirect-login")
    else:
        return page_layout

@app.callback(
    Output("text-login-warning", "children"),
    Output("url", "pathname"),
    Input("button-login", "n_clicks"),
    State("input-login", "value"),
    State("input-password", "value"),
)
def handle_login(n_clicks, username, password):
    if not n_clicks:
        return no_update, no_update

    print(username, password, USER_DETAILS)
    if username in USER_DETAILS and USER_DETAILS.get(username).get("password") == password:
        user = USER_DETAILS.get(username)
        session["logged_in"] = True
        for key in ["name", "role"]: session[key] = user.get(key)
        return "", "/"
    
    return "Invalid username or password", no_update

# CALLBACKS to change how the login text changes
# ----------------------------------------------
@app.callback(
    Output("text-login-name", "children"),
    Input("url", "pathname")
)
def adjust_login_title(urls):
    return f"Login: {session.get('name')} [{session.get('role')}]"

# CALLBACKS to open/close burger menu on mobile
# ---------------------------------------------
@app.callback(
    Output("appshell-main", "navbar"),
    Input("burger-menu", "opened"),
    State("appshell-main", "navbar"),
)
def toggle_navbar(mobile_opened, navbar):
    navbar["collapsed"]={"mobile": not mobile_opened,}
    return navbar

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)