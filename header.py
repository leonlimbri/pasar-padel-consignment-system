import dash_mantine_components as dmc
from dash import Output, Input, callback
from flask import session

logo = "assets/favicon.ico"
PageHeader = dmc.AppShellHeader(
    dmc.Group(
        [
            dmc.Burger(
                id = "mobile-burger",
                size = "sm",
                hiddenFrom = "sm",
                opened=False,
            ),
            dmc.Burger(
                id = "desktop-burger",
                size = "sm",
                visibleFrom = "sm",
                opened=True,
            ),
            dmc.Image(src = logo, h = 35, flex = 0),
            dmc.Text(id="title-text"),
        ],
        h="100%",
        px="md",
    )
)

@callback(
    Output("title-text", "children"),
    Input("url", "pathname")
)
def adjust_title(urls):
    if urls:
        username=session.get("username")
        return [
            dmc.Title(f"Pasar Padel"),
            dmc.Text(f"Login: {username}", size="xs")
        ]
    else:
        return None