import dash_mantine_components as dmc

page_header = dmc.AppShellHeader(
    dmc.Group(
        [
            dmc.Burger(
                id="burger-menu",
                size="sm",
                hiddenFrom="sm",
                opened=False,
            ),
            dmc.Image(src="assets/favicon.ico", h=35, flex=0),
            dmc.Stack(
                [
                    dmc.Title("Pasar Padel"),
                    dmc.Text(id="text-login-name"),
                ],
                gap="0em",
            ),
        ],
        align="center",
        h="100%"
    ), 
    px="md"
)