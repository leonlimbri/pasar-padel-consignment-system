import dash_mantine_components as dmc
import dash_ag_grid as dag
from dash import register_page, callback, Output, Input, State, html, no_update
from dash_iconify import DashIconify
from utils import *

register_page(__name__, path="/")

# Components & Selectors & Buttons
# --------------------------------
subtitleTexts = "Tambah / Edit data consignmentmu disini. Untuk menambahkan data consignment, silahkan klik tombol 'Add Consignment' dibawah. Untuk mengedit data consignment, silahkan klik dua kali pada baris data consignment yang ingin diubah."

# Data Table
# ----------
# TODO: Add conditional format of the cell colour of the consignment table
value_formatter_currency = {"function": "`Rp. `+d3.format(',.0f')(params.value)"}
value_formatter_id = {"function": "`PP` + params.value"}
consignment_table_columns = [
    {"headerName": "Consignment ID", "field": "consignment_id", "type": "text", "valueFormatter": value_formatter_id},
    {"headerName": "Tipe Barang", "field": "item_type", "type": "text", "filter": False},
    {"headerName": "Nama Barang", "field": "item_name", "type": "text"},
    {"headerName": "Harga Modal", "field": "price_modal", "valueFormatter": value_formatter_currency},
    {"headerName": "Harga di Instagram", "field": "price_posted", "valueFormatter": value_formatter_currency},
    {"headerName": "WA Seller", "field": "seller_wa", "type": "text"},
    {"headerName": "Nama Seller", "field": "seller_name", "type": "text"},
    {"headerName": "Lokasi", "field": "seller_location", "type": "text"},
    {"headerName": "Kondisi Barang", "field": "item_condition", "type": "text"},
    {"headerName": "Status Barang", "field": "status", "type": "text", "filter": False},
]
consignment_table = dag.AgGrid(
    id="aggrid-consignment-table",
    className="ag-theme-quartz",
    columnDefs=consignment_table_columns,
    rowData=get_complete_consignments(),
    defaultColDef={
        "sortable": True,
        "filter": True,
        "resizable": True,
        "minWidth": 150,
    },
    dashGridOptions={
        "pagination": True, 
        "paginationPageSize": 250, 
        "paginationPageSizeSelector": False,
        "rowBuffer": 0,
        "rowSelection": {
            "mode": "multiRow",
            "enableClickSelection": True
        },
        "suppressColumnVirtualisation": True,
    },
    style={"height": "500px", "width": "100%", "--ag-font-size": "0.8rem"},
    persistence=True,
    persisted_props=["filterModel", "columnState"],
    dangerously_allow_code=True,
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
                                        data=consignment_type_options, value="",
                                        withAsterisk=True,
                                    ),

                                    # Brand
                                    dmc.Autocomplete(
                                        id="autocomplete-item-brand", label="Brand Barang", size="xs", 
                                        placeholder="Masukkan nama brand barang.", withAsterisk=True, selectFirstOptionOnChange=True,
                                        limit=15, debounce=True, value=""
                                    ),

                                    # Name
                                    dmc.Autocomplete(
                                        id="autocomplete-item-name", label="Nama Barang", size="xs", 
                                        placeholder="Masukkan nama barang.", withAsterisk=True, selectFirstOptionOnChange=True,
                                        limit=15, debounce=True, value=""
                                    ),
                                    
                                    dmc.Divider(label="Detail Barang", labelPosition="center"),

                                    # Racket Consignment Inputs
                                    html.Div(
                                        id="div-input-racket-consignment",
                                        children=[
                                            # Is Women Racket
                                            dmc.Switch(
                                                id="switch-racket-women", label="Woman's Racket", size="xs", checked=False,
                                                description="Toggle untuk menandakan bahwa raket adalah raket wanita",
                                                onLabel=DashIconify(icon="material-symbols-light-female", width=15,color="gray"),
                                                mt=1
                                            ),

                                            # Shape
                                            dmc.Autocomplete(
                                                id="autocomplete-racket-shape", label="Shape Racket", size="xs", 
                                                withAsterisk=True,  selectFirstOptionOnChange=True, debounce=True
                                            ),
                                            
                                            # Face Material
                                            dmc.Autocomplete(
                                                id="autocomplete-racket-facematerial", label="Surface Material", size="xs", 
                                                placeholder="Masukkan surface material", withAsterisk=True, selectFirstOptionOnChange=True,
                                                limit=15, debounce=True
                                            ),

                                            # Core Material
                                            dmc.Autocomplete(
                                                id="autocomplete-racket-corematerial", label="Core Material", size="xs", 
                                                placeholder="Masukkan core material", withAsterisk=True, selectFirstOptionOnChange=True,
                                                limit=15, debounce=True
                                            ),

                                            # Additional Specifications
                                            dmc.TagsInput(
                                                id="tagsinput-racket-additionalspec", label="Additional Specification", size="xs",
                                                data=["Attack","Balance","Comfort","Control","Large Sweet Spot","Light","Powerful","Precision","Top Heavy"]
                                            ),
                                            
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
                                        id="autocomplete-owner-whatsapp", label="Owner WhatsApp", size="xs",
                                        placeholder="Masukkan nomor WhatsApp pemilik barang consignment", selectFirstOptionOnChange=True,
                                        limit=15, debounce=True, withAsterisk=True,
                                    ),

                                    # Owner Name
                                    dmc.TextInput(
                                        id="textinput-owner-name", label="Nama Pemilik", size="xs", 
                                        placeholder="Masukkan nama pemilik barang consignment",
                                        withAsterisk=True
                                    ),

                                    # Owner Location
                                    dmc.Autocomplete(
                                        id="autocomplete-owner-location", label="Lokasi Pemilik", size="xs", 
                                        placeholder="Masukkan lokasi pemilik barang consignment",
                                        withAsterisk=True
                                    )
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
        dmc.LoadingOverlay(id="loading-overlay-register-consignment", visible=False, overlayProps={"radius": "sm", "blur": 2}, zIndex=10),

        # Modals
        modal_register_new,
        
        # Desktop Filtering View
        dmc.Stack(
            [
                dmc.Accordion(
                    children=dmc.AccordionItem([
                        dmc.AccordionControl("Filter Data Consignment", icon=DashIconify(icon="mingcute-filter-line"),),
                        dmc.AccordionPanel(
                            dmc.Group([
                                generate_multi_select("multiselect-filter-item-type-desktop", "Tipe Barang", "Pilih tipe consigment untuk mengfilter data consignment", consignment_type_options), 
                                generate_multi_select("multiselect-filter-item-status-desktop", "Status Barang", "Pilih status consignment untuk memfilter data consignment", status_type_options), 
                                generate_button("button-add-consignment", "Tambah Consignment Baru", "Klik untuk menambahkan data consignment baru", "first", "gg:add"), 
                                generate_button("button-refresh-consignment", "Refresh Tabel Consignment", "Klik untuk meng-refresh data pada tabel consignment", "gray", "material-symbols:refresh")
                            ], justify="space-evenly", gap="md", grow=True),
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
                generate_button("button-add-consignment", "Tambah Consignment Baru", "Klik untuk menambahkan data consignment baru", "first", "gg:add"),
                dmc.Accordion(
                    children=dmc.AccordionItem([
                        dmc.AccordionControl("Filter Data Consignment", icon=DashIconify(icon="mingcute-filter-line")),
                        dmc.AccordionPanel(
                            dmc.Stack([
                                generate_multi_select("multiselect-filter-item-type-mobile", "Tipe Barang", "Pilih tipe consigment untuk mengfilter data consignment", consignment_type_options), 
                                generate_multi_select("multiselect-filter-item-status-mobile", "Status Barang", "Pilih status consignment untuk memfilter data consignment", status_type_options), 
                                generate_button("button-refresh-consignment", "Refresh Tabel Consignment", "Klik untuk meng-refresh data pada tabel consignment", "gray", "material-symbols:refresh")
                            ]),
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

        # Desktop Marking Buttons
        dmc.Group(
            [
                generate_button("button-mark-posted-consignment", "Mark as Posted", "Memasukkan link IG dan menandai consignment sebagai 'Posted'", "gray", "mdi-instagram"),
                generate_button("button-mark-sold-consignment", "Mark as Sold", "Menandai consignment sebagai 'Sold'", "fourth", "material-symbols:sell-outline-sharp"),
                generate_button("button-mark-shipped-consignment", "Mark as Shipped", "Memasukkan Tracking Code Menandai consignment sebagai 'Shipped'", "fifth", "gridicons-shipping"),
                generate_button("button-mark-complete-consignment", "Mark as Completed", "Menandai consignment sebagai 'Completed' / 'Completed Elsewhere", "first", "mdi-done-all"),
            ],
            justify="space-evenly",
            mt=25,
            grow=True,
            visibleFrom="sm"
        ),

        # Mobile Marking Buttons
        dmc.Group(
            [
                dmc.Stack(
                    [
                        generate_button("button-mark-posted-consignment", "Mark as Posted", "Memasukkan link IG dan menandai consignment sebagai 'Posted'", "gray", "mdi-instagram"),
                        generate_button("button-mark-sold-consignment", "Mark as Sold", "Menandai consignment sebagai 'Sold'", "fourth", "material-symbols:sell-outline-sharp"),        
                    ]
                ),
                dmc.Stack(
                    [
                        generate_button("button-mark-shipped-consignment", "Mark as Shipped", "Memasukkan Tracking Code Menandai consignment sebagai 'Shipped'", "fifth", "gridicons-shipping"),
                        generate_button("button-mark-complete-consignment", "Mark as Completed", "Menandai consignment sebagai 'Completed' / 'Completed Elsewhere", "first", "mdi-done-all"),
                    ]
                )
            ],
            justify="space-evenly",
            mt=25,
            grow=True,
            hiddenFrom="sm"
        )



    ]
)

# --------------------------------
# CALLBACKS
# --------------------------------

# Callback for dark theme toggle
# ------------------------------
@callback(
    Output("aggrid-consignment-table", "className"),
    Input("switch-color-scheme", "checked"),
    supress_callback_exceptions=True
)
def toggle_color_scheme(switch_on):
    return "ag-theme-quartz-dark" if switch_on else "ag-theme-quartz"

# Callback Refresh Consignment Table
# ---------------------------------
@callback(
    Output("aggrid-consignment-table", "rowData"),
    Input("button-refresh-consignment", "n_clicks"),
    State("multiselect-filter-item-type-desktop", "value"),
    State("multiselect-filter-item-status-desktop", "value"),
    State("multiselect-filter-item-type-mobile", "value"),
    State("multiselect-filter-item-status-mobile", "value"),
    running=[Output("loading-overlay-register-consignment", "visible"), True, False],
)
def refresh_consignment_table(_, types_d, status_d, types_m, status_m):
    types = types_d if types_d else types_m
    status = status_d if status_d else status_m
    
    # Fetch data from database
    consignment_data = get_complete_consignments(types, status)
    return consignment_data

# Callback Register New Consignment
# ---------------------------------
@callback(
    Output("modal-register-consignment", "opened"),
    Output("autocomplete-racket-shape", "data"),
    Output("autocomplete-racket-facematerial", "data"),
    Output("autocomplete-racket-corematerial", "data"),
    Output("autocomplete-owner-whatsapp", "data"),
    Output("autocomplete-owner-location", "data"),
    Input("button-add-consignment", "n_clicks"),
    prevent_initial_call=True,
    running=[Output("loading-overlay-register-consignment", "visible"), True, False],
)
def open_register_modal(_):
    shape_opts = [d.get("shape_name") for d in get_complete_shapes()]
    face_opts, core_opts = [], []
    for d in get_complete_materials():
        if d.get("material_type") == "FACE": face_opts += [d.get("material_name")]
        else: core_opts += [d.get("material_name")]
    contact_was = [d.get("contact_wa") for d in get_complete_contacts()]
    contact_locs = [d.get("contact_location") for d in get_distinct_contact_location()]
    return True, shape_opts, face_opts, core_opts, contact_was, contact_locs

# Manipulate Item Detail Options
@callback(
    Output("div-input-racket-consignment", "hidden"),
    Output("div-input-others-consignment", "hidden"),
    Output("div-input-shirt-size", "hidden"),
    Output("div-input-shoes-size", "hidden"),
    Output("div-input-others-description", "hidden"),
    Input("select-new-consignment-type", "value"),
    Input("autocomplete-item-brand", "value"),
    Input("autocomplete-item-name", "value"),
)
def adjust_consignment_input_div(selected_type, selected_brand, selected_item):
    if selected_brand != "" and selected_item != "":
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

@callback(
    Output("autocomplete-item-brand", "data"),
    Input("select-new-consignment-type", "value"),
    running=[Output("autocomplete-item-brand", "disabled"), True, False],
)
def get_brand_options(item_type):
        return [d.get("brand_name") for d in get_complete_brands()]
        
@callback(
    Output("autocomplete-item-name", "data"),
    Input("select-new-consignment-type", "value"),
    Input("autocomplete-item-brand", "value"),
    running=[Output("autocomplete-item-name", "disabled"), True, False],
)
def get_item_options(item_type, brand_name):
    if item_type == "" or brand_name == "": return no_update
    return [
        d.get("item_name")
        for d in get_complete_items(item_type, brand_name)
    ]

@callback(
    Output("switch-racket-women", "checked"),
    Output("autocomplete-racket-shape", "value"),
    Output("autocomplete-racket-facematerial", "value"),
    Output("autocomplete-racket-corematerial", "value"),
    Output("tagsinput-racket-additionalspec", "value"),
    Output("textinput-racket-weight", "value"),
    State("autocomplete-item-brand", "value"),
    Input("autocomplete-item-name", "value"),
    State("autocomplete-item-name", "data"),
    State("select-new-consignment-type", "value"),
    running=[
        (Output("switch-racket-women", "disabled"), True, False),
        (Output("autocomplete-racket-shape", "disabled"), True, False),
        (Output("autocomplete-racket-facematerial", "disabled"), True, False),
        (Output("autocomplete-racket-corematerial", "disabled"), True, False),
        (Output("tagsinput-racket-additionalspec", "disabled"), True, False),
        (Output("textinput-racket-weight", "disabled"), True, False),
    ],
)
def get_racket_information(brand_name, item_name, item_opts, item_type):
    if item_type != "Racket" or item_name not in item_opts: 
        return no_update
    data = get_complete_items(item_type, brand_name, item_name)[0]
    return \
        data.get("is_racket_woman"), \
        data.get("shape_name"), \
        data.get("face_material"), \
        data.get("core_material"), \
        data.get("racket_additional_spec"), \
        data.get("racket_weight")

@callback(
    Output("textinput-owner-name", "value"),
    Output("autocomplete-owner-location", "value"),
    Input("autocomplete-owner-whatsapp", "value"),
    Input("autocomplete-owner-whatsapp", "data"),
    prevent_initial_call=True,
    running=[
        (Output("textinput-owner-name", "disabled"), True, False),
        (Output("autocomplete-owner-location", "disabled"), True, False),
    ]
)
def get_owner_details(owner_wa, owner_wa_opts):
    if owner_wa not in owner_wa_opts:
        return no_update
    else:
        data = get_complete_contacts(owner_wa)[0]
        return data.get("contact_name"), data.get("contact_location")

# TODO: Add disabled/enable button for add consignment
# TODO: Button to change status of the item to POSTED
# TODO: Button to change status of the item to SOLD
# TODO: Button to change status of the item to SHIPPED
# TODO: Button to change status of the item to COMPLETED

# --------------------------------
# End of File