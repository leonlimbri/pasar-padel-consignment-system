"""pages/not_found_404.py
Renders a simple 404 page for any unrecognised URL.
"""

import dash_mantine_components as dmc
from dash import register_page, dcc

register_page(__name__)

layout = dmc.AppShellMain(
    [
        dmc.Title("404 - Halaman Tidak Ditemukan!"),
        dmc.Text(
            [
                "Halaman yang anda cari tidak ada / belom terbuatkan. ",
                dcc.Link("Kembali ke halaman utama", href="/"),
            ],
        ),
    ]
)
