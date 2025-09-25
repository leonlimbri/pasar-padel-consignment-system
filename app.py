import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback, page_container, dcc
from navbar import NavigationBar
from header import PageHeader

app = Dash(use_pages=True)
layout = dmc.AppShell(
    [
        dcc.Location(id="url", refresh=False),
        PageHeader,
        NavigationBar,
        page_container,
    ],
    header={"height": 75},
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"mobile": True, "desktop": False},
    },
    padding="md",
    id="appshell",
)

app.layout = dmc.MantineProvider(layout)

@callback(
    Output("appshell", "navbar"),
    Input("mobile-burger", "opened"),
    Input("desktop-burger", "opened"),
    Input("url", "pathname"),
    State("appshell", "navbar"),
)
def toggle_navbar(mobile_opened, desktop_opened, pathname, navbar):
    navbar["collapsed"] = {
        "mobile": not mobile_opened,
        "desktop": not desktop_opened,
    }
    return navbar

if __name__ == "__main__":
    # app.run(debug=True, host='0.0.0.0', port = 8080) # Run locally
    app.run()
