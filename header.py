import dash_mantine_components as dmc

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
            dmc.Title("Pasar Padel"),
        ],
        h="100%",
        px="md",
    )
)