import dash_mantine_components as dmc
from dash import register_page
from dash_iconify import DashIconify

register_page(__name__, path="/")

# Components
# ----------
dividerForFilter = dmc.Divider(label="Filter data consignment berdasarkan kriteria berikut:", labelPosition="center")
subtitleTexts = "Tambah / Edit data consignmentmu disini. Untuk menambahkan data consignment, silahkan klik tombol 'Add Consignment' dibawah. Untuk mengedit data consignment, silahkan klik dua kali pada baris data consignment yang ingin diubah."

# Selectors & Buttons
# -------------------
selectItemType = dmc.MultiSelect(
    id="multiselect-filter-item-type", clearable=True,
    label="Tipe Barang", description="Pilih tipe consignment untuk memfilter data consignment",
    data=["Racket", "Shirt", "Shoes", "Bag", "Others"],
)
selectItemStatus = dmc.MultiSelect(
    id="multiselect-filter-item-status", clearable=True, 
    label="Status Barang", description="Pilih status consignment untuk memfilter data consignment",
    data=["New", "Posted", "Sold", "Shipped", "Completed", "Completed Elsewhere"],
)
buttonRegister = dmc.Box([
    dmc.Button(
        id="button-add-consignment", 
        children=dmc.Text("Tambah Consignment Baru", size="sm"),
        leftSection=DashIconify(icon="gg:add"),
        fullWidth=True,
        color="#5B8710"
    ),
    dmc.Tooltip(
        target="#button-add-consignment",
        label="Klik untuk menambahkan data consignment baru",
        position="top",
        withArrow=True,
        transitionProps={
            "transition": "slide-up", 
            "duration": 200,
            "timingFunction": "ease"
        },
        color="#5B8710"
    )
])
buttonRefresh = dmc.Box([
    dmc.Button(
        id="button-refresh-consignment", 
        children=dmc.Text("Refresh Tabel Consignment", size="sm"),
        leftSection=DashIconify(icon="material-symbols:refresh"),
        fullWidth=True,
        color="#3C5909"
    ),
    dmc.Tooltip(
        target="#button-refresh-consignment",
        label="Klik untuk meng-refresh data pada tabel consignment",
        position="top",
        withArrow=True,
        transitionProps={
            "transition": "slide-up", 
            "duration": 200,
            "timingFunction": "ease"
        },
        color="#3C5909"
    )
])

layout=dmc.AppShellMain(
    [
        dmc.Title("Consignments"),
        dmc.Text(subtitleTexts, size="sm", visibleFrom="sm", mb=20),
        dmc.Text(subtitleTexts, size="xs", hiddenFrom="sm", mb=20),
        dmc.Stack(
            [
                dividerForFilter,
                dmc.Group([selectItemType, selectItemStatus, buttonRegister, buttonRefresh], justify="space-evenly", gap="md", grow=True),
            ],
            visibleFrom="sm",
        ),
        dmc.Stack(
            [
                buttonRegister,
                dmc.Accordion(
                    children=dmc.AccordionItem([
                        dmc.AccordionControl("Filter Data Consignment", icon=DashIconify(icon="mingcute-filter-line")),
                        dmc.AccordionPanel(
                            dmc.Stack([selectItemType, selectItemStatus, buttonRefresh]),
                        ),
                    ], value="filter-accordion-item"),
                    chevronPosition="right",
                    radius="md",
                    variant="separated",
                )
            ],
            hiddenFrom="sm",
        ),
        # dmc.Divider("Filter data consignment berdasarkan kriteria berikut:")

    ]
)