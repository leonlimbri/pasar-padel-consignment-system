"""app.py
Entry point for the Pasar Padel Dash application.

Responsibilities:
  - Create the Flask server and Dash app instance.
  - Define the login page and the main protected app layout.
  - Register callbacks for login, auth, navbar toggle, theme.
"""

import os
import json

import dotenv
import psutil
import dash_mantine_components as dmc
from dash import Dash, html, dcc, Output, Input, State, no_update, page_container, clientside_callback
from flask import Flask, session

from header import page_header
from navbar import page_navbar
from assets.colors import theme_colors_dark, theme_colors_light

# ── Flask server + Dash app initialisation ────────────────────────────────────
dotenv.load_dotenv()

server = Flask(__name__)
server.secret_key = os.environ.get("SECRET_KEY")

USER_DETAILS = json.loads(os.environ.get("USER_DETAILS"))
IS_LOCAL     = os.environ.get("IS_LOCAL", "true").lower() == "true"

app = Dash(
    __name__,
    server=server,
    use_pages=True,
    url_base_pathname="/",
    suppress_callback_exceptions=True,
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no",
        },
    ],
)

# psutil process handle used to track memory usage in local/dev mode
process = psutil.Process(os.getpid())

app.layout = dmc.MantineProvider(
    id="mantine-provider",
    children=[
        dcc.Location(id="url", refresh=False),
        html.Div(id="protected-layout"),
        # Fires every second to poll memory usage (dev only)
        dcc.Interval(id="interval-memory", interval=1000 if IS_LOCAL else 0, n_intervals=0),
    ],
)

# ── Login page layout ─────────────────────────────────────────────────────────
page_login = dmc.Center(
    dmc.Paper(
        [
            dmc.Title("Pasar Padel", order=2),
            dmc.TextInput(
                label="Username",
                id="input-login",
                placeholder="Masukkan username anda",
                mt="lg",
            ),
            dmc.PasswordInput(
                label="Password",
                id="input-password",
                placeholder="Masukkan password anda",
                mt="sm",
            ),
            dmc.Button("Login", id="button-login", fullWidth=True, mt="sm", size="sm"),
            dmc.Text(id="text-login-warning", size="xs", c="red"),
        ],
        shadow="sm",
        p="xl",
        withBorder=True,
        style={"width": 350},
    ),
    style={"height": "100vh"},
)

# ── Authenticated app layout ──────────────────────────────────────────────────
page_layout = dmc.AppShell(
    [
        page_header,
        page_navbar,
        page_container,
    ],
    id="appshell-main",
    header={"height": 80},
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"mobile": True, "desktop": False},
    },
    padding="md",
)


# ── Auth callbacks ────────────────────────────────────────────────────────────

@app.callback(
    Output("protected-layout", "children"),
    Input("url", "pathname"),
)
def display_protected_pages(pathname):
    """Show the login page for unauthenticated users; otherwise show the app."""
    if not session.get("logged_in") or pathname == "/logout":
        # Clear session on logout or when not logged in
        session["logged_in"] = False
        session["name"]      = None
        session["role"]      = None
        if pathname == "/login":
            return page_login
        return dcc.Location(href="/login", id="redirect-login")
    return page_layout


@app.callback(
    Output("text-login-warning", "children"),
    Output("url", "pathname"),
    Input("button-login", "n_clicks"),
    State("input-login", "value"),
    State("input-password", "value"),
)
def handle_login(n_clicks, username, password):
    """Validate credentials and redirect to home on success."""
    if not n_clicks:
        return no_update, no_update

    uname = username.lower()
    if uname in USER_DETAILS and USER_DETAILS[uname].get("password") == password:
        session["logged_in"] = True
        session["role"]      = uname.title()
        return "", "/"

    return "Invalid username or password", no_update


@app.callback(
    Output("text-login-name", "children"),
    Input("url", "pathname"),
)
def adjust_login_title(pathname):
    """Keep the header user label in sync with the current session role."""
    return f"Login: {session.get('role')}"


# ── Navbar / UI callbacks ─────────────────────────────────────────────────────

@app.callback(
    Output("appshell-main", "navbar"),
    Input("burger-menu", "opened"),
    State("appshell-main", "navbar"),
)
def toggle_navbar(mobile_opened, navbar):
    """Open or close the sidebar when the mobile burger menu is clicked."""
    navbar["collapsed"] = {"mobile": not mobile_opened}
    return navbar


# Dark/light theme — clientside callback avoids a round-trip to the server
clientside_callback(
    """
    (switchOn) => {
        document.documentElement.setAttribute(
            'data-mantine-color-scheme',
            switchOn ? 'dark' : 'light'
        );
        return window.dash_clientside.no_update;
    }
    """,
    Output("switch-color-scheme", "id"),
    Input("switch-color-scheme", "checked"),
    Input("url", "pathname"),
)


@app.callback(
    Output("mantine-provider", "theme"),
    Input("switch-color-scheme", "checked"),
    supress_callback_exceptions=True,
)
def toggle_color_scheme(switch_on):
    """Update the Mantine theme colors when the dark/light switch changes."""
    return {
        "primaryColor": "first",
        "autoContrast": True,
        "colors": theme_colors_dark if switch_on else theme_colors_light,
    }


# ── Memory usage monitor (dev only) ──────────────────────────────────────────

@app.callback(
    Output("memory-usage-text", "children"),
    Output("memory-usage-text", "color"),
    Input("interval-memory", "n_intervals"),
)
def update_memory_usage(n, is_local=IS_LOCAL):
    """Poll the process RSS memory and display it in the sidebar.
    Turns red when usage exceeds 100 MB. Disabled in production.
    """
    if not is_local:
        return no_update, no_update

    used_mb = process.memory_info().rss / (1024 ** 2)
    color   = "red" if used_mb > 100 else "green"
    return f"Memory Usage: {used_mb:.2f} MB", color


# ── App entry point ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=IS_LOCAL)