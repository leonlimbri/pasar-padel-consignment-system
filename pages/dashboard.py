import dash_mantine_components as dmc
from dash import register_page, dcc

register_page(__name__, "/dashboard")
layout=dmc.AppShellMain(
    [
        dmc.Title("Sample Dashboard"),
        dmc.Text(
            [
                "Sedang dibuat... ",
                dcc.Link("Kembali ke halaman utama", href="/"),
            ],
        )
    ]
)

# TODO: Dashboard status barang consignment
# TODO: Persentase penjualan pasar padel vs tempat lain
# TODO: Financial omset dan profit
# TODO: Barang favorit yang banyak di post / terjual
# TODO: Barang favorit yang banyak di post / terjual
# TODO: Performance Sales (jumlah barang yang dijual + total $ yang dijual)
# TODO: Mobile view tidak disarankan...