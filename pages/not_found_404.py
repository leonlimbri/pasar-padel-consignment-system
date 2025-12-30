import dash_mantine_components as dmc
from dash import register_page

register_page(__name__)
layout=dmc.AppShellMain(
    [
        dmc.Title("404 - Page Not Found"),
        dmc.Text("The page you are looking for does not exist."),
        dmc.NavLink("Go to Home Page", href="/"),
    ]
)