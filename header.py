"""header.py
Defines the top app-shell header component.
Shows the burger menu (mobile), app logo, app title, and logged-in user name.
"""

import dash_mantine_components as dmc

page_header = dmc.AppShellHeader(
    dmc.Group(
        [
            # Burger icon — only visible on mobile (hidden on sm+ screens)
            dmc.Burger(
                id="burger-menu",
                size="sm",
                hiddenFrom="sm",
                opened=False,
            ),

            # App logo
            dmc.Image(src="assets/favicon.ico", h=35, flex=0),

            # App title + logged-in user label
            dmc.Stack(
                [
                    dmc.Title("Pasar Padel"),
                    dmc.Text(id="text-login-name", size="sm"),
                ],
                gap="0em",
            ),
        ],
        align="center",
        h="100%",
    ),
    px="md",
)
