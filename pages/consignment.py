import dash_mantine_components as dmc
import dash_ag_grid as dag
from dash import register_page, callback, Output, Input, State, html
from dash_iconify import DashIconify

register_page(__name__, path="/")

# Components & Selectors & Buttons
# --------------------------------
subtitleTexts = "Tambah / Edit data consignmentmu disini. Untuk menambahkan data consignment, silahkan klik tombol 'Add Consignment' dibawah. Untuk mengedit data consignment, silahkan klik dua kali pada baris data consignment yang ingin diubah."
consignment_type_options = ["Racket", "Shirt", "Shoes", "Bag", "Others"]

# Filters
# -------
selectItemType = dmc.MultiSelect(
    id="multiselect-filter-item-type", clearable=True,
    label="Tipe Barang", description="Pilih tipe consignment untuk memfilter data consignment",
    data=consignment_type_options,
)
selectItemStatus = dmc.MultiSelect(
    id="multiselect-filter-item-status", clearable=True, 
    label="Status Barang", description="Pilih status consignment untuk memfilter data consignment",
    data=["New", "Posted", "Sold", "Shipped", "Completed", "Completed Elsewhere"],
)

# Buttons
# -------
buttonRegister = dmc.Box([
    dmc.Button(
        id="button-add-consignment", 
        children=dmc.Text("Tambah Consignment Baru", size="sm"),
        leftSection=DashIconify(icon="gg:add"),
        fullWidth=True,
        color="first"
    ),
    dmc.Tooltip(
        target="#button-add-consignment",
        label="Klik untuk menambahkan data consignment baru",
        position="top", withArrow=True,
        transitionProps={
            "transition": "slide-up", 
            "duration": 200,
            "timingFunction": "ease"
        },
        color="first"
    )
])
buttonRefresh = dmc.Box([
    dmc.Button(
        id="button-refresh-consignment", 
        children=dmc.Text("Refresh Tabel Consignment", size="sm"),
        leftSection=DashIconify(icon="material-symbols:refresh"),
        fullWidth=True,
        color="second"
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
        color="second"
    )
])

# Data Table
# ----------
consignment_table_columns = [
    {"headerName": "Consignment ID", "field": "consignment_id", "type": "text"},
    {"headerName": "Tipe Barang", "field": "item_type", "type": "text", "filter": False},
    {"headerName": "Nama Barang", "field": "item_name", "type": "text"},
    {"headerName": "Harga Modal", "field": "price_modal", "type": "text"},
    {"headerName": "Harga di Instagram", "field": "price_posted", "type": "text"},
    {"headerName": "WA Seller", "field": "seller_wa", "type": "text"},
    {"headerName": "Nama Seller", "field": "seller_name", "type": "text"},
    {"headerName": "Lokasi", "field": "seller_location", "type": "text"},
    {"headerName": "Kondisi Barang", "field": "item_condition", "type": "text"},
    {"headerName": "Status Barang", "field": "item_status", "type": "text", "filter": False},
]
consignment_table = dag.AgGrid(
    id="aggrid-consignment-table",
    className="ag-theme-quartz",
    columnDefs=consignment_table_columns,
    rowData=[],
    defaultColDef={
        "sortable": True,
        "filter": True,
        "resizable": True,
        "minWidth": 150,
    },
    dashGridOptions={"pagination": True, "paginationPageSize": 10, "rowBuffer": 0},
    style={"height": "500px", "width": "100%"},
)

# Modals
# ------
modal_register_new=dmc.Modal(
    id="modal-register-consignment",
    size="lg",
    title=dmc.Title("Form Consignment Baru", order=3),
    children=dmc.Stack(
        [
            dmc.Text("Gunakan form dibawah ini untuk menginputkan data consignment baru. Setelah input data terbuat, data consignment bisa dipakai untuk pembuatan caption dan lainnya.", fz="xs"),
            dmc.Divider(),

            # Consignment Inputs
            dmc.Accordion(
                id="accordion-new-consignment",
                children=[
                    dmc.AccordionItem(
                        value="accordionitem-new-consignment-item-detail",
                        children=[
                            dmc.AccordionControl("Detail Barang", icon=DashIconify(icon="material-symbols:padel-outline",)),
                            dmc.AccordionPanel(
                                [
                                    dmc.Select(
                                        id="select-new-consignment-type", label="Tipe Consignment", size="xs",
                                        data=consignment_type_options,
                                        withAsterisk=True,
                                    ),

                                    # Racket Consignment Inputs
                                    html.Div(
                                        id="div-input-racket-consignment",
                                        children=[
                                            # Racket Name
                                            dmc.Select(
                                                id="select-racket-name", label="Nama Raket", size="xs", 
                                                withAsterisk=True, searchable=True,
                                            ),
                                            dmc.Text(id="text-racket-details", size="xs"),
                                            
                                            # Actual Weight
                                            dmc.TextInput(
                                                id="textinput-racket-weight", label="Berat Asli", size="xs", 
                                                placeholder="Masukkan berat asli raket dalam gram (g) dengan format ###G. Contoh: 132G",
                                            ),
                                        ],
                                    ),

                                    # Others Consignment Inputs
                                    html.Div(
                                        id="div-input-others-consignment",
                                        children=[
                                            # Item Name
                                            dmc.Select(
                                                id="select-item-name", label="Nama Barang", size="xs", 
                                                withAsterisk=True, searchable=True,
                                            ),
                                            
                                            # Shoe Size
                                            html.Div(
                                                dmc.TextInput(
                                                    id="textinput-shoe-size", label="Ukuran Sepatu", size="xs",
                                                    placeholder="Masukkan ukuran sepatu dengan sizing EUR. Contoh: EUR41 (Pastikan menambahkan awalan 'EUR')", 
                                                ),
                                                id="div-input-shoes-size",
                                            ),
                                            
                                            # Shirt Size
                                            html.Div(
                                                dmc.TextInput(
                                                    id="textinput-shirt-size", label="Ukuran Baju", size="xs", 
                                                    placeholder="Masukkan ukuran baju sesuai dengan barangnya. Contoh: Small",
                                                ),
                                                id="div-input-shirt-size",
                                            ),

                                            # Others Description
                                            html.Div(
                                                dmc.Textarea(
                                                    id="textinput-others-description", label="Deskripsi Lainnya", size="xs",
                                                    placeholder="Masukkan deskripsi tambahan terkait barang consignment ini",
                                                ),
                                                id="div-input-others-description",
                                            )
                                        ],
                                    ),
                                ]
                            )
                        ]
                    ),                    
                    dmc.AccordionItem(
                        value="accordionitem-new-consignment-owner-detail",
                        children=[
                            dmc.AccordionControl("Detail Owner", icon=DashIconify(icon="mingcute-user-3-line", )),
                            dmc.AccordionPanel(
                                [
                                    # Owner WhatsApp
                                    dmc.Autocomplete(
                                        id="textinput-owner-whatsapp", label="Owner WhatsApp", size="xs",
                                        placeholder="Masukkan nomor WhatsApp pemilik barang consignment",
                                        withAsterisk=True,
                                    ),

                                    # Input new owners
                                    html.Div(
                                        id="div-input-owners-new",
                                        children=[
                                            dmc.TextInput(
                                                id="textinput-owner-name", label="Nama Pemilik", size="xs", 
                                                placeholder="Masukkan nama pemilik barang consignment",
                                                withAsterisk=True
                                            ),
                                            dmc.Autocomplete(
                                                id="textinput-owner-location", label="Lokasi Pemilik", size="xs", 
                                                placeholder="Masukkan lokasi pemilik barang consignment",
                                                withAsterisk=True
                                            )
                                        ],
                                    ),
                                ],
                            ),
                        ]
                    ),
                    dmc.AccordionItem(
                        value="accordionitem-new-consignment-consignment-detail",
                        children=[
                            dmc.AccordionControl("Detail Consignment", icon=DashIconify(icon="material-symbols:sell-outline-sharp")),
                            dmc.AccordionPanel(
                                [
                                    dmc.Stack(
                                        [
                                            # Identifier Barang Lama / Baru 
                                            dmc.Switch(
                                                id="switch-old-racket", label="Barang Lama / Baru", size="xs",
                                                description="Aktifkan jika barang consignment ini bukan barang baru",
                                            ),

                                            # Rating
                                            html.Div(
                                                dmc.NumberInput(
                                                    id="numberinput-rating", label="Rating Barang", size="xs", 
                                                    withAsterisk=True, min=0, max=10, decimalScale=1, fixedDecimalScale=True,
                                                    value=10, suffix=" / 10.0",
                                                ),
                                                id="div-input-item-rating",
                                            ),

                                            # Price Modal
                                            dmc.NumberInput(
                                                id="numberinput-price-modal", label="Harga dari Owner (Rp.)", size="xs", thousandSeparator=",", prefix="Rp.",
                                                withAsterisk=True, allowNegative=False, value=10000
                                            ),

                                            # Price Posted
                                            dmc.NumberInput(
                                                id="numberinput-price-posted", label="Harga Jual (Rp.)", size="xs", thousandSeparator=",", prefix="Rp.",
                                                withAsterisk=True, allowNegative=False, value=10000
                                            ),

                                            # Extra Note
                                            dmc.Textarea(
                                                id="textarea-extranote", label="Extra Note", size="xs",
                                                description="Masukkan catatan tambahan terkait consignment ini",
                                            ),
                                        ],
                                        gap="xs"
                                    )
                                ]
                            ),
                        ],
                    )
                ],
                multiple=True,
                variant="separated",
                radius="md",
            ),

            # Button to submit
            dmc.Button(
                id="button-register-consignment", children="Tambahkan Consignment",
                fullWidth=True, color="#5B8710"
            ),
        ],
        gap="xs"
    ),
)
modal_posted=dmc.Modal(
    id="modal-mark-posted-consignment",
    size="sm",
    title=dmc.Title("Mark Consignment as Posted", order=3),
    children=dmc.Text("Fungsi ini akan segera hadir. Nantikan pembaruan selanjutnya!", fz="sm")
)

# Page Layout
# -----------
layout=dmc.AppShellMain(
    [
        dmc.Title("Consignments"),
        dmc.Text(subtitleTexts, size="sm", visibleFrom="sm", mb=20),
        dmc.Text(subtitleTexts, size="xs", hiddenFrom="sm", mb=20),
        dmc.LoadingOverlay(
            visible=False,
            id="loading-overlay-modal",
            overlayProps={"radius": "sm", "blur": 2},
            zIndex=210
        ),

        # Modals
        modal_register_new,
        
        # Desktop Filtering View
        dmc.Stack(
            [
                dmc.Accordion(
                    children=dmc.AccordionItem([
                        dmc.AccordionControl("Filter Data Consignment", icon=DashIconify(icon="mingcute-filter-line")),
                        dmc.AccordionPanel(
                            dmc.Group([selectItemType, selectItemStatus, buttonRegister, buttonRefresh], justify="space-evenly", gap="md", grow=True),
                        ),
                    ], value="filter-accordion-item"),
                    chevronPosition="right",
                    radius="md",
                    variant="separated",
                    value="filter-accordion-item"
                )
            ],
            visibleFrom="sm",
            mb=20,
        ),

        # Mobile Filtering View
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
            mb=20,
        ),

        consignment_table,
        dmc.Group(
            [
                dmc.Box([
                    dmc.Button(
                        id="button-mark-posted-consignment",
                        children=dmc.Text("Mark Consignment as Posted", size="sm"),
                        leftSection=DashIconify(icon="material-symbols:sell-outline-sharp"),
                        fullWidth=True,
                        color="third"
                    ),
                    dmc.Tooltip(
                        target="#button-mark-posted-consignment",
                        label="Memasukkan link IG dan menandai consignment sebagai 'Posted'",
                        position="top",
                        withArrow=True,
                        transitionProps={
                            "transition": "slide-up", 
                            "duration": 200,
                            "timingFunction": "ease"
                        },
                        color="third"
                    )
                ]),
                dmc.Box([
                    dmc.Button(
                        id="button-mark-sold-consignment",
                        children=dmc.Text("Mark Consignment as Sold", size="sm"),
                        leftSection=DashIconify(icon="material-symbols:sell-outline-sharp"),
                        fullWidth=True,
                        color="fourth"
                    ),
                    dmc.Tooltip(
                        target="#button-mark-sold-consignment",
                        label="Memasukkan link IG dan menandai consignment sebagai 'Sold'",
                        position="top",
                        withArrow=True,
                        transitionProps={
                            "transition": "slide-up", 
                            "duration": 200,
                            "timingFunction": "ease"
                        },
                        color="fourth"
                    )
                ]),
                dmc.Box([
                    dmc.Button(
                        id="button-mark-shipped-consignment",
                        children=dmc.Text("Mark Consignment as Shipped", size="sm"),
                        leftSection=DashIconify(icon="material-symbols:sell-outline-sharp"),
                        fullWidth=True,
                        color="fifth"
                    ),
                    dmc.Tooltip(
                        target="#button-mark-shipped-consignment",
                        label="Memasukkan link IG dan menandai consignment sebagai 'Shipped'",
                        position="top",
                        withArrow=True,
                        transitionProps={
                            "transition": "slide-up", 
                            "duration": 200,
                            "timingFunction": "ease"
                        },
                        color="fifth"
                    )
                ]),
                dmc.Box([
                    dmc.Button(
                        id="button-mark-complete-consignment",
                        children=dmc.Text("Mark Consignment as Completed", size="sm"),
                        leftSection=DashIconify(icon="material-symbols:sell-outline-sharp"),
                        fullWidth=True,
                        color="sixth"
                    ),
                    dmc.Tooltip(
                        target="#button-mark-complete-consignment",
                        label="Memasukkan link IG dan menandai consignment sebagai 'Complete' / 'Completed Elsewhere'",
                        position="top",
                        withArrow=True,
                        transitionProps={
                            "transition": "slide-up", 
                            "duration": 200,
                            "timingFunction": "ease"
                        },
                        color="sixth"
                    )
                ]),
            ],
            justify="space-evenly",
            mt=25,
            grow=True,
        )

    ]
)

# --------------------------------
# CALLBACKS
# Callback Register New Consignment
# ---------------------------------
@callback(
    Output("modal-register-consignment", "opened"),
    Input("button-add-consignment", "n_clicks"),
    prevent_initial_call=True,
)
def open_register_modal(_):
    return True

# Manipulate Item Detail Options
@callback(
    Output("div-input-racket-consignment", "hidden"),
    Output("div-input-others-consignment", "hidden"),
    Output("div-input-shirt-size", "hidden"),
    Output("div-input-shoes-size", "hidden"),
    Output("div-input-others-description", "hidden"),
    Input("select-new-consignment-type", "value"),
)
def adjust_consignment_input_div(selected_type):
    if selected_type == "Racket":
        return False, True, True, True, True
    elif selected_type == "Shirt":
        return True, False, False, True, True
    elif selected_type == "Shoes":
        return True, False, True, False, True
    elif selected_type == "Others":
        return True, False, True, True, False
    elif selected_type == "Bag":
        return True, False, True, True, True
    else:
        return True, True, True, True, True

@callback(
    Output("div-input-owners-new", "hidden"),
    Input("textinput-owner-whatsapp", "value"),
    State("textinput-owner-whatsapp", "data"),
)
def adjust_owner_input_div(value, data):
    if value is None or value == "": 
        return True
    else:
        return value in data

@callback(
    Output("div-input-item-rating", "hidden"),
    Input("switch-old-racket", "checked"),  
)
def adjust_item_rating_input_div(is_old):
    return not is_old

# --------------------------------
# End of File