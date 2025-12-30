import dash_mantine_components as dmc
import os
from dash import Dash, html, Input, Output, State, callback, page_container, dcc, no_update
from flask import Flask, session

# Server
server=Flask(__name__)
server.secret_key=os.environ.get("SECRET_KEY")
app=Dash(
    __name__,
    server=server,
    use_pages=True,
    url_base_pathname="/",
    suppress_callback_exceptions=True,
)


text_login={
    "title": "Pasar Padel",
    "subtitle-username": "Username", 
    "placeholder-username": "Masukkan username anda", 
    "subtitle-password": "Password", 
    "placeholder-password": "Masukkan password anda", 
    "button-login": "Login", 
}

# Login Layout
login_layout=dmc.Center(
    dmc.Paper(
        children=[
            dmc.Title(
                children=text_login.get("title"), 
                order=2
            ),
            dmc.TextInput(
                id="input-login", 
                label=text_login.get("subtitle-username"), 
                placeholder=text_login.get("placeholder-username"), 
                mt="lg"
            ),
            dmc.PasswordInput(
                id="input-password", 
                label=text_login.get("subtitle-password"), 
                placeholder=text_login.get("placeholder-password"), 
                mt="sm"
            ),
            dmc.Button(
                id="login-btn", 
                children="Login", 
                fullWidth=True, 
                mt="sm", 
                size="sm"
            ),
            dmc.Text(
                id="login-message", 
                size="xs", 
                c="red"
            ),
        ],
        shadow="sm",
        p="xl",
        withBorder=True,
        style={"width": 350},
    ),
    style={"height": "100vh"},
)

appshell_layout=dmc.AppShell(
    header={"height": 75},
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"mobile": True, "desktop": False},
    },
    padding="md",
    id="appshell",
)

# # app.layout=dmc.MantineProvider(layout)
# app.layout=dmc.MantineProvider(
#     children=[
#         dcc.Location(id="url", refresh=False),
#         html.Div(id="protected-layout"),
#     ]
# )

# @app.callback(
#     Output("protected-layout", "children"),
#     Input("url", "pathname"),
#     prevent_initial_call=False,
# )
# def display_page(pathname):
#     if not session.get("logged_in"):
#         if pathname == "/login":
#             return login_layout
#         # redirect any unauthorized request to login
#         return dcc.Location(href="/login", id="redirect-login")

#     # handle logout
#     if pathname == "/logout":
#         session["logged_in"]=False
#         session["user-id"]=None
#         session["role"]=None
#         return dcc.Location(href="/login", id="redirect-logout")

#     # otherwise show full app
#     return appshell_layout

# @app.callback(
#     Output("login-message", "children"),
#     Output("url", "pathname", allow_duplicate=True),
#     Input("login-btn", "n_clicks"),
#     State("username", "value"),
#     State("password", "value"),
#     prevent_initial_call=True,
# )
# def handle_login(n_clicks, username, password):
#     if not n_clicks:
#         return no_update, no_update

#     if username in USER_DETAILS and USER_DETAILS.get(username).get("password") == password:
#         session["logged_in"]=True
#         session["username"]=USER_DETAILS.get(username).get("name")
#         session["role"]=USER_DETAILS.get(username).get("role")
#         return "", "/"
#     return "Invalid username or password", no_update

# @callback(
#     Output("appshell", "navbar"),
#     Input("mobile-burger", "opened"),
#     State("appshell", "navbar"),
# )
# def toggle_navbar(mobile_opened, navbar):
#     navbar["collapsed"]={
#         "mobile": not mobile_opened,
#     }
#     return navbar

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)