import dash_mantine_components as dmc
from dash import register_page, dcc

register_page(__name__, "/caption-ig")
layout=dmc.AppShellMain(
    [
        dmc.Title("Sample"),
        dmc.Text(
            [
                "Sedang dibuat... ",
                dcc.Link("Kembali ke halaman utama", href="/"),
            ],
        )
    ]
)

# TODO: Create Caption IG from Consignment List
# TODO: Add copy button
