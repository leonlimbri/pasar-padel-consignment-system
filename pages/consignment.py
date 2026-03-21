import dash_mantine_components as dmc
import dash_ag_grid as dag
import ast
from dash import register_page, callback, Output, Input, State, html, no_update, dcc
from dash_iconify import DashIconify
from utils import *
from datetime import datetime

register_page(__name__, path="/")

# Components & Selectors & Buttons
# --------------------------------
subtitleTexts = "Tambah / Edit data consignmentmu disini. Untuk menambahkan data consignment, silahkan klik tombol 'Add Consignment' dibawah. Untuk mengedit data consignment, silahkan klik dua kali pada baris data consignment yang ingin diubah."

# Data Table
# ----------
# TODO: Add conditional format of the cell colour of the consignment table
tuplejoiner = "','"
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
getRowStyle = {
    "styleConditions": [
        {
            "condition": "params.data.status == 'New'",
            "style": {"backgroundColor": "#F6FFA3AA", "color": "black"}
        },
        {
            "condition": "params.data.status == 'Posted'",
            "style": {"backgroundColor": "#FFFFFFCC", "color": "black"}
        },
        {
            "condition": "params.data.status == 'Sold'",
            "style": {"backgroundColor": "#A9C1FF99", "color": "black"}
        },
        {
            "condition": "params.data.status == 'Shipped'",
            "style": {"backgroundColor": "#AEE5CC99", "color": "black"}
        },
        {
            "condition": "params.data.status == 'Completed Elsewhere'",
            "style": {"backgroundColor": "#D3D3D366", "color": "black"}
        },
        {
            "condition": "params.data.status == 'Completed'",
            "style": {"backgroundColor": "#B8F2D999", "color": "black"}
        }
    ],
    "defaultStyle": {"backgroundColor": "grey", "color": "white"}
}
consignment_table = dag.AgGrid(
    id="aggrid-consignment-table",
    className="ag-theme-quartz",
    columnDefs=consignment_table_columns,
    rowData=run_query_from_sql("get_all_consignments.sql", sel_types=f"('{tuplejoiner.join(consignment_type_options)}')", sel_status=f"('{tuplejoiner.join(status_type_options)}')"),
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
    getRowStyle=getRowStyle,
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
                                        limit=15, debounce=300, value=""
                                    ),

                                    # Name
                                    dmc.Autocomplete(
                                        id="autocomplete-item-name", label="Nama Barang", size="xs", 
                                        placeholder="Masukkan nama barang.", withAsterisk=True, selectFirstOptionOnChange=True,
                                        limit=15, debounce=300, value=""
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
                                                withAsterisk=True,  selectFirstOptionOnChange=True, debounce=300
                                            ),
                                            
                                            # Face Material
                                            dmc.Autocomplete(
                                                id="autocomplete-racket-facematerial", label="Surface Material", size="xs", 
                                                placeholder="Masukkan surface material", withAsterisk=True, selectFirstOptionOnChange=True,
                                                limit=15, debounce=300
                                            ),

                                            # Core Material
                                            dmc.Autocomplete(
                                                id="autocomplete-racket-corematerial", label="Core Material", size="xs", 
                                                placeholder="Masukkan core material", withAsterisk=True, selectFirstOptionOnChange=True,
                                                limit=15, debounce=300
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
                                                    id="textarea-others-description", label="Deskripsi Barang", size="xs",
                                                    placeholder="Masukkan deskripsi barang consignment ini",
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
                                        limit=15, debounce=300, withAsterisk=True,
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
    size="md",
    title=dmc.Title("Update Consignment 'Posted'", order=3),
    children=[
        dmc.TextInput(id="textinput-ig-link-posted-consignment", label="Link Instagram", placeholder="Masukkan link Instagram tempat consignment diposting", size="xs", withAsterisk=True),
        dmc.Space(h="md"),
        generate_button("button-confirm-mark-posted-consignment", "Submit", "Klik untuk mengkonfirmasi perubahan status consignment menjadi 'Posted'", "gray", "mdi-instagram"),
    ]
)
modal_sold=dmc.Modal(
    id="modal-mark-sold-consignment",
    size="md",
    title=dmc.Title("Update Consignment 'Sold'", order=3),
    children=[
        dmc.Text(id="text-consignment-to-sold", size="xs", mb=10),
        dmc.Switch(id="switch-consignment-sold-in-pasarpadel", label="Terjual di Pasar Padel", description="Centang untuk mengkonfirmasi bahwa consignment telah terjual di Pasar Padel", size="xs", checked=True, mt=0, mb=10),
        html.Div(
            id="div-input-mark-sold-consignment",
            children=[

                # Nama Sales
                dmc.Autocomplete(
                    id="autocomplete-sales-name-mark-sold-consignment", label="Nama Sales", size="xs",
                    placeholder="Masukkan nama sales yang menangani penjualan consignment", selectFirstOptionOnChange=True,
                    limit=15, debounce=300, withAsterisk=True,
                ),

                # Buyer WhatsApp
                dmc.Autocomplete(
                    id="autocomplete-buyer-whatsapp", label="Buyer WhatsApp", size="xs",
                    placeholder="Masukkan nomor WhatsApp pembeli barang consignment", selectFirstOptionOnChange=True,
                    limit=15, debounce=300, withAsterisk=True,
                ),

                # Buyer Name
                dmc.TextInput(
                    id="textinput-buyer-name", label="Nama Pembeli", size="xs", 
                    placeholder="Masukkan nama pembeli barang consignment",
                    withAsterisk=True
                ),

                # Buyer Location
                dmc.Autocomplete(
                    id="autocomplete-buyer-location", label="Lokasi Pembeli", size="xs", 
                    placeholder="Masukkan lokasi pembeli barang consignment",
                    withAsterisk=True
                ),

                # Harga Terjual
                dmc.NumberInput(
                    id="numberinput-price-sold", label="Harga Terjual (Rp.)", size="xs", thousandSeparator=",", prefix="Rp.",
                    withAsterisk=True, allowNegative=False, value=10000
                ),
            ]
        ),
        dmc.Space(h="md"),
        generate_button("button-confirm-mark-sold-consignment", "Submit", "Klik untuk mengkonfirmasi perubahan status consignment menjadi 'Sold'", "fourth", "material-symbols:sell-outline-sharp"),
    ]
)
modal_shipped=dmc.Modal(
    id="modal-mark-shipped-consignment",
    size="md",
    title=dmc.Title("Update Consignment 'Shipped'", order=3),
    children=[
        dmc.TextInput(id="textinput-tracking-shipped-consignment", label="Tracking Code", placeholder="Masukkan nomor tracking consignment", size="xs", withAsterisk=True),
        dmc.Space(h="md"),
        generate_button("button-confirm-mark-shipped-consignment", "Submit", "Klik untuk mengkonfirmasi perubahan status consignment menjadi 'Shipped'", "fifth", "gridicons-shipping"),
    ]
)
modal_completed=dmc.Modal(
    id="modal-mark-completed-consignment",
    size="md",
    title=dmc.Title("Update Consignment 'Completed'", order=3),
    children=[
        dmc.Text("Apakah Anda yakin ingin menandai consignment ini sebagai 'Completed'? Pastikan bahwa barang sudah diterima pembeli dan tidak ada masalah terkait transaksi consignment ini sebelum mengkonfirmasi perubahan status menjadi 'Completed'.", size="xs"),
        dmc.Space(h="md"),
        generate_button("button-confirm-mark-completed-consignment", "Submit", "Klik untuk mengkonfirmasi perubahan status consignment menjadi 'Completed'", "fifth", "gridicons-shipping"),
    ]
)
modal_change_price=dmc.Modal(
    id="modal-edit-price-consignment",
    size="md",
    title=dmc.Title("Edit Harga Consignment", order=3),
    children=[
        dmc.Text("Gunakan form dibawah ini untuk mengubah harga consignment. Pastikan untuk memasukkan harga yang valid dan sesuai dengan kondisi consignment saat ini. REFRESH DATA SETELAH PERUBAHAN.", size="xs", mb=10),
        # Ubah Harga Buyer / Jual (jika belom di jual)
        dmc.NumberInput(
            id="numberinput-price-modal-changes",
            label="Ubah Harga dari Owner (Rp.)",
            size="xs", thousandSeparator=",", prefix="Rp.",
            allowNegative=False,
        ),
        dmc.NumberInput(
            id="numberinput-price-posted-changes",
            label="Ubah Harga yang di post di IG (Rp.)",
            size="xs", thousandSeparator=",", prefix="Rp.",
            allowNegative=False,
        ),
        dmc.Space(h="md"),
        generate_button("button-confirm-edit-price-consignment", "Submit", "Klik untuk mengkonfirmasi perubahan harga consignment", "first", "fa7-regular--edit"),
    ]
)
modal_details=dmc.Modal(
    id="modal-consignment-details",
    size="lg",
    title=dmc.Title("Detail Consignment", order=3),
    children=dmc.Stack(
        [
            dmc.Text("Detail informasi terkait consignment yang dipilih akan ditampilkan pada modal ini. Gunakan informasi ini untuk memverifikasi data consignment atau untuk keperluan lainnya.", fz="xs"),
            dmc.Divider(),

            # Detail information will be displayed here
            html.Div(id="div-consignment-detail-information"),
        ],
        gap="xs"
    ),
)

# Page Layout
# -----------
layout=dmc.AppShellMain(
    [
        dmc.Title("Consignments"),
        dmc.Text(subtitleTexts, size="sm", visibleFrom="sm", mb=20),
        dmc.Text(subtitleTexts, size="xs", hiddenFrom="sm", mb=20),
        dmc.LoadingOverlay(id="loading-overlay-register-consignment", visible=False, overlayProps={"radius": "sm", "blur": 2}, zIndex=10),
        dmc.NotificationContainer(id="consignment-notification"),

        # Signals
        dcc.Store(id="signal-to-refresh-consignment-table", storage_type="memory"),

        # Modals
        modal_register_new,
        modal_posted,
        modal_sold,
        modal_shipped,
        modal_completed,
        modal_details,
        modal_change_price,

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
                                generate_button("button-add-consignment-desktop", "Tambah Consignment Baru", "Klik untuk menambahkan data consignment baru", "first", "gg:add"), 
                                generate_button("button-refresh-consignment-desktop", "Refresh Tabel Consignment", "Klik untuk meng-refresh data pada tabel consignment", "gray", "material-symbols:refresh")
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
                generate_button("button-add-consignment-mobile", "Tambah Consignment Baru", "Klik untuk menambahkan data consignment baru", "first", "gg:add"),
                dmc.Accordion(
                    children=dmc.AccordionItem([
                        dmc.AccordionControl("Filter Data Consignment", icon=DashIconify(icon="mingcute-filter-line")),
                        dmc.AccordionPanel(
                            dmc.Stack([
                                generate_multi_select("multiselect-filter-item-type-mobile", "Tipe Barang", "Pilih tipe consigment untuk mengfilter data consignment", consignment_type_options), 
                                generate_multi_select("multiselect-filter-item-status-mobile", "Status Barang", "Pilih status consignment untuk memfilter data consignment", status_type_options), 
                                generate_button("button-refresh-consignment-mobile", "Refresh Tabel Consignment", "Klik untuk meng-refresh data pada tabel consignment", "gray", "material-symbols:refresh")
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
                generate_button("button-mark-posted-consignment-desktop", "Mark as Posted", "Memasukkan link IG dan menandai consignment sebagai 'Posted'", "gray", "mdi-instagram"),
                generate_button("button-mark-sold-consignment-desktop", "Mark as Sold", "Menandai consignment sebagai 'Sold'", "fourth", "material-symbols:sell-outline-sharp"),
                generate_button("button-mark-shipped-consignment-desktop", "Mark as Shipped", "Memasukkan Tracking Code Menandai consignment sebagai 'Shipped'", "fifth", "gridicons-shipping"),
                generate_button("button-mark-completed-consignment-desktop", "Mark as Completed", "Menandai consignment sebagai 'Completed'", "first", "mdi-done-all"),
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
                        generate_button("button-mark-posted-consignment-mobile", "Mark as Posted", "Memasukkan link IG dan menandai consignment sebagai 'Posted'", "gray", "mdi-instagram"),
                        generate_button("button-mark-sold-consignment-mobile", "Mark as Sold", "Menandai consignment sebagai 'Sold'", "fourth", "material-symbols:sell-outline-sharp"),        
                    ]
                ),
                dmc.Stack(
                    [
                        generate_button("button-mark-shipped-consignment-mobile", "Mark as Shipped", "Memasukkan Tracking Code Menandai consignment sebagai 'Shipped'", "fifth", "gridicons-shipping"),
                        generate_button("button-mark-completed-consignment-mobile", "Mark as Completed", "Menandai consignment sebagai 'Completed'", "first", "mdi-done-all"),
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
    Input("button-refresh-consignment-desktop", "n_clicks"),
    Input("button-refresh-consignment-mobile", "n_clicks"),
    Input("signal-to-refresh-consignment-table", "data"),
    State("multiselect-filter-item-type-desktop", "value"),
    State("multiselect-filter-item-status-desktop", "value"),
    State("multiselect-filter-item-type-mobile", "value"),
    State("multiselect-filter-item-status-mobile", "value"),
    running=[Output("loading-overlay-register-consignment", "visible"), True, False],
)
def refresh_consignment_table(n_click_refresh_desktop, n_click_refresh_mobile, signal_to_refresh, types_d, status_d, types_m, status_m):
    # Check if use desktop or not
    if not any(v is not None for v in [n_click_refresh_desktop, n_click_refresh_mobile, signal_to_refresh]):
        return no_update
    else:
        types = types_d if types_d else types_m
        status = status_d if status_d else status_m

        # Check if it selects all or not
        types = types if types else consignment_type_options
        status = status if status else status_type_options
        
        # Fetch data from database
        consignment_data = run_query_from_sql(
            "get_all_consignments.sql", 
            sel_types=f"('{tuplejoiner.join(types)}')",
            sel_status=f"('{tuplejoiner.join(status)}')",
        )
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
    Input("button-add-consignment-desktop", "n_clicks"),
    Input("button-add-consignment-mobile", "n_clicks"),
    prevent_initial_call=True,
    running=[Output("loading-overlay-register-consignment", "visible"), True, False],
)
def open_register_modal(n_click_desktop, n_click_mobile):
    if any(v is not None for v in [n_click_desktop, n_click_mobile]):
        shape_opts = [d.get("shape_name") for d in run_query_from_sql("get_all_shapes.sql")]
        face_opts = [d.get("contact_wa") for d in run_query_from_sql("get_specific_materials.sql", material_type="FACE")]
        core_opts = [d.get("contact_wa") for d in run_query_from_sql("get_specific_materials.sql", material_type="CORE")]
        contact_was = [d.get("contact_wa") for d in run_query_from_sql("get_all_contacts.sql")]
        contact_locs = [d.get("contact_location") for d in run_query_from_sql("get_distinct_locations.sql")]
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
def get_brand_options(_):
        return [d.get("brand_name") for d in run_query_from_sql("get_all_brands.sql")]
        
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
        for d in run_query_from_sql("get_all_items.sql", item_type=item_type, brand_name=brand_name)
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
    data = run_query_from_sql("get_specific_item.sql", item_type=item_type, brand_name=brand_name, item_name=item_name)[0]
    return \
        data.get("is_racket_woman"), \
        data.get("shape_name"), \
        data.get("face_material"), \
        data.get("core_material"), \
        ast.literal_eval(data.get("racket_additional_spec")) if data.get("racket_additional_spec") else [], \
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
        data = run_query_from_sql("get_specific_contact.sql", contact_wa=owner_wa)[0]
        return data.get("contact_name"), data.get("contact_location")

# Add disabled/enable button for add consignment
@callback(
    Output("button-register-consignment", "disabled"),
    Input("select-new-consignment-type", "value"),
    Input("autocomplete-item-brand", "value"),
    Input("autocomplete-item-name", "value"),
    Input("autocomplete-racket-shape", "value"),
    Input("autocomplete-racket-facematerial", "value"),
    Input("autocomplete-racket-corematerial", "value"),
    Input("textinput-racket-weight", "value"),
    Input("textinput-shoe-size", "value"),
    Input("textinput-shirt-size", "value"),
    Input("textarea-others-description", "value"),
    Input("autocomplete-owner-whatsapp", "value"),
    Input("textinput-owner-name", "value"),
    Input("autocomplete-owner-location", "value"),
    Input("numberinput-rating", "value"),
    Input("numberinput-price-modal", "value"),
    Input("numberinput-price-posted", "value"),
)
def check_inputs(consignment_type, brand, name, rackets_shape, rackets_face, rackets_core, rackets_weight, shoe_inp, shirt_inp, others_inp, *args):
    if consignment_type == "Racket":
        return check_any_input_is_empty([brand, name, rackets_shape, rackets_face, rackets_core, rackets_weight, list(args)])
    elif consignment_type == "Shirt":
        return check_any_input_is_empty([brand, name, rackets_shape, rackets_face, rackets_core, shirt_inp, list(args)]) 
    elif consignment_type == "Shoe":
        return check_any_input_is_empty([brand, name, rackets_shape, rackets_face, rackets_core, shoe_inp, list(args)]) 
    elif consignment_type in ("Others", "Bag"):
        return check_any_input_is_empty([brand, name, rackets_shape, rackets_face, rackets_core, others_inp, list(args)]) 
    return True

# DONE: Button to add new consignment
@callback(
    Output("modal-register-consignment", "opened", allow_duplicate=True),
    Output("consignment-notification", "sendNotifications", allow_duplicate=True),
    Output("signal-to-refresh-consignment-table", "data", allow_duplicate=True),
    Input("button-register-consignment", "n_clicks"),
    State("select-new-consignment-type", "value"),
    State("autocomplete-item-brand", "data"),
    State("autocomplete-item-brand", "value"),
    State("autocomplete-item-name", "data"),
    State("autocomplete-item-name", "value"),
    State("switch-racket-women", "checked"),
    State("autocomplete-racket-shape", "data"),
    State("autocomplete-racket-shape", "value"),
    State("autocomplete-racket-facematerial", "data"),
    State("autocomplete-racket-facematerial", "value"),
    State("autocomplete-racket-corematerial", "data"),
    State("autocomplete-racket-corematerial", "value"),
    State("textinput-racket-weight", "value"),
    State("tagsinput-racket-additionalspec", "value"),
    State("textinput-shoe-size", "value"),
    State("textinput-shirt-size", "value"),
    State("textarea-others-description", "value"),
    State("autocomplete-owner-whatsapp", "data"),
    State("autocomplete-owner-whatsapp", "value"),
    State("autocomplete-owner-location", "value"),
    State("textinput-owner-name", "value"),
    State("numberinput-rating", "value"),
    State("numberinput-price-modal", "value"),
    State("numberinput-price-posted", "value"),
    State("textarea-extranote", "value"),
    State("switch-old-racket", "checked"),
    prevent_initial_call=True
)
def add_new_consignment(
    n_click, consignment_type, brand_data, brand, item_data, name, is_racket_w,
    rackets_shape_data, rackets_shape, rackets_face_data, rackets_face, rackets_core_data, rackets_core, rackets_weight, rackets_additional_spec, shoe_inp, shirt_inp, others_inp, 
    owner_wa_data, owner_wa, owner_location, owner_name, item_rating, price_modal, price_posted, extranote, is_old):
    if n_click:
        
        # Check if brands exists
        if brand not in brand_data:
            # Add brand to BRAND table
            run_query_from_sql("insert_new_brand.sql", brand_name=brand)

        # Check if item exists
        rackets_additional_spec = str(rackets_additional_spec).replace("'", '"')
        if consignment_type == "Racket":
            if name not in item_data:
                if rackets_shape not in rackets_shape_data:
                    # Add Racket Shape
                    run_query_from_sql("insert_new_racket_shape.sql", shape_name=rackets_shape)
                if rackets_face not in rackets_face_data:
                    # Add Racket Face
                    run_query_from_sql("insert_new_racket_material.sql", material_type="FACE", material_name=rackets_face)
                if rackets_core not in rackets_core_data:
                    # Add Racket Core
                    run_query_from_sql("insert_new_racket_material.sql", material_type="CORE", material_name=rackets_core)
                
                run_query_from_sql(
                    "insert_new_racket.sql", 
                    item_type=consignment_type, brand_name=brand, item_name=name, 
                    is_racket_woman=1 if is_racket_w else 0, racket_shape=rackets_shape, racket_face_material=rackets_face, 
                    racket_core_material=rackets_core, racket_weight=rackets_weight, racket_additional_spec=rackets_additional_spec
                )
            else:
                run_query_from_sql(
                    "update_racket.sql", 
                    item_type=consignment_type, brand_name=brand, item_name=name, 
                    is_racket_woman=1 if is_racket_w else 0, racket_shape=rackets_shape, racket_face_material=rackets_face, 
                    racket_core_material=rackets_core, racket_weight=rackets_weight, racket_additional_spec=rackets_additional_spec
                )
        elif name not in item_data:
            run_query_from_sql("insert_new_item.sql", item_type=consignment_type, brand_name=brand, item_name=name,)

        # Check if the owner contact exists
        if owner_wa not in owner_wa_data:
            # Add contact to CONTACTS table
            run_query_from_sql(
                "insert_new_contact.sql", 
                contact_name=owner_name, 
                contact_wa=owner_wa, 
                contact_location=owner_location
            )
        else:
            run_query_from_sql(
                "update_contact.sql", 
                contact_name=owner_name, 
                contact_wa=owner_wa, 
                contact_location=owner_location
            )

        # Add consignment data to CONSIGNMENTS table
        rackets_weight = f"'{rackets_weight}'" if rackets_weight else "null"
        extranote = f"'{extranote}'" if extranote else "null"
        item_rating = item_rating if is_old else 10
        if consignment_type == "Racket":
            extra_description = "null"
        elif consignment_type == "Shirt":
            extra_description = f"'{shirt_inp}'" if shirt_inp else "null"
        elif consignment_type == "Shoes":
            extra_description = f"'{shoe_inp}'" if shoe_inp else "null"
        elif consignment_type in ("Others", "Bag"):
            extra_description = f"'{others_inp}'" if others_inp else "null"
        
        run_query_from_sql(
            "insert_new_consignment.sql",
            item_type=consignment_type, item_name=name, seller_wa=owner_wa, 
            item_rating=item_rating, price_modal=price_modal, price_posted=price_posted, extra_note=extranote,
            racket_weight=rackets_weight, extra_description=extra_description, item_condition="Used" if is_old else "New",
        )

        return False, [
            dict(
                title="Consignment berhasil ditambahkan",
                id="show-notify",
                action="show",
                message="Data Consignment telah berhasil ditambah, mohon refresh data.",
                icon=DashIconify(icon="fluent-mdl2:completed-solid"),
            )
        ], str(datetime.now())

@callback(
    Output("button-mark-posted-consignment-mobile", "disabled"),
    Output("button-mark-sold-consignment-mobile", "disabled"),
    Output("button-mark-shipped-consignment-mobile", "disabled"),
    Output("button-mark-completed-consignment-mobile", "disabled"),
    Output("button-mark-posted-consignment-desktop", "disabled"),
    Output("button-mark-sold-consignment-desktop", "disabled"),
    Output("button-mark-shipped-consignment-desktop", "disabled"),
    Output("button-mark-completed-consignment-desktop", "disabled"),
    Input("aggrid-consignment-table", "selectedRows"),
)
def set_disabled_when_selecting_multiple_rows(selected_rows):
    if selected_rows:
        statuses = set([rd.get("status") for rd in selected_rows])
        if len(statuses) > 1:
            return True, True, True, True, True, True, True, True
        status = statuses.pop()
        is_posted_disabled = status != "New" or len(selected_rows) < 1
        is_sold_disabled = status != "Posted" or len(selected_rows) != 1
        is_shipped_disabled = status != "Sold" or len(selected_rows) < 1
        is_completed_disabled = status != "Shipped" or len(selected_rows) < 1
        return is_posted_disabled, is_sold_disabled, is_shipped_disabled, is_completed_disabled, is_posted_disabled, is_sold_disabled, is_shipped_disabled, is_completed_disabled
    else:
        return True, True, True, True, True, True, True, True

# DONE: Button to change status of the item to POSTED
@callback(
    Output("modal-mark-posted-consignment", "opened", allow_duplicate=True),
    Input("button-mark-posted-consignment-desktop", "n_clicks"),
    Input("button-mark-posted-consignment-mobile", "n_clicks"),
    prevent_initial_call=True,
)
def open_modal_mark_posted(n_clicks_desktop, n_clicks_mobile):
    if n_clicks_desktop or n_clicks_mobile:
        return True
    return False

@callback(
    Output("modal-mark-posted-consignment", "opened", allow_duplicate=True),
    Output("consignment-notification", "sendNotifications", allow_duplicate=True),
    Output("signal-to-refresh-consignment-table", "data", allow_duplicate=True),
    Input("button-confirm-mark-posted-consignment", "n_clicks"),
    State("aggrid-consignment-table", "selectedRows"),
    State("textinput-ig-link-posted-consignment", "value"),
    prevent_initial_call=True,
)
def close_modal_mark_posted(n_clicks_confirm, selrows, link_ig):
    if n_clicks_confirm:
        cons_ids = "','".join([str(rd.get("consignment_id")) for rd in selrows]) if selrows else ""
        run_query_from_sql("update_consignment_posted.sql", consignment_ids=cons_ids, link_ig=link_ig)
        return False, [
            dict(
                title="Consignment berhasil diupdate",
                id="show-notify",
                action="show",
                message="Data Consignment telah berhasil diupdate menjadi posted, mohon refresh data.",
                icon=DashIconify(icon="fluent-mdl2:completed-solid"),
            )
        ], str(datetime.now())
    return True, no_update, no_update

@callback(
    Output("button-confirm-mark-posted-consignment", "disabled"),
    Input("textinput-ig-link-posted-consignment", "value"),
)
def check_mark_posted_input(link_ig):
    return not bool(link_ig and link_ig.strip())

# DONE: Button to change status of the item to SOLD
@callback(
    Output("modal-mark-sold-consignment", "opened", allow_duplicate=True),
    Output("text-consignment-to-sold", "children"),
    Output("autocomplete-buyer-whatsapp", "data"),
    Output("autocomplete-buyer-location", "data"),
    Output("autocomplete-sales-name-mark-sold-consignment", "data"),
    Input("button-mark-sold-consignment-desktop", "n_clicks"),
    Input("button-mark-sold-consignment-mobile", "n_clicks"),
    State("aggrid-consignment-table", "selectedRows"),
    prevent_initial_call=True,
)
def open_modal_mark_sold(n_clicks_desktop, n_clicks_mobile, selrows):
    if n_clicks_desktop or n_clicks_mobile:
        contact_was = [d.get("contact_wa") for d in run_query_from_sql("get_all_contacts.sql")]
        contact_locs = [d.get("contact_location") for d in run_query_from_sql("get_distinct_locations.sql")]
        all_sales = [d.get("sales_name") for d in run_query_from_sql("get_sales_name.sql")]
        rowdat = selrows[0] if selrows else None
        texts = [
            dmc.Text([
                "Mengupdate consignment ",
                dmc.Text(f'PP{rowdat.get("consignment_id")} ', fw="bold", span=True),
                " dengan data sebagai berikut:",
            ]),

            dmc.Text([
                dmc.Text("Barang Consignment: ", fw="bold", span=True),
                f'{rowdat.get("item_type").upper()} - {rowdat.get("item_name")}'
            ]),
            
            dmc.Text([
                dmc.Text("Owner: ", fw="bold", span=True),
                f'{rowdat.get("seller_name")} ({rowdat.get("seller_location")}) | ({rowdat.get("seller_wa")})'
            ]),
            
            dmc.Text([
                dmc.Text("Harga dari Owner: ", fw="bold", span=True),
                dmc.NumberFormatter(value=rowdat.get("price_modal"), thousandSeparator=",", prefix="Rp. "),
            ]),
            
            dmc.Text([
                dmc.Text("Harga di post di IG: ", fw="bold", span=True),
                dmc.NumberFormatter(value=rowdat.get("price_posted"), thousandSeparator=",", prefix="Rp. "),
            ]),
        ]
        return True, texts, contact_was, contact_locs, all_sales
    return False, None, [], []

@callback(
    Output("textinput-buyer-name", "value"),
    Output("autocomplete-buyer-location", "value"),
    Input("autocomplete-buyer-whatsapp", "value"),
    Input("autocomplete-buyer-whatsapp", "data"),
    prevent_initial_call=True,
    running=[
        (Output("textinput-buyer-name", "disabled"), True, False),
        (Output("autocomplete-buyer-location", "disabled"), True, False),
    ]
)
def get_buyer_details(buyer_wa, buyer_wa_opts):
    if buyer_wa not in buyer_wa_opts:
        return no_update
    else:
        data = run_query_from_sql("get_specific_contact.sql", contact_wa=buyer_wa)[0]
        return data.get("contact_name"), data.get("contact_location")

@callback(
    Output("div-input-mark-sold-consignment", "hidden"),
    Input("switch-consignment-sold-in-pasarpadel", "checked"),
)
def adjust_mark_sold_input_div(is_checked):
    return not is_checked

@callback(
    Output("button-confirm-mark-sold-consignment", "disabled"),
    Input("switch-consignment-sold-in-pasarpadel", "checked"),
    Input("autocomplete-sales-name-mark-sold-consignment", "value"),
    Input("autocomplete-buyer-whatsapp", "value"),
    Input("textinput-buyer-name", "value"),
    Input("autocomplete-buyer-location", "value"),
    Input("numberinput-price-sold", "value"),
)
def check_mark_sold_inputs(is_checked, sales_name, buyer_wa, buyer_name, buyer_location, price_sold):
    if is_checked:
        return not all([sales_name, buyer_wa, buyer_name, buyer_location, price_sold])
    else:
        return False

@callback(
    Output("modal-mark-sold-consignment", "opened", allow_duplicate=True),
    Output("consignment-notification", "sendNotifications", allow_duplicate=True),
    Output("signal-to-refresh-consignment-table", "data", allow_duplicate=True),
    Input("button-confirm-mark-sold-consignment", "n_clicks"),
    State("aggrid-consignment-table", "selectedRows"),
    State("switch-consignment-sold-in-pasarpadel", "checked"),
    State("autocomplete-sales-name-mark-sold-consignment", "value"),
    State("autocomplete-buyer-whatsapp", "value"),
    State("textinput-buyer-name", "value"),
    State("autocomplete-buyer-location", "value"),
    State("numberinput-price-sold", "value"),
    State("autocomplete-buyer-whatsapp", "data"),
    prevent_initial_call=True,
)
def close_modal_mark_sold(n_clicks_confirm, selrows, is_checked, sales_name, buyer_wa, buyer_name, buyer_location, price_sold, buyer_wa_data):
    if n_clicks_confirm:
        rowdat = selrows[0] if selrows else None
        cons_id = rowdat.get("consignment_id") if rowdat else None

        # Check if the owner contact exists
        if buyer_wa not in buyer_wa_data:
            # Add contact to CONTACTS table
            run_query_from_sql(
                "insert_new_contact.sql", 
                contact_name=buyer_name, 
                contact_wa=buyer_wa, 
                contact_location=buyer_location
            )
        else:
            run_query_from_sql(
                "update_contact.sql", 
                contact_name=buyer_name, 
                contact_wa=buyer_wa, 
                contact_location=buyer_location
            )

        if is_checked:
            run_query_from_sql("update_consignment_sold.sql", consignment_id=cons_id, sold_in_pasarpadel=1, sales_name=sales_name, buyer_wa=buyer_wa, price_sold=price_sold)
        else:
            run_query_from_sql("update_consignment_sold_elsewhere.sql", consignment_id=cons_id)

        return False, [
            dict(
                title="Consignment berhasil diupdate",
                id="show-notify",
                action="show",
                message="Data Consignment telah berhasil diupdate menjadi sold, mohon refresh data.",
                icon=DashIconify(icon="fluent-mdl2:completed-solid"),
            )
        ], str(datetime.now())
    return True, no_update, no_update


# DONE: Button to change status of the item to SHIPPED
@callback(
    Output("modal-mark-shipped-consignment", "opened", allow_duplicate=True),
    Input("button-mark-shipped-consignment-desktop", "n_clicks"),
    Input("button-mark-shipped-consignment-mobile", "n_clicks"),
    prevent_initial_call=True,
)
def open_modal_mark_shipped(n_clicks_desktop, n_clicks_mobile):
    if n_clicks_desktop or n_clicks_mobile:
        return True
    return False

@callback(
    Output("modal-mark-shipped-consignment", "opened", allow_duplicate=True),
    Output("consignment-notification", "sendNotifications", allow_duplicate=True),
    Output("signal-to-refresh-consignment-table", "data", allow_duplicate=True),
    Input("button-confirm-mark-shipped-consignment", "n_clicks"),
    State("aggrid-consignment-table", "selectedRows"),
    State("textinput-tracking-shipped-consignment", "value"),
    prevent_initial_call=True,
)
def close_modal_mark_shipped(n_clicks_confirm, selrows, tracking_code):
    if n_clicks_confirm:
        cons_ids = "','".join([str(rd.get("consignment_id")) for rd in selrows]) if selrows else ""
        run_query_from_sql("update_consignment_shipped.sql", consignment_ids=cons_ids, tracking_code=tracking_code)
        return False, [
            dict(
                title="Consignment berhasil diupdate",
                id="show-notify",
                action="show",
                message="Data Consignment telah berhasil diupdate menjadi shipped, mohon refresh data.",
                icon=DashIconify(icon="fluent-mdl2:completed-solid"),
            )
        ], str(datetime.now())
    return True, no_update, no_update

@callback(
    Output("button-confirm-mark-shipped-consignment", "disabled"),
    Input("textinput-tracking-shipped-consignment", "value"),
)
def check_mark_shipped_input(tracking_code):
    return not bool(tracking_code and tracking_code.strip())

# DONE: Button to change status of the item to COMPLETED
@callback(
    Output("modal-mark-completed-consignment", "opened", allow_duplicate=True),
    Input("button-mark-completed-consignment-desktop", "n_clicks"),
    Input("button-mark-completed-consignment-mobile", "n_clicks"),
    prevent_initial_call=True,
)
def open_modal_mark_completed(n_clicks_desktop, n_clicks_mobile):
    if n_clicks_desktop or n_clicks_mobile:
        return True
    return False

@callback(
    Output("modal-mark-completed-consignment", "opened", allow_duplicate=True),
    Output("consignment-notification", "sendNotifications", allow_duplicate=True),
    Output("signal-to-refresh-consignment-table", "data", allow_duplicate=True),
    Input("button-confirm-mark-completed-consignment", "n_clicks"),
    State("aggrid-consignment-table", "selectedRows"),
    prevent_initial_call=True,
)
def close_modal_mark_completed(n_clicks_confirm, selrows):
    if n_clicks_confirm:
        cons_ids = "','".join([str(rd.get("consignment_id")) for rd in selrows]) if selrows else ""
        run_query_from_sql("update_consignment_completed.sql", consignment_ids=cons_ids)
        return False, [
            dict(
                title="Consignment berhasil diupdate",
                id="show-notify",
                action="show",
                message="Data Consignment telah berhasil diupdate menjadi completed, mohon refresh data.",
                icon=DashIconify(icon="fluent-mdl2:completed-solid"),
            )
        ], str(datetime.now())
    return True, no_update, no_update

# Open details
@callback(
    Output("modal-consignment-details", "opened", allow_duplicate=True),
    Output("consignment-notification", "sendNotifications", allow_duplicate=True),
    Output("div-consignment-detail-information", "children"),
    Output("numberinput-price-posted-changes", "value"),
    Output("numberinput-price-modal-changes", "value"),
    Input("aggrid-consignment-table", "cellDoubleClicked"),
    State("aggrid-consignment-table", "selectedRows"),
    prevent_initial_call=True,
)
def open_details(cell_data, selrows):
    if selrows:    
        if len(selrows) > 1:
            return no_update, [
                dict(
                    title="Peringatan",
                    id="show-notify",
                    action="show",
                    message="Silakan pilih hanya satu consignment untuk melihat detailnya.",
                    icon=DashIconify(icon="ep-warning"),
                )
            ], no_update, no_update, no_update
        
        rowdat = selrows[0]
        print(rowdat)

        # Text untuk detail consignment awal
        text_consignment_start = dmc.Text(
            [
                dmc.Text([
                    "Consignment ",
                    dmc.Text(f'PP{rowdat.get("consignment_id")} ', fw="bold", span=True),
                    " dengan data sebagai berikut:",
                ]),

                dmc.Text([
                    dmc.Text("Barang Consignment: ", fw="bold", span=True),
                    f'{rowdat.get("item_type").upper()} - {rowdat.get("item_name")}'
                ]),
                
                dmc.Text([
                    dmc.Text("Owner: ", fw="bold", span=True),
                    f'{rowdat.get("seller_name")} ({rowdat.get("seller_location")}) | ({rowdat.get("seller_wa")})'
                ]),
                
                dmc.Text([
                    dmc.Text("Harga dari Owner: ", fw="bold", span=True),
                    dmc.NumberFormatter(value=rowdat.get("price_modal"), thousandSeparator=",", prefix="Rp. "),
                ]),
                
                dmc.Text([
                    dmc.Text("Harga di post di IG: ", fw="bold", span=True),
                    dmc.NumberFormatter(value=rowdat.get("price_posted"), thousandSeparator=",", prefix="Rp. "),
                ]),
            ],
            size="xs",
            mb=10
        )
        text_consignment_instagram = [
            dmc.Divider(label="Link Instagram Post", variant="dashed", my=10),
            dmc.Text([
                dmc.Text("Instagram Link: ", fw="bold", span=True),
                dmc.Anchor(rowdat.get("link_ig"), href=rowdat.get("link_ig"), target="_blank") if rowdat.get("link_ig") else "-"
            ], size="xs")
        ]

        text_consignment_sold = [
            dmc.Divider(label="Informasi Penjualan", variant="dashed", my=10),
            dmc.Text(
                [
                    dmc.Text([
                        dmc.Text("Tanggal Terjual: ", fw="bold", span=True),
                        f'{rowdat.get("sold_date")}' if rowdat.get("sold_date") else "-"
                    ]),

                    dmc.Text([
                        dmc.Text("Pembeli: ", fw="bold", span=True),
                        f'{rowdat.get("buyer_name")} ({rowdat.get("buyer_location")}) | ({rowdat.get("buyer_wa")})' if rowdat.get("buyer_wa") else "-"
                    ]),
                    
                    dmc.Text([
                        dmc.Text("Nama Sales: ", fw="bold", span=True),
                        f'{rowdat.get("sales_name")}' if rowdat.get("sales_name") else "-"
                    ]),
                    
                    dmc.Text([
                        dmc.Text("Harga Terjual: ", fw="bold", span=True),
                        dmc.NumberFormatter(value=rowdat.get("price_sold"), thousandSeparator=",", prefix="Rp. "),
                    ]),
                ],
                size="xs",
                mb=10
            )
        ]

        text_consignment_shipped = [
            dmc.Divider(label="Informasi Pengiriman", variant="dashed", my=10),
            dmc.Text([
                dmc.Text("Tracking ID: ", fw="bold", span=True),
                f'{rowdat.get("tracking_id")}' if rowdat.get("tracking_id") else "-"
            ], size="xs")
        ]

        is_disabled = rowdat.get("status") in ("Sold", "Shipped", "Completed", "Completed Elsewhere")
        details = [
            text_consignment_start,
            generate_button("button-edit-price-consignment", "Edit Harga", "Edit harga dari owner / harga yang di post di IG", "second", "typcn-edit", disabled=is_disabled),
            *text_consignment_instagram,
            *text_consignment_sold,
            *text_consignment_shipped,
            dmc.Grid(
                [
                    dmc.GridCol(
                        generate_button("button-unsold-consignment", "Batalkan Penjualan", "Batalkan penjualan dan kembalikan status ke Posted", "third", "ic-round-cancel", disabled=rowdat.get("status") in ("New", "Posted", "Completed")),
                        span=6
                    ),
                    dmc.GridCol(
                        generate_button("button-delete-consignment", "Delete Consignment", "Hapus data consignment", "fifth", "fluent-mdl2:delete", disabled=rowdat.get("status")=="Completed"),
                        span=6
                    )
                ],
                mt=10
            )
        ]

        return True, no_update, details, rowdat.get("price_posted"), rowdat.get("price_modal")
    else:
        return no_update, no_update, no_update, no_update, no_update

@callback(
    Output("modal-edit-price-consignment", "opened", allow_duplicate=True),
    Input("button-edit-price-consignment", "n_clicks"),
    prevent_initial_call=True,
)
def open_modal_edit_price(n_clicks):
    if n_clicks:
        return True
    return False

@callback(
    Output("modal-edit-price-consignment", "opened", allow_duplicate=True),
    Output("consignment-notification", "sendNotifications", allow_duplicate=True),
    Output("modal-consignment-details", "opened", allow_duplicate=True),
    Output("signal-to-refresh-consignment-table", "data", allow_duplicate=True),
    Input("button-confirm-edit-price-consignment", "n_clicks"),
    State("numberinput-price-posted-changes", "value"),
    State("numberinput-price-modal-changes", "value"),
    State("aggrid-consignment-table", "selectedRows"),
    prevent_initial_call=True,
)
def close_modal_edit_price(n_clicks_confirm, price_posted, price_modal, selrows):
    if n_clicks_confirm:
        rowdat = selrows[0] if selrows else None
        cons_id = rowdat.get("consignment_id") if rowdat else None
        run_query_from_sql("update_consignment_price.sql", consignment_id=cons_id, price_posted=price_posted, price_modal=price_modal)
        return False, [
            dict(
                title="Consignment berhasil diupdate",
                id="show-notify",
                action="show",
                message="Data Consignment telah berhasil diupdate harganya, mohon refresh data.",
                icon=DashIconify(icon="fluent-mdl2:completed-solid"),
            )
        ], False, str(datetime.now())
    return True, no_update, no_update, no_update

@callback(
    Output("modal-consignment-details", "opened", allow_duplicate=True),
    Output("consignment-notification", "sendNotifications", allow_duplicate=True),
    Output("signal-to-refresh-consignment-table", "data", allow_duplicate=True),
    Input("button-unsold-consignment", "n_clicks"),
    State("aggrid-consignment-table", "selectedRows"),
    prevent_initial_call=True,
)
def unsold_data(n_clicks, selrows):
    if n_clicks:
        rowdat = selrows[0] if selrows else None
        cons_id = rowdat.get("consignment_id") if rowdat else None
        run_query_from_sql("unsold_consignment.sql", consignment_id=cons_id)
        return False, [
            dict(
                title="Penjualan consignment berhasil dibatalkan",
                id="show-notify",
                action="show",
                message="Data Consignment telah berhasil dibatalkan penjualannya, mohon refresh data.",
                icon=DashIconify(icon="fluent-mdl2:completed-solid"),
            )
        ], str(datetime.now())
    return no_update, no_update, no_update

@callback(
    Output("modal-consignment-details", "opened", allow_duplicate=True),
    Output("consignment-notification", "sendNotifications", allow_duplicate=True),
    Output("signal-to-refresh-consignment-table", "data", allow_duplicate=True),
    Input("button-delete-consignment", "n_clicks"),
    State("aggrid-consignment-table", "selectedRows"),
    prevent_initial_call=True,
)
def delete_data(n_clicks, selrows):
    if n_clicks:
        rowdat = selrows[0] if selrows else None
        cons_id = rowdat.get("consignment_id") if rowdat else None
        run_query_from_sql("delete_consignment.sql", consignment_id=cons_id)
        return False, [
            dict(
                title="Penjualan consignment berhasil dihapus",
                id="show-notify",
                action="show",
                message="Data Consignment telah berhasil dihapus, mohon refresh data.",
                icon=DashIconify(icon="fluent-mdl2:completed-solid"),
            )
        ], str(datetime.now())
    return no_update, no_update, no_update

# --------------------------------
# End of File