"""pages/consignment.py
Main consignment management page.

Allows users to:
  - View all consignments in a filterable/sortable AG Grid table.
  - Add a new consignment via a multi-step modal form.
  - Progress consignments through statuses: New → Posted → Sold → Shipped → Completed.
  - View full consignment details (double-click a row).
  - Edit prices, reverse a sale, or delete a consignment from the details modal.
"""

import ast
from datetime import datetime
from pandas import to_datetime as pd_to_timestamp

import dash_mantine_components as dmc
import dash_ag_grid as dag
from dash import clientside_callback, register_page, callback, Output, Input, State, html, no_update, dcc
from dash_iconify import DashIconify

from utils import (
    run_query_from_sql,
    check_any_input_is_empty,
    generate_button,
    generate_multi_select,
    consignment_type_options,
    status_type_options,
)

register_page(__name__, path="/")

# ── Constants ─────────────────────────────────────────────────────────────────
# Helper string used to build SQL IN-clause tuples from lists
tuplejoiner = "','"

# ── AG Grid value formatters (JS expressions evaluated client-side) ───────────
value_formatter_currency = {"function": "`Rp. `+d3.format(',.0f')(params.value)"}
value_formatter_id       = {"function": "`PP` + params.value"}
# value_formatter_rating   = {"function": "params.value ? d3.format(',.1f')(params.value) + ' / 10.0' : 'N/A'"}

# ── Consignment table column definitions ──────────────────────────────────────
consignment_table_columns = [
    {"headerName": "Consignment ID",    "field": "consignment_id",    "valueFormatter": value_formatter_id},
    {"headerName": "Tipe Barang",       "field": "item_type",         "filter": False},
    {"headerName": "Nama Barang",       "field": "item_name"},
    {"headerName": "Extra Description", "field": "extra_description"},
    {"headerName": "Harga Modal",       "field": "price_modal",       "valueFormatter": value_formatter_currency},
    {"headerName": "Harga di Instagram","field": "price_posted",      "valueFormatter": value_formatter_currency},
    {"headerName": "WA Seller",         "field": "seller_wa"},
    {"headerName": "Nama Seller",       "field": "seller_name"},
    {"headerName": "Lokasi",            "field": "seller_location"},
    {"headerName": "Kondisi Barang",    "field": "item_condition_rating"},
    # {"headerName": "Rating Barang",     "field": "item_rating",      "valueFormatter": value_formatter_rating},
    {"headerName": "Status Barang",     "field": "status",            "filter": False},
    {"headerName": "Tanggal Posted",    "field": "consignment_date",},
    {"headerName": "Tanggal Terjual",   "field": "sold_date",},
]

# Row background colours keyed by consignment status
getRowStyle = {
    "styleConditions": [
        {"condition": "params.data.status == 'New'",                "style": {"backgroundColor": "#F6FFA3AA", "color": "black"}},
        {"condition": "params.data.status == 'Posted'",             "style": {"backgroundColor": "#FFFFFFCC", "color": "black"}},
        {"condition": "params.data.status == 'Sold'",               "style": {"backgroundColor": "#A9C1FF99", "color": "black"}},
        {"condition": "params.data.status == 'Shipped'",            "style": {"backgroundColor": "#AEE5CC99", "color": "black"}},
        {"condition": "params.data.status == 'Completed Elsewhere'","style": {"backgroundColor": "#D3D3D366", "color": "black"}},
        {"condition": "params.data.status == 'Completed'",          "style": {"backgroundColor": "#B8F2D999", "color": "black"}},
    ],
    "defaultStyle": {"backgroundColor": "grey", "color": "white"},
}

consignment_table = dag.AgGrid(
    id="aggrid-consignment-table",
    className="ag-theme-quartz",
    columnDefs=consignment_table_columns,
    rowData=run_query_from_sql(
        "get_all_consignments.sql",
        sel_types=f"('{tuplejoiner.join(consignment_type_options)}')",
        sel_status=f"('{tuplejoiner.join(status_type_options)}')",
    ),
    defaultColDef={
        "sortable":   True,
        "filter":     True,
        "resizable":  True,
        "minWidth":   150,
    },
    dashGridOptions={
        "pagination":               True,
        "paginationPageSize":       250,
        "paginationPageSizeSelector": False,
        "rowBuffer":                0,
        "rowSelection": {
            "mode":                 "multiRow",
            "enableClickSelection": True,
        },
        "suppressColumnVirtualisation": True,
        "applyColumnDefOrder": True,
    },
    style={"height": "500px", "width": "100%", "--ag-font-size": "0.8rem"},
    persistence=True,
    persisted_props=["filterModel", "columnState"],
    dangerously_allow_code=True,
    getRowStyle=getRowStyle,
)


# ── Modal: Register new consignment ──────────────────────────────────────────
modal_register_new = dmc.Modal(
    id="modal-register-consignment",
    size="lg",
    title=dmc.Text("Form Consignment Baru", fw=500, fz="lg"),
    children=dmc.Stack(
        [
            dmc.Text(
                "Gunakan form dibawah ini untuk menginputkan data consignment baru. Setelah input data terbuat, data consignment bisa dipakai untuk pembuatan caption dan lainnya.",
                fz="xs",
            ),
            dmc.Divider(),

            dmc.Accordion(
                id="accordion-new-consignment",
                multiple=True,
                variant="separated",
                radius="md",
                children=[

                    # Section 1: Item detail
                    dmc.AccordionItem(
                        value="accordionitem-new-consignment-item-detail",
                        children=[
                            dmc.AccordionControl(
                                "Detail Barang",
                                icon=DashIconify(icon="material-symbols:padel-outline"),
                            ),
                            dmc.AccordionPanel(
                                [
                                    dmc.Select(
                                        id="select-new-consignment-type",
                                        label="Tipe Consignment",
                                        size="xs",
                                        data=consignment_type_options,
                                        value="",
                                        withAsterisk=True,
                                    ),

                                    # Brand autocomplete
                                    dmc.Autocomplete(
                                        id="autocomplete-item-brand",
                                        label="Brand Barang",
                                        size="xs",
                                        placeholder="Masukkan nama brand barang.",
                                        withAsterisk=True,
                                        selectFirstOptionOnChange=True,
                                        limit=15,
                                        debounce=300,
                                        value="",
                                    ),

                                    # Item name autocomplete
                                    dmc.Autocomplete(
                                        id="autocomplete-item-name",
                                        label="Nama Barang",
                                        size="xs",
                                        placeholder="Masukkan nama barang.",
                                        withAsterisk=True,
                                        selectFirstOptionOnChange=True,
                                        limit=15,
                                        debounce=300,
                                        value="",
                                    ),

                                    dmc.Divider(label="Detail Barang", labelPosition="center"),

                                    # ── Racket-specific inputs (shown when type = Racket) ──
                                    html.Div(
                                        id="div-input-racket-consignment",
                                        children=[
                                            dmc.Switch(
                                                id="switch-racket-women",
                                                label="Woman's Racket",
                                                size="xs",
                                                checked=False,
                                                description="Toggle untuk menandakan bahwa raket adalah raket wanita",
                                                onLabel=DashIconify(icon="material-symbols-light-female", width=15, color="gray"),
                                                mt=1,
                                            ),
                                            dmc.Autocomplete(
                                                id="autocomplete-racket-shape",
                                                label="Shape Racket",
                                                size="xs",
                                                withAsterisk=True,
                                                selectFirstOptionOnChange=True,
                                                debounce=300,
                                            ),
                                            dmc.Autocomplete(
                                                id="autocomplete-racket-facematerial",
                                                label="Surface Material",
                                                size="xs",
                                                placeholder="Masukkan surface material",
                                                withAsterisk=True,
                                                selectFirstOptionOnChange=True,
                                                limit=15,
                                                debounce=300,
                                            ),
                                            dmc.Autocomplete(
                                                id="autocomplete-racket-corematerial",
                                                label="Core Material",
                                                size="xs",
                                                placeholder="Masukkan core material",
                                                withAsterisk=True,
                                                selectFirstOptionOnChange=True,
                                                limit=15,
                                                debounce=300,
                                            ),
                                            dmc.TagsInput(
                                                id="tagsinput-racket-additionalspec",
                                                label="Additional Specification",
                                                size="xs",
                                                data=["Attack", "Balance", "Comfort", "Control", "Large Sweet Spot",
                                                      "Light", "Powerful", "Precision", "Top Heavy"],
                                            ),
                                            dmc.TextInput(
                                                id="textinput-racket-weight",
                                                label="Berat Asli",
                                                size="xs",
                                                placeholder="Masukkan berat asli raket dalam gram (g) dengan format ###G. Contoh: 132G",
                                            ),
                                        ],
                                    ),

                                    # ── Non-racket inputs (shown when type ≠ Racket) ──
                                    html.Div(
                                        id="div-input-others-consignment",
                                        children=[
                                            html.Div(
                                                dmc.TextInput(
                                                    id="textinput-shoe-size",
                                                    label="Ukuran Sepatu",
                                                    size="xs",
                                                    placeholder="Masukkan ukuran sepatu dengan sizing EUR. Contoh: EUR41",
                                                ),
                                                id="div-input-shoes-size",
                                            ),
                                            html.Div(
                                                dmc.TextInput(
                                                    id="textinput-shirt-size",
                                                    label="Ukuran Baju",
                                                    size="xs",
                                                    placeholder="Masukkan ukuran baju sesuai dengan barangnya. Contoh: Small",
                                                ),
                                                id="div-input-shirt-size",
                                            ),
                                            html.Div(
                                                dmc.Textarea(
                                                    id="textarea-others-description",
                                                    label="Deskripsi Barang",
                                                    size="xs",
                                                    placeholder="Masukkan deskripsi barang consignment ini",
                                                ),
                                                id="div-input-others-description",
                                            ),
                                        ],
                                    ),
                                ]
                            ),
                        ],
                    ),

                    # Section 2: Owner detail
                    dmc.AccordionItem(
                        value="accordionitem-new-consignment-owner-detail",
                        children=[
                            dmc.AccordionControl(
                                "Detail Owner",
                                icon=DashIconify(icon="mingcute-user-3-line"),
                            ),
                            dmc.AccordionPanel(
                                [
                                    dmc.Autocomplete(
                                        id="autocomplete-owner-whatsapp",
                                        label="Owner WhatsApp",
                                        size="xs",
                                        placeholder="Masukkan nomor WhatsApp pemilik barang consignment",
                                        selectFirstOptionOnChange=True,
                                        limit=15,
                                        debounce=300,
                                        withAsterisk=True,
                                    ),
                                    dmc.TextInput(
                                        id="textinput-owner-name",
                                        label="Nama Pemilik",
                                        size="xs",
                                        placeholder="Masukkan nama pemilik barang consignment",
                                        withAsterisk=True,
                                    ),
                                    dmc.Autocomplete(
                                        id="autocomplete-owner-location",
                                        label="Lokasi Pemilik",
                                        size="xs",
                                        placeholder="Masukkan lokasi pemilik barang consignment",
                                        withAsterisk=True,
                                    ),
                                ]
                            ),
                        ],
                    ),

                    # Section 3: Consignment pricing & condition
                    dmc.AccordionItem(
                        value="accordionitem-new-consignment-consignment-detail",
                        children=[
                            dmc.AccordionControl(
                                "Detail Consignment",
                                icon=DashIconify(icon="material-symbols:sell-outline-sharp"),
                            ),
                            dmc.AccordionPanel(
                                dmc.Stack(
                                    [
                                        dmc.Switch(
                                            id="switch-old-racket",
                                            label="Barang Lama / Baru",
                                            size="xs",
                                            description="Aktifkan jika barang consignment ini bukan barang baru",
                                        ),

                                        # Rating input — only shown for used items
                                        html.Div(
                                            dmc.NumberInput(
                                                id="numberinput-rating",
                                                label="Rating Barang",
                                                size="xs",
                                                withAsterisk=True,
                                                min=0, max=10,
                                                decimalScale=1,
                                                fixedDecimalScale=True,
                                                value=10,
                                                suffix=" / 10.0",
                                            ),
                                            id="div-input-item-rating",
                                        ),

                                        dmc.NumberInput(
                                            id="numberinput-price-modal",
                                            label="Harga dari Owner (Rp.)",
                                            size="xs",
                                            thousandSeparator=",",
                                            prefix="Rp.",
                                            withAsterisk=True,
                                            allowNegative=False,
                                            value=10000,
                                        ),
                                        dmc.NumberInput(
                                            id="numberinput-price-posted",
                                            label="Harga Jual (Rp.)",
                                            size="xs",
                                            thousandSeparator=",",
                                            prefix="Rp.",
                                            withAsterisk=True,
                                            allowNegative=False,
                                            value=10000,
                                        ),
                                        dmc.Textarea(
                                            id="textarea-extranote",
                                            label="Extra Note",
                                            size="xs",
                                            description="Masukkan catatan tambahan terkait consignment ini (akan muncul di Caption IG jika diisi)",
                                        ),
                                    ],
                                    gap="xs",
                                )
                            ),
                        ],
                    ),
                ],
                value=["accordionitem-new-consignment-item-detail", "accordionitem-new-consignment-owner-detail", "accordionitem-new-consignment-consignment-detail"]
            ),

            # Submit button
            dmc.Button(
                id="button-register-consignment",
                children="Tambahkan Consignment",
                fullWidth=True,
                color="#5B8710",
            ),
        ],
        gap="xs",
    ),
)


# ── Modal: Mark as Posted ─────────────────────────────────────────────────────
modal_posted = dmc.Modal(
    id="modal-mark-posted-consignment",
    size="md",
    title=dmc.Text("Update Consignment 'Posted'", fw=500, fz="lg"),
    children=[
        dmc.Text(
            "Gunakan Caption IG yang sudah dibuat dibawah ini untuk memposting consignment di Instagram. Pastikan untuk memasukkan link postingan Instagram dengan benar untuk mengupdate status consignment menjadi 'Posted'.",
            size="xs", mb=10,
        ),
        dmc.Flex(
            justify="space-between",
            align="center",
            children=[
                dmc.Stack(
                    gap=0,
                    children=[
                        dmc.Text("Caption IG", size="xs", fw=500),
                        dmc.Text("Klik tombol copy di kanan untuk menyalin caption IG ke clipboard", size="xs", c="dimmed"),
                    ],
                ),
                dmc.ActionIcon(
                    id="copy-caption-ig-posted-consignment",
                    children=DashIconify(icon="fa6-solid:copy"),
                    size="xs",
                    variant="subtle",
                ),
            ],
        ),
        dmc.Textarea(
            id="textarea-caption-ig-posted-consignment",
            size="xs",
            minRows=6,
            autosize=True,
        ),
        dmc.TextInput(
            id="textinput-ig-link-posted-consignment",
            label="Link Instagram",
            placeholder="Masukkan link Instagram tempat consignment diposting",
            size="xs",
            withAsterisk=True,
        ),
        dmc.Space(h="md"),
        generate_button(
            "button-confirm-mark-posted-consignment",
            "Submit",
            "Klik untuk mengkonfirmasi perubahan status consignment menjadi 'Posted'",
            "gray",
            "mdi-instagram",
        ),
    ],
)


# ── Modal: Mark as Sold ───────────────────────────────────────────────────────
modal_sold = dmc.Modal(
    id="modal-mark-sold-consignment",
    size="md",
    title=dmc.Text("Update Consignment 'Sold'", fw=500, fz="lg"),
    children=[
        dmc.Text(id="text-consignment-to-sold", size="xs", mb=10),
        dmc.Switch(
            id="switch-consignment-sold-in-pasarpadel",
            label="Terjual di Pasar Padel",
            description="Centang untuk mengkonfirmasi bahwa consignment telah terjual di Pasar Padel",
            size="xs",
            checked=True,
            mt=0,
            mb=10,
        ),
        html.Div(
            id="div-input-mark-sold-consignment",
            children=[
                dmc.Autocomplete(
                    id="autocomplete-sales-name-mark-sold-consignment",
                    label="Nama Sales",
                    size="xs",
                    placeholder="Masukkan nama sales yang menangani penjualan consignment",
                    selectFirstOptionOnChange=True,
                    limit=15,
                    debounce=300,
                    withAsterisk=True,
                ),
                dmc.Autocomplete(
                    id="autocomplete-buyer-whatsapp",
                    label="Buyer WhatsApp",
                    size="xs",
                    placeholder="Masukkan nomor WhatsApp pembeli barang consignment",
                    selectFirstOptionOnChange=True,
                    limit=15,
                    debounce=300,
                    withAsterisk=True,
                ),
                dmc.TextInput(
                    id="textinput-buyer-name",
                    label="Nama Pembeli",
                    size="xs",
                    placeholder="Masukkan nama pembeli barang consignment",
                    withAsterisk=True,
                ),
                dmc.Autocomplete(
                    id="autocomplete-buyer-location",
                    label="Lokasi Pembeli",
                    size="xs",
                    placeholder="Masukkan lokasi pembeli barang consignment",
                    withAsterisk=True,
                ),
                dmc.NumberInput(
                    id="numberinput-price-sold",
                    label="Harga Terjual (Rp.)",
                    size="xs",
                    thousandSeparator=",",
                    prefix="Rp.",
                    withAsterisk=True,
                    allowNegative=False,
                    value=10000,
                ),
            ],
        ),
        dmc.Space(h="md"),
        generate_button(
            "button-confirm-mark-sold-consignment",
            "Submit",
            "Klik untuk mengkonfirmasi perubahan status consignment menjadi 'Sold'",
            "fourth",
            "material-symbols:sell-outline-sharp",
        ),
    ],
)


# ── Modal: Mark as Shipped ────────────────────────────────────────────────────
modal_shipped = dmc.Modal(
    id="modal-mark-shipped-consignment",
    size="md",
    title=dmc.Text("Update Consignment 'Shipped'", fw=500, fz="lg"),
    children=[
        dmc.TextInput(
            id="textinput-tracking-shipped-consignment",
            label="Tracking Code",
            placeholder="Masukkan nomor tracking consignment",
            size="xs",
            withAsterisk=True,
        ),
        dmc.Space(h="md"),
        generate_button(
            "button-confirm-mark-shipped-consignment",
            "Submit",
            "Klik untuk mengkonfirmasi perubahan status consignment menjadi 'Shipped'",
            "fifth",
            "gridicons-shipping",
        ),
    ],
)


# ── Modal: Mark as Completed ──────────────────────────────────────────────────
modal_completed = dmc.Modal(
    id="modal-mark-completed-consignment",
    size="md",
    title=dmc.Text("Update Consignment 'Completed'", fw=500, fz="lg"),
    children=[
        dmc.Text(
            "Apakah Anda yakin ingin menandai consignment ini sebagai 'Completed'? Pastikan bahwa barang sudah diterima pembeli dan tidak ada masalah terkait transaksi consignment ini sebelum mengkonfirmasi perubahan status menjadi 'Completed'.",
            size="xs",
        ),
        dmc.Space(h="md"),
        generate_button(
            "button-confirm-mark-completed-consignment",
            "Submit",
            "Klik untuk mengkonfirmasi perubahan status consignment menjadi 'Completed'",
            "fifth",
            "gridicons-shipping",
        ),
    ],
)


# ── Modal: Edit price ─────────────────────────────────────────────────────────
modal_change_price = dmc.Modal(
    id="modal-edit-price-consignment",
    size="md",
    title=dmc.Text("Edit Harga Consignment", fw=500, fz="lg"),
    children=[
        dmc.Text(
            "Gunakan form dibawah ini untuk mengubah harga consignment. Pastikan untuk memasukkan harga yang valid dan sesuai dengan kondisi consignment saat ini. REFRESH DATA SETELAH PERUBAHAN.",
            size="xs",
            mb=10,
        ),
        dmc.NumberInput(
            id="numberinput-price-modal-changes",
            label="Ubah Harga dari Owner (Rp.)",
            size="xs",
            thousandSeparator=",",
            prefix="Rp.",
            allowNegative=False,
        ),
        dmc.NumberInput(
            id="numberinput-price-posted-changes",
            label="Ubah Harga yang di post di IG (Rp.)",
            size="xs",
            thousandSeparator=",",
            prefix="Rp.",
            allowNegative=False,
        ),
        dmc.Space(h="md"),
        generate_button(
            "button-confirm-edit-price-consignment",
            "Submit",
            "Klik untuk mengkonfirmasi perubahan harga consignment",
            "first",
            "fa7-regular--edit",
        ),
    ],
)


# ── Modal: Consignment details (opened on row double-click) ───────────────────
modal_details = dmc.Modal(
    id="modal-consignment-details",
    size="lg",
    title=dmc.Text("Detail Consignment", fw=500, fz="lg"),
    children=dmc.Stack(
        [
            dmc.Text(
                "Detail informasi terkait consignment yang dipilih akan ditampilkan pada modal ini. Gunakan informasi ini untuk memverifikasi data consignment atau untuk keperluan lainnya.",
                fz="xs",
            ),
            dmc.Divider(),
            html.Div(id="div-consignment-detail-information"),
        ],
        gap="xs",
    ),
)


# ── Page layout ───────────────────────────────────────────────────────────────
subtitle_text = (
    "Tambah / Edit data consignmentmu disini. Untuk menambahkan data consignment, "
    "silahkan klik tombol 'Add Consignment' dibawah. Untuk mengedit data consignment, "
    "silahkan klik dua kali pada baris data consignment yang ingin diubah."
)

layout = dmc.AppShellMain(
    [
        dmc.Title("Consignments"),
        dmc.Text(subtitle_text, size="sm", visibleFrom="sm", c="dimmed", mb=20),
        dmc.Text(subtitle_text, size="xs", hiddenFrom="sm",  c="dimmed", mb=20),

        dmc.LoadingOverlay(
            id="loading-overlay-register-consignment",
            visible=False,
            overlayProps={"radius": "sm", "blur": 2},
            zIndex=10,
        ),
        dmc.NotificationContainer(id="consignment-notification"),

        # In-memory store used to signal table refresh
        dcc.Store(id="signal-to-refresh-consignment-table", storage_type="memory"),

        # All modals (rendered in the DOM but hidden by default)
        modal_register_new,
        modal_posted,
        modal_sold,
        modal_shipped,
        modal_completed,
        modal_details,
        modal_change_price,

        # ── Desktop filter row ────────────────────────────────────────────────
        dmc.Stack(
            [
                dmc.Accordion(
                    children=dmc.AccordionItem(
                        [
                            dmc.AccordionControl(
                                "Filter Data Consignment",
                                icon=DashIconify(icon="mingcute-filter-line"),
                            ),
                            dmc.AccordionPanel(
                                dmc.Group(
                                    [
                                        generate_multi_select("multiselect-filter-item-type-desktop",   "Tipe Barang",   "Pilih tipe consigment untuk mengfilter data consignment",   consignment_type_options),
                                        generate_multi_select("multiselect-filter-item-status-desktop", "Status Barang", "Pilih status consignment untuk memfilter data consignment", status_type_options),
                                        generate_button("button-add-consignment-desktop",     "Tambah Consignment Baru",      "Klik untuk menambahkan data consignment baru",               "first", "gg:add"),
                                        generate_button("button-refresh-consignment-desktop", "Refresh Tabel Consignment",    "Klik untuk meng-refresh data pada tabel consignment",        "gray",  "material-symbols:refresh"),
                                    ],
                                    justify="space-evenly",
                                    gap="md",
                                    grow=True,
                                ),
                            ),
                        ],
                        value="filter-accordion-item",
                    ),
                    chevronPosition="right",
                    radius="md",
                    variant="separated",
                    value="filter-accordion-item",
                ),
            ],
            visibleFrom="sm",
            mb=20,
        ),

        # ── Mobile filter row ─────────────────────────────────────────────────
        dmc.Stack(
            [
                generate_button("button-add-consignment-mobile", "Tambah Consignment Baru", "Klik untuk menambahkan data consignment baru", "first", "gg:add"),
                dmc.Accordion(
                    children=dmc.AccordionItem(
                        [
                            dmc.AccordionControl(
                                "Filter Data Consignment",
                                icon=DashIconify(icon="mingcute-filter-line"),
                            ),
                            dmc.AccordionPanel(
                                dmc.Stack(
                                    [
                                        generate_multi_select("multiselect-filter-item-type-mobile",   "Tipe Barang",   "Pilih tipe consigment untuk mengfilter data consignment",   consignment_type_options),
                                        generate_multi_select("multiselect-filter-item-status-mobile", "Status Barang", "Pilih status consignment untuk memfilter data consignment", status_type_options),
                                        generate_button("button-refresh-consignment-mobile", "Refresh Tabel Consignment", "Klik untuk meng-refresh data pada tabel consignment", "gray", "material-symbols:refresh"),
                                    ]
                                ),
                            ),
                        ],
                        value="filter-accordion-item",
                    ),
                    chevronPosition="right",
                    radius="md",
                    variant="separated",
                ),
            ],
            hiddenFrom="sm",
            mb=10,
        ),

        # ── Desktop status action buttons ─────────────────────────────────────
        dmc.Group(
            [
                generate_button("button-mark-posted-consignment-desktop",    "Update ke Posted",    "Memasukkan link IG dan menandai consignment sebagai 'Posted'",                   "gray",   "mdi-instagram"),
                generate_button("button-mark-sold-consignment-desktop",      "Update ke Sold",      "Menandai consignment sebagai 'Sold'",                                            "fourth", "material-symbols:sell-outline-sharp"),
                generate_button("button-mark-shipped-consignment-desktop",   "Update ke Shipped",   "Memasukkan Tracking Code Menandai consignment sebagai 'Shipped'",               "fifth",  "gridicons-shipping"),
                generate_button("button-mark-completed-consignment-desktop", "Update ke Completed", "Menandai consignment sebagai 'Completed'",                                      "first",  "mdi-done-all"),
            ],
            justify="space-evenly",
            mb=10,
            mt=25,
            grow=True,
            visibleFrom="sm",
        ),

        # ── Mobile status action buttons (short labels) ───────────────────────
        dmc.Group(
            [
                generate_button("button-mark-posted-consignment-mobile",    "Post", "Memasukkan link IG dan menandai consignment sebagai 'Posted'",  "gray",   "mdi-instagram"),
                generate_button("button-mark-sold-consignment-mobile",      "Sold", "Menandai consignment sebagai 'Sold'",                           "fourth", "material-symbols:sell-outline-sharp"),
                generate_button("button-mark-shipped-consignment-mobile",   "Ship", "Memasukkan Tracking Code Menandai consignment sebagai 'Shipped'","fifth", "gridicons-shipping"),
                generate_button("button-mark-completed-consignment-mobile", "Done", "Menandai consignment sebagai 'Completed'",                      "first",  "mdi-done-all"),
            ],
            justify="space-evenly",
            mb=10,
            gap="xs",
            grow=True,
            hiddenFrom="sm",
        ),

        consignment_table,
    ]
)


# ══════════════════════════════════════════════════════════════════════════════
# CALLBACKS
# ══════════════════════════════════════════════════════════════════════════════

# ── Dark theme ────────────────────────────────────────────────────────────────
@callback(
    Output("aggrid-consignment-table", "className"),
    Input("switch-color-scheme", "checked"),
    supress_callback_exceptions=True,
)
def toggle_color_scheme(switch_on):
    """Switch the AG Grid theme class between light and dark."""
    return "ag-theme-quartz-dark" if switch_on else "ag-theme-quartz"


# ── Refresh consignment table ─────────────────────────────────────────────────
@callback(
    Output("aggrid-consignment-table", "rowData"),
    Input("button-refresh-consignment-desktop", "n_clicks"),
    Input("button-refresh-consignment-mobile",  "n_clicks"),
    Input("signal-to-refresh-consignment-table", "data"),
    Input("url", "pathname"),
    Input("multiselect-filter-item-type-desktop",   "value"),
    Input("multiselect-filter-item-status-desktop", "value"),
    Input("multiselect-filter-item-type-mobile",    "value"),
    Input("multiselect-filter-item-status-mobile",  "value"),
    running=[Output("loading-overlay-register-consignment", "visible"), True, False],
)
def refresh_consignment_table(n_desktop, n_mobile, signal, pathname, types_d, status_d, types_m, status_m):
    """Re-fetch consignment rows whenever the table is manually refreshed,
    a signal fires, or the user navigates to this page.
    """
    has_trigger = any(v is not None for v in [n_desktop, n_mobile, signal])
    if not has_trigger and pathname != "/":
        return no_update

    # Prefer desktop filter values; fall back to mobile
    types  = types_d  or types_m  or consignment_type_options
    status = status_d or status_m or status_type_options

    return run_query_from_sql(
        "get_all_consignments.sql",
        sel_types=f"('{tuplejoiner.join(types)}')",
        sel_status=f"('{tuplejoiner.join(status)}')",
    )


# ── Open "Add Consignment" modal ──────────────────────────────────────────────
@callback(
    Output("modal-register-consignment", "opened"),
    Output("autocomplete-racket-shape",        "data"),
    Output("autocomplete-racket-facematerial", "data"),
    Output("autocomplete-racket-corematerial", "data"),
    Output("autocomplete-owner-whatsapp",      "data"),
    Output("autocomplete-owner-location",      "data"),
    Input("button-add-consignment-desktop", "n_clicks"),
    Input("button-add-consignment-mobile",  "n_clicks"),
    prevent_initial_call=True,
    running=[Output("loading-overlay-register-consignment", "visible"), True, False],
)
def open_register_modal(n_desktop, n_mobile):
    """Load dropdown options fresh from the DB and open the registration modal."""
    if n_desktop or n_mobile:
        shape_opts   = list(set([d.get("shape_name")    for d in run_query_from_sql("get_all_shapes.sql")                             if d.get("shape_name")]))
        face_opts    = list(set([d.get("contact_wa")    for d in run_query_from_sql("get_specific_materials.sql", material_type="FACE") if d.get("contact_wa")]))
        core_opts    = list(set([d.get("contact_wa")    for d in run_query_from_sql("get_specific_materials.sql", material_type="CORE") if d.get("contact_wa")]))
        contact_was  = list(set([d.get("contact_wa")    for d in run_query_from_sql("get_all_contacts.sql")                            if d.get("contact_wa")]))
        contact_locs = list(set([d.get("contact_location") for d in run_query_from_sql("get_distinct_locations.sql")                  if d.get("contact_location")]))
        return True, shape_opts, face_opts, core_opts, contact_was, contact_locs
    return no_update, no_update, no_update, no_update, no_update, no_update


# ── Show/hide item-type-specific input sections ───────────────────────────────
@callback(
    Output("div-input-racket-consignment",  "hidden"),
    Output("div-input-others-consignment",  "hidden"),
    Output("div-input-shirt-size",          "hidden"),
    Output("div-input-shoes-size",          "hidden"),
    Output("div-input-others-description",  "hidden"),
    Input("select-new-consignment-type", "value"),
    Input("autocomplete-item-brand",     "value"),
    Input("autocomplete-item-name",      "value"),
)
def adjust_consignment_input_div(selected_type, selected_brand, selected_item):
    """Show only the relevant detail inputs for the chosen consignment type."""
    if selected_brand and selected_item:
        if selected_type == "Racket":
            # show racket section; hide all others
            return False, True, True, True, True
        elif selected_type == "Shirt":
            return True, False, False, True, True
        elif selected_type == "Shoes":
            return True, False, True, False, True
        elif selected_type in ("Others", "Bag"):
            return True, False, True, True, False
    # Hide everything when brand / name are blank
    return True, True, True, True, True


@callback(
    Output("div-input-owners-new", "hidden"),
    Input("textinput-owner-whatsapp", "value"),
    State("textinput-owner-whatsapp", "data"),
)
def adjust_owner_input_div(value, data):
    """Hide new-owner fields when the WA number already exists in the DB."""
    if not value:
        return True
    return value in data


@callback(
    Output("div-input-item-rating", "hidden"),
    Input("switch-old-racket", "checked"),
)
def adjust_item_rating_input_div(is_old):
    """Show the rating field only when the item is marked as used (old)."""
    return not is_old


# ── Dynamic autocomplete options ──────────────────────────────────────────────
@callback(
    Output("autocomplete-item-brand", "data"),
    Input("select-new-consignment-type", "value"),
    running=[Output("autocomplete-item-brand", "disabled"), True, False],
)
def get_brand_options(_):
    """Reload brand options whenever the consignment type changes."""
    return [d.get("brand_name") for d in run_query_from_sql("get_all_brands.sql")]


@callback(
    Output("autocomplete-item-name", "data"),
    Input("select-new-consignment-type", "value"),
    Input("autocomplete-item-brand",     "value"),
    running=[Output("autocomplete-item-name", "disabled"), True, False],
)
def get_item_options(item_type, brand_name):
    """Reload item-name options when the brand or type changes."""
    if not item_type or not brand_name:
        return no_update
    return list(set(
        [
            d.get("item_name")
            for d in run_query_from_sql("get_all_items.sql", item_type=item_type, brand_name=brand_name)
        ]
    ))


@callback(
    Output("switch-racket-women",          "checked"),
    Output("autocomplete-racket-shape",    "value"),
    Output("autocomplete-racket-facematerial", "value"),
    Output("autocomplete-racket-corematerial", "value"),
    Output("tagsinput-racket-additionalspec",  "value"),
    Output("textinput-racket-weight",      "value"),
    State("autocomplete-item-brand",       "value"),
    Input("autocomplete-item-name",        "value"),
    State("autocomplete-item-name",        "data"),
    State("select-new-consignment-type",   "value"),
    running=[
        (Output("switch-racket-women",          "disabled"), True, False),
        (Output("autocomplete-racket-shape",    "disabled"), True, False),
        (Output("autocomplete-racket-facematerial", "disabled"), True, False),
        (Output("autocomplete-racket-corematerial", "disabled"), True, False),
        (Output("tagsinput-racket-additionalspec",  "disabled"), True, False),
        (Output("textinput-racket-weight",      "disabled"), True, False),
    ],
)
def get_racket_information(brand_name, item_name, item_opts, item_type):
    """Pre-fill racket spec fields when a known racket is selected."""
    if item_type != "Racket" or item_name not in item_opts:
        return no_update
    data = run_query_from_sql(
        "get_specific_item.sql",
        item_type=item_type,
        brand_name=brand_name,
        item_name=item_name,
    )[0]
    return (
        data.get("is_racket_woman"),
        data.get("shape_name"),
        data.get("face_material"),
        data.get("core_material"),
        ast.literal_eval(data.get("racket_additional_spec")) if data.get("racket_additional_spec") else [],
        data.get("racket_weight"),
    )


@callback(
    Output("textinput-owner-name",       "value"),
    Output("autocomplete-owner-location","value"),
    Input("autocomplete-owner-whatsapp", "value"),
    Input("autocomplete-owner-whatsapp", "data"),
    prevent_initial_call=True,
    running=[
        (Output("textinput-owner-name",        "disabled"), True, False),
        (Output("autocomplete-owner-location", "disabled"), True, False),
    ],
)
def get_owner_details(owner_wa, owner_wa_opts):
    """Auto-fill owner name and location when a known WA number is entered."""
    if not owner_wa_opts or owner_wa not in owner_wa_opts:
        return no_update, no_update
    data = run_query_from_sql("get_specific_contact.sql", contact_wa=owner_wa)[0]
    return data.get("contact_name"), data.get("contact_location")


# ── Validate required fields before enabling the submit button ────────────────
@callback(
    Output("button-register-consignment", "disabled"),
    Input("select-new-consignment-type",      "value"),
    Input("autocomplete-item-brand",          "value"),
    Input("autocomplete-item-name",           "value"),
    Input("autocomplete-racket-shape",        "value"),
    Input("autocomplete-racket-facematerial", "value"),
    Input("autocomplete-racket-corematerial", "value"),
    Input("textinput-racket-weight",          "value"),
    Input("textinput-shoe-size",              "value"),
    Input("textinput-shirt-size",             "value"),
    Input("textarea-others-description",      "value"),
    Input("autocomplete-owner-whatsapp",      "value"),
    Input("textinput-owner-name",             "value"),
    Input("autocomplete-owner-location",      "value"),
    Input("numberinput-rating",               "value"),
    Input("numberinput-price-modal",          "value"),
    Input("numberinput-price-posted",         "value"),
)
def check_inputs(consignment_type, brand, name, shape, face, core, weight, shoe, shirt, others, *args):
    """Disable the submit button if any required field for the selected type is empty."""
    if consignment_type == "Racket":
        return check_any_input_is_empty([brand, name, shape, face, core, weight, list(args)])
    elif consignment_type == "Shirt":
        return check_any_input_is_empty([brand, name, shirt, list(args)])
    elif consignment_type == "Shoes":
        return check_any_input_is_empty([brand, name, shoe,  list(args)])
    elif consignment_type in ("Others", "Bag"):
        return check_any_input_is_empty([brand, name, others, list(args)])
    return True


# ── Submit: Add new consignment ───────────────────────────────────────────────
@callback(
    Output("modal-register-consignment",        "opened",           allow_duplicate=True),
    Output("consignment-notification",          "sendNotifications",allow_duplicate=True),
    Output("signal-to-refresh-consignment-table","data",            allow_duplicate=True),
    Output("select-new-consignment-type",       "value",            allow_duplicate=True),
    Output("autocomplete-item-brand",           "value",            allow_duplicate=True),
    Output("autocomplete-item-name",            "value",            allow_duplicate=True),
    Output("switch-racket-women",               "checked",          allow_duplicate=True),
    Output("autocomplete-racket-shape",         "value",            allow_duplicate=True),
    Output("autocomplete-racket-facematerial",  "value",            allow_duplicate=True),
    Output("autocomplete-racket-corematerial",  "value",            allow_duplicate=True),
    Output("textinput-racket-weight",           "value",            allow_duplicate=True),
    Output("tagsinput-racket-additionalspec",   "value",            allow_duplicate=True),
    Output("textinput-shoe-size",               "value",            allow_duplicate=True),
    Output("textinput-shirt-size",              "value",            allow_duplicate=True),
    Output("textarea-others-description",       "value",            allow_duplicate=True),
    Output("autocomplete-owner-whatsapp",       "value",            allow_duplicate=True),
    Output("autocomplete-owner-location",       "value",            allow_duplicate=True),
    Output("textinput-owner-name",              "value",            allow_duplicate=True),
    Output("numberinput-rating",                "value",            allow_duplicate=True),
    Output("numberinput-price-modal",           "value",            allow_duplicate=True),
    Output("numberinput-price-posted",          "value",            allow_duplicate=True),
    Output("textarea-extranote",                "value",            allow_duplicate=True),
    Output("switch-old-racket",                 "checked",          allow_duplicate=True),
    Input("button-register-consignment", "n_clicks"),
    State("select-new-consignment-type",        "value"),
    State("autocomplete-item-brand",            "data"),
    State("autocomplete-item-brand",            "value"),
    State("autocomplete-item-name",             "data"),
    State("autocomplete-item-name",             "value"),
    State("switch-racket-women",                "checked"),
    State("autocomplete-racket-shape",          "data"),
    State("autocomplete-racket-shape",          "value"),
    State("autocomplete-racket-facematerial",   "data"),
    State("autocomplete-racket-facematerial",   "value"),
    State("autocomplete-racket-corematerial",   "data"),
    State("autocomplete-racket-corematerial",   "value"),
    State("textinput-racket-weight",            "value"),
    State("tagsinput-racket-additionalspec",     "value"),
    State("textinput-shoe-size",                "value"),
    State("textinput-shirt-size",               "value"),
    State("textarea-others-description",        "value"),
    State("autocomplete-owner-whatsapp",        "data"),
    State("autocomplete-owner-whatsapp",        "value"),
    State("autocomplete-owner-location",        "value"),
    State("textinput-owner-name",               "value"),
    State("numberinput-rating",                 "value"),
    State("numberinput-price-modal",            "value"),
    State("numberinput-price-posted",           "value"),
    State("textarea-extranote",                 "value"),
    State("switch-old-racket",                  "checked"),
    prevent_initial_call=True,
)
def add_new_consignment(
    n_click, consignment_type,
    brand_data, brand, item_data, name,
    is_racket_w,
    shape_data, shape, face_data, face, core_data, core, weight, additional_spec,
    shoe, shirt, others,
    owner_wa_data, owner_wa, owner_location, owner_name,
    item_rating, price_modal, price_posted, extranote, is_old,
):
    """Persist a new consignment (and any new brand / item / contact) to the DB,
    then reset all form fields and trigger a table refresh.
    """
    if not n_click:
        return no_update

    # ── Upsert brand ──────────────────────────────────────────────────────────
    if brand not in brand_data:
        run_query_from_sql("insert_new_brand.sql", brand_name=brand.upper())

    # ── Upsert item / racket ──────────────────────────────────────────────────
    additional_spec_str = str(additional_spec).replace("'", '"')

    if consignment_type == "Racket":
        if name not in item_data:
            # Insert any new shape / materials before the racket itself
            if shape not in shape_data:
                run_query_from_sql("insert_new_racket_shape.sql",    shape_name=shape.upper())
            if face  not in face_data:
                run_query_from_sql("insert_new_racket_material.sql", material_type="FACE", material_name=face.upper())
            if core  not in core_data:
                run_query_from_sql("insert_new_racket_material.sql", material_type="CORE", material_name=core.upper())
            run_query_from_sql(
                "insert_new_racket.sql",
                item_type=consignment_type, brand_name=brand.upper(), item_name=name.upper(),
                is_racket_woman=1 if is_racket_w else 0,
                racket_shape=shape.upper(), racket_face_material=face.upper(),
                racket_core_material=core.upper(), racket_weight=weight,
                racket_additional_spec=additional_spec_str,
            )
        else:
            # Update existing racket specs in case they've changed
            run_query_from_sql(
                "update_racket.sql",
                item_type=consignment_type, brand_name=brand.upper(), item_name=name.upper(),
                is_racket_woman=1 if is_racket_w else 0,
                racket_shape=shape.upper(), racket_face_material=face.upper(),
                racket_core_material=core.upper(), racket_weight=weight,
                racket_additional_spec=additional_spec_str,
            )
    elif name not in item_data:
        run_query_from_sql("insert_new_item.sql", item_type=consignment_type, brand_name=brand.upper(), item_name=name.upper())

    # ── Upsert owner contact ──────────────────────────────────────────────────
    if owner_wa not in owner_wa_data:
        run_query_from_sql(
            "insert_new_contact.sql",
            contact_name=owner_name.upper(),
            contact_wa=owner_wa,
            contact_location=owner_location.upper(),
        )
    else:
        run_query_from_sql(
            "update_contact.sql",
            contact_name=owner_name.upper(),
            contact_wa=owner_wa,
            contact_location=owner_location.upper(),
        )

    # ── Build SQL-safe nullable fields ───────────────────────────────────────
    weight_sql    = f"'{weight}'"  if weight    else "null"
    extranote_sql = f"'{extranote}'" if extranote else "null"
    item_rating   = item_rating    if is_old    else 10   # new items always rate 10

    if consignment_type == "Racket":
        extra_description = f"'{','.join(additional_spec)}'" if additional_spec else "null"
    elif consignment_type == "Shirt":
        extra_description = f"'{shirt}'" if shirt  else "null"
    elif consignment_type == "Shoes":
        extra_description = f"'{shoe}'"  if shoe   else "null"
    elif consignment_type in ("Others", "Bag"):
        extra_description = f"'{others}'" if others else "null"
    else:
        extra_description = "null"

    # ── Insert consignment row ────────────────────────────────────────────────
    run_query_from_sql(
        "insert_new_consignment.sql",
        item_type=consignment_type,
        item_name=f"{brand.upper()}-{name.upper()}",
        seller_wa=owner_wa,
        item_rating=item_rating,
        price_modal=price_modal,
        price_posted=price_posted,
        extra_note=extranote_sql,
        racket_weight=weight_sql,
        extra_description=extra_description,
        item_condition="Used" if is_old else "New",
    )

    # Return tuple: (close modal, notification, refresh signal, reset all fields…)
    return (
        False,  # close modal
        [dict(
            title="Consignment berhasil ditambahkan",
            id="show-notify",
            action="show",
            message="Data Consignment telah berhasil ditambah, mohon refresh data.",
            icon=DashIconify(icon="fluent-mdl2:completed-solid"),
        )],
        str(datetime.now()),    # trigger table refresh
        None,   # select-new-consignment-type
        "",     # autocomplete-item-brand
        "",     # autocomplete-item-name
        False,  # switch-racket-women
        "",     # autocomplete-racket-shape
        "",     # autocomplete-racket-facematerial
        "",     # autocomplete-racket-corematerial
        "",     # textinput-racket-weight
        [],     # tagsinput-racket-additionalspec (must be list)
        "",     # textinput-shoe-size
        "",     # textinput-shirt-size
        "",     # textarea-others-description
        "",     # autocomplete-owner-whatsapp
        "",     # autocomplete-owner-location
        "",     # textinput-owner-name
        None,   # numberinput-rating
        None,   # numberinput-price-modal
        None,   # numberinput-price-posted
        "",     # textarea-extranote
        False,  # switch-old-racket
    )


# ── Enable/disable status buttons based on selected rows ─────────────────────
@callback(
    Output("button-mark-posted-consignment-mobile",    "disabled"),
    Output("button-mark-sold-consignment-mobile",      "disabled"),
    Output("button-mark-shipped-consignment-mobile",   "disabled"),
    Output("button-mark-completed-consignment-mobile", "disabled"),
    Output("button-mark-posted-consignment-desktop",   "disabled"),
    Output("button-mark-sold-consignment-desktop",     "disabled"),
    Output("button-mark-shipped-consignment-desktop",  "disabled"),
    Output("button-mark-completed-consignment-desktop","disabled"),
    Input("aggrid-consignment-table", "selectedRows"),
)
def set_disabled_when_selecting_multiple_rows(selected_rows):
    """Disable action buttons when no rows are selected or statuses are mixed."""
    if not selected_rows:
        return (True,) * 8

    statuses = {rd.get("status") for rd in selected_rows}
    if len(statuses) > 1:
        # Mixed statuses — all buttons disabled
        return (True,) * 8

    status = statuses.pop()
    is_posted_disabled    = status != "New"      or len(selected_rows) < 1
    is_sold_disabled      = status != "Posted"   or len(selected_rows) != 1  # sold = single item only
    is_shipped_disabled   = status != "Sold"     or len(selected_rows) < 1
    is_completed_disabled = status != "Shipped"  or len(selected_rows) < 1

    result = (is_posted_disabled, is_sold_disabled, is_shipped_disabled, is_completed_disabled)
    return result + result  # same values for mobile + desktop


# ── Posted modal: open + generate IG caption ─────────────────────────────────
@callback(
    Output("modal-mark-posted-consignment", "opened",  allow_duplicate=True),
    Output("textarea-caption-ig-posted-consignment",   "value"),
    Output("copy-caption-ig-posted-consignment",       "value"),
    Input("button-mark-posted-consignment-desktop",    "n_clicks"),
    Input("button-mark-posted-consignment-mobile",     "n_clicks"),
    State("aggrid-consignment-table", "selectedRows"),
    prevent_initial_call=True,
)
def open_modal_mark_posted(n_desktop, n_mobile, selrows):
    """Build an Instagram caption from selected consignment rows and open the modal."""
    if not (n_desktop or n_mobile):
        return no_update, no_update, no_update

    consignments = sorted(selrows, key=lambda x: x["consignment_id"])
    caption_blocks = []

    for cons in consignments:
        brand_part = cons.get("item_name").split("-")[0]
        name_part  = "-".join(cons.get("item_name").split("-")[1:])

        item_details = run_query_from_sql(
            "get_specific_item.sql",
            item_type=cons.get("item_type"),
            brand_name=brand_part,
            item_name=name_part,
        )[0]

        lines = [f"PP{cons.get('consignment_id')} {name_part}"]

        if cons.get("item_type") == "Racket":
            if item_details.get("shape_name"):
                lines.append(f"Shape: {item_details.get('shape_name')}")
            if item_details.get("racket_weight"):
                lines.append(f"Weight: {item_details.get('racket_weight')}")
            if item_details.get("core_material"):
                lines.append(f"Core: {item_details.get('core_material')}")
            if item_details.get("face_material"):
                lines.append(f"Face: {item_details.get('face_material')}")
        elif cons.get("item_type") in ("Shirt", "Shoes") and cons.get("extra_description"):
            lines.append(f"Size: {cons.get('extra_description')}")
        elif cons.get("item_type") in ("Others", "Bag") and cons.get("extra_description"):
            lines.append(f"Description: {cons.get('extra_description')}")

        # Condition line
        if cons.get("item_condition") == "New":
            lines.append("Condition: New")
        else:
            lines.append(f"Condition: Used ({cons.get('item_rating')} / 10)")

        lines.append(f"💵 Rp. {cons.get('price_posted', 0):,} 💵")
        if cons.get("seller_location"):
            lines.append(f"Location: {cons.get('seller_location').title()}")

        if cons.get("extra_note"):
            lines.append(f"Note: {cons.get('extra_note')}")

        caption_blocks.append("\n".join(lines))

    caption = "\n\n".join(caption_blocks)
    return True, caption, caption


@callback(
    Output("consignment-notification", "sendNotifications", allow_duplicate=True),
    Input("copy-caption-ig-posted-consignment", "n_clicks"),
    prevent_initial_call=True,
)
def show_notification_copy_caption(n_clicks):
    """Show a toast notification after the IG caption is copied."""
    if n_clicks:
        return [dict(
            title="Caption berhasil disalin",
            id="show-notify",
            action="show",
            message="Caption IG untuk consignment yang diposting telah berhasil disalin, silahkan paste di aplikasi lain untuk digunakan.",
            icon=DashIconify(icon="fluent-mdl2:completed-solid"),
        )]
    return no_update


# Clientside copy-to-clipboard (avoids a server round-trip)
clientside_callback(
    """
    function(n_clicks, caption_value) {
        if (n_clicks && caption_value) {
            var el = document.getElementById("textarea-caption-ig-posted-consignment");
            el.select();
            document.execCommand("copy");
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("copy-caption-ig-posted-consignment", "disabled"),
    Input("copy-caption-ig-posted-consignment",  "n_clicks"),
    State("textarea-caption-ig-posted-consignment", "value"),
    prevent_initial_call=True,
)


@callback(
    Output("modal-mark-posted-consignment", "opened",           allow_duplicate=True),
    Output("consignment-notification",      "sendNotifications",allow_duplicate=True),
    Output("signal-to-refresh-consignment-table", "data",       allow_duplicate=True),
    Output("textinput-ig-link-posted-consignment","value",      allow_duplicate=True),
    Input("button-confirm-mark-posted-consignment", "n_clicks"),
    State("aggrid-consignment-table",               "selectedRows"),
    State("textinput-ig-link-posted-consignment",   "value"),
    prevent_initial_call=True,
)
def close_modal_mark_posted(n_confirm, selrows, link_ig):
    """Save the IG link and update selected consignments to 'Posted'."""
    if n_confirm:
        cons_ids = "','".join(str(rd.get("consignment_id")) for rd in selrows) if selrows else ""
        run_query_from_sql(
            "update_consignment_posted.sql",
            consignment_ids=cons_ids,
            link_ig=link_ig,
            consignment_date=str(datetime.now().date()),
        )
        return False, [dict(
            title="Consignment berhasil diupdate",
            id="show-notify",
            action="show",
            message="Data Consignment telah berhasil diupdate menjadi posted, mohon refresh data.",
            icon=DashIconify(icon="fluent-mdl2:completed-solid"),
        )], str(datetime.now()), ""
    return True, no_update, no_update, no_update


@callback(
    Output("button-confirm-mark-posted-consignment", "disabled"),
    Input("textinput-ig-link-posted-consignment",    "value"),
)
def check_mark_posted_input(link_ig):
    """Keep the Posted submit button disabled until a valid IG link is entered."""
    return not bool(link_ig and link_ig.strip())


# ── Sold modal ────────────────────────────────────────────────────────────────
@callback(
    Output("modal-mark-sold-consignment",              "opened",  allow_duplicate=True),
    Output("text-consignment-to-sold",                 "children"),
    Output("autocomplete-buyer-whatsapp",              "data"),
    Output("autocomplete-buyer-location",              "data"),
    Output("autocomplete-sales-name-mark-sold-consignment", "data"),
    Input("button-mark-sold-consignment-desktop",      "n_clicks"),
    Input("button-mark-sold-consignment-mobile",       "n_clicks"),
    State("aggrid-consignment-table",                  "selectedRows"),
    prevent_initial_call=True,
)
def open_modal_mark_sold(n_desktop, n_mobile, selrows):
    """Load buyer/sales options and display consignment summary, then open modal."""
    if not (n_desktop or n_mobile) or not selrows:
        return no_update, no_update, no_update, no_update, no_update

    contact_was = list(set([d.get("contact_wa")       for d in run_query_from_sql("get_all_contacts.sql")]))
    contact_locs = list(set([d.get("contact_location") for d in run_query_from_sql("get_distinct_locations.sql")]))
    all_sales    = list(set([d.get("sales_name")       for d in run_query_from_sql("get_sales_name.sql")]))
    row = selrows[0]

    summary = [
        dmc.Text(["Mengupdate consignment ", dmc.Text(f'PP{row.get("consignment_id")} ', fw="bold", span=True), " dengan data sebagai berikut:"]),
        dmc.Text([dmc.Text("Barang Consignment: ", fw="bold", span=True), f'{row.get("item_type").upper()} - {row.get("item_name")}']),
        dmc.Text([dmc.Text("Owner: ",              fw="bold", span=True), f'{row.get("seller_name")} ({row.get("seller_location")}) | ({row.get("seller_wa")})']),
        dmc.Text([dmc.Text("Harga dari Owner: ",   fw="bold", span=True), dmc.NumberFormatter(value=row.get("price_modal"), thousandSeparator=",", prefix="Rp. ")]),
        dmc.Text([dmc.Text("Harga di post di IG: ",fw="bold", span=True), dmc.NumberFormatter(value=row.get("price_posted"), thousandSeparator=",", prefix="Rp. ")]),
    ]
    return True, summary, contact_was, contact_locs, all_sales


@callback(
    Output("textinput-buyer-name",       "value"),
    Output("autocomplete-buyer-location","value"),
    Input("autocomplete-buyer-whatsapp", "value"),
    Input("autocomplete-buyer-whatsapp", "data"),
    prevent_initial_call=True,
    running=[
        (Output("textinput-buyer-name",        "disabled"), True, False),
        (Output("autocomplete-buyer-location", "disabled"), True, False),
    ],
)
def get_buyer_details(buyer_wa, buyer_wa_opts):
    """Auto-fill buyer name and location for known WA numbers."""
    if buyer_wa not in buyer_wa_opts:
        return no_update, no_update
    data = run_query_from_sql("get_specific_contact.sql", contact_wa=buyer_wa)[0]
    return data.get("contact_name"), data.get("contact_location")


@callback(
    Output("div-input-mark-sold-consignment", "hidden"),
    Input("switch-consignment-sold-in-pasarpadel", "checked"),
)
def adjust_mark_sold_input_div(is_checked):
    """Hide buyer/sales fields when the item sold outside Pasar Padel."""
    return not is_checked


@callback(
    Output("button-confirm-mark-sold-consignment", "disabled"),
    Input("switch-consignment-sold-in-pasarpadel",          "checked"),
    Input("autocomplete-sales-name-mark-sold-consignment",  "value"),
    Input("autocomplete-buyer-whatsapp",                    "value"),
    Input("textinput-buyer-name",                           "value"),
    Input("autocomplete-buyer-location",                    "value"),
    Input("numberinput-price-sold",                         "value"),
)
def check_mark_sold_inputs(is_checked, sales_name, buyer_wa, buyer_name, buyer_location, price_sold):
    """Disable submit until all required sold-in-PasarPadel fields are filled."""
    if is_checked:
        return not all([sales_name, buyer_wa, buyer_name, buyer_location, price_sold])
    return False  # sold elsewhere — no fields required


@callback(
    Output("modal-mark-sold-consignment",              "opened",           allow_duplicate=True),
    Output("consignment-notification",                 "sendNotifications",allow_duplicate=True),
    Output("signal-to-refresh-consignment-table",      "data",             allow_duplicate=True),
    Output("switch-consignment-sold-in-pasarpadel",    "checked",          allow_duplicate=True),
    Output("autocomplete-sales-name-mark-sold-consignment","value",        allow_duplicate=True),
    Output("autocomplete-buyer-whatsapp",              "value",            allow_duplicate=True),
    Output("textinput-buyer-name",                     "value",            allow_duplicate=True),
    Output("autocomplete-buyer-location",              "value",            allow_duplicate=True),
    Input("button-confirm-mark-sold-consignment",      "n_clicks"),
    State("aggrid-consignment-table",                  "selectedRows"),
    State("switch-consignment-sold-in-pasarpadel",     "checked"),
    State("autocomplete-sales-name-mark-sold-consignment","value"),
    State("autocomplete-buyer-whatsapp",               "value"),
    State("textinput-buyer-name",                      "value"),
    State("autocomplete-buyer-location",               "value"),
    State("numberinput-price-sold",                    "value"),
    State("autocomplete-buyer-whatsapp",               "data"),
    prevent_initial_call=True,
)
def close_modal_mark_sold(n_confirm, selrows, is_checked, sales_name, buyer_wa, buyer_name, buyer_location, price_sold, buyer_wa_data):
    """Upsert buyer contact and update consignment status to Sold or Completed Elsewhere."""
    if not n_confirm:
        return (True, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update)

    row     = selrows[0] if selrows else None
    cons_id = row.get("consignment_id") if row else None

    # Upsert buyer contact
    if buyer_wa not in buyer_wa_data:
        run_query_from_sql("insert_new_contact.sql", contact_name=buyer_name, contact_wa=buyer_wa, contact_location=buyer_location)
    else:
        run_query_from_sql("update_contact.sql",    contact_name=buyer_name, contact_wa=buyer_wa, contact_location=buyer_location)

    if is_checked:
        run_query_from_sql(
            "update_consignment_sold.sql",
            consignment_id=cons_id, sold_in_pasarpadel=1,
            sales_name=sales_name, buyer_wa=buyer_wa,
            price_sold=price_sold, sold_date=str(datetime.now().date()),
        )
    else:
        run_query_from_sql("update_consignment_sold_elsewhere.sql", consignment_id=cons_id)

    return False, [dict(
        title="Consignment berhasil diupdate",
        id="show-notify",
        action="show",
        message="Data Consignment telah berhasil diupdate menjadi sold, mohon refresh data.",
        icon=DashIconify(icon="fluent-mdl2:completed-solid"),
    )], str(datetime.now()), True, "", "", "", ""


# ── Shipped modal ─────────────────────────────────────────────────────────────
@callback(
    Output("modal-mark-shipped-consignment", "opened", allow_duplicate=True),
    Input("button-mark-shipped-consignment-desktop",   "n_clicks"),
    Input("button-mark-shipped-consignment-mobile",    "n_clicks"),
    prevent_initial_call=True,
)
def open_modal_mark_shipped(n_desktop, n_mobile):
    return True if (n_desktop or n_mobile) else False


@callback(
    Output("modal-mark-shipped-consignment",      "opened",           allow_duplicate=True),
    Output("consignment-notification",            "sendNotifications",allow_duplicate=True),
    Output("signal-to-refresh-consignment-table", "data",             allow_duplicate=True),
    Output("textinput-tracking-shipped-consignment","value",          allow_duplicate=True),
    Input("button-confirm-mark-shipped-consignment","n_clicks"),
    State("aggrid-consignment-table",              "selectedRows"),
    State("textinput-tracking-shipped-consignment","value"),
    prevent_initial_call=True,
)
def close_modal_mark_shipped(n_confirm, selrows, tracking_code):
    """Save tracking code and update selected consignments to 'Shipped'."""
    if n_confirm:
        cons_ids = "','".join(str(rd.get("consignment_id")) for rd in selrows) if selrows else ""
        run_query_from_sql("update_consignment_shipped.sql", consignment_ids=cons_ids, tracking_code=tracking_code)
        return False, [dict(
            title="Consignment berhasil diupdate",
            id="show-notify",
            action="show",
            message="Data Consignment telah berhasil diupdate menjadi shipped, mohon refresh data.",
            icon=DashIconify(icon="fluent-mdl2:completed-solid"),
        )], str(datetime.now()), ""
    return True, no_update, no_update, no_update


@callback(
    Output("button-confirm-mark-shipped-consignment", "disabled"),
    Input("textinput-tracking-shipped-consignment",   "value"),
)
def check_mark_shipped_input(tracking_code):
    return not bool(tracking_code and tracking_code.strip())


# ── Completed modal ───────────────────────────────────────────────────────────
@callback(
    Output("modal-mark-completed-consignment", "opened", allow_duplicate=True),
    Input("button-mark-completed-consignment-desktop",   "n_clicks"),
    Input("button-mark-completed-consignment-mobile",    "n_clicks"),
    prevent_initial_call=True,
)
def open_modal_mark_completed(n_desktop, n_mobile):
    return True if (n_desktop or n_mobile) else False


@callback(
    Output("modal-mark-completed-consignment",    "opened",           allow_duplicate=True),
    Output("consignment-notification",            "sendNotifications",allow_duplicate=True),
    Output("signal-to-refresh-consignment-table", "data",             allow_duplicate=True),
    Input("button-confirm-mark-completed-consignment","n_clicks"),
    State("aggrid-consignment-table",              "selectedRows"),
    prevent_initial_call=True,
)
def close_modal_mark_completed(n_confirm, selrows):
    """Update selected consignments to 'Completed'."""
    if n_confirm:
        cons_ids = "','".join(str(rd.get("consignment_id")) for rd in selrows) if selrows else ""
        run_query_from_sql("update_consignment_completed.sql", consignment_ids=cons_ids)
        return False, [dict(
            title="Consignment berhasil diupdate",
            id="show-notify",
            action="show",
            message="Data Consignment telah berhasil diupdate menjadi completed, mohon refresh data.",
            icon=DashIconify(icon="fluent-mdl2:completed-solid"),
        )], str(datetime.now())
    return True, no_update, no_update


# ── Details modal (double-click a row) ───────────────────────────────────────
@callback(
    Output("modal-consignment-details",           "opened",           allow_duplicate=True),
    Output("consignment-notification",            "sendNotifications",allow_duplicate=True),
    Output("div-consignment-detail-information",  "children"),
    Output("numberinput-price-posted-changes",    "value"),
    Output("numberinput-price-modal-changes",     "value"),
    Input("aggrid-consignment-table",             "cellDoubleClicked"),
    State("aggrid-consignment-table",             "selectedRows"),
    prevent_initial_call=True,
)
def open_details(cell_data, selrows):
    """Display full consignment details including sale/shipping info and action buttons."""
    if not selrows:
        return no_update, no_update, no_update, no_update, no_update

    if len(selrows) > 1:
        return no_update, [dict(
            title="Peringatan",
            id="show-notify",
            action="show",
            message="Silakan pilih hanya satu consignment untuk melihat detailnya.",
            icon=DashIconify(icon="ep-warning"),
        )], no_update, no_update, no_update

    row = selrows[0]

    # ── Summary block ──────────────────────────────────────────────────────
    if row.get("item_type") == "Racket":
        print(row.get("item_name"))
        racket_details = run_query_from_sql("get_specific_item.sql", item_type="Racket", brand_name=row.get("item_name").split("-")[0], item_name="-".join(row.get("item_name").split("-")[1:]))[0]
        extra_details = dmc.Text(
            [
                dmc.Text("Racket Specs:", fw="bold", span=True),
                dmc.Text([dmc.Text("- Shape: ", fw="bold", span=True), f"{racket_details.get('shape_name')}"] if racket_details.get("shape_name") else "-"),
                dmc.Text([dmc.Text("- Face Material: ", fw="bold", span=True), f"{racket_details.get('face_material')}"] if racket_details.get("face_material") else "-"),
                dmc.Text([dmc.Text("- Core Material: ", fw="bold", span=True), f"{racket_details.get('core_material')}"] if racket_details.get("core_material") else "-"),
                dmc.Text([dmc.Text("- Weight: ", fw="bold", span=True), f"{row.get('item_weight')}"] if row.get("item_weight") else "-"),
                dmc.Text([dmc.Text("- Additional Specs: ", fw="bold", span=True), f"{racket_details.get('racket_additional_spec')}"] if racket_details.get("racket_additional_spec") else "-"),
            ],
        )
    elif row.get("item_type") in ("Shirt", "Shoes"):
        extra_details = dmc.Text(
            [dmc.Text(f"Size: ", fw="bold", span=True), row.get("extra_description")] if row.get("extra_description") else []
        )
    elif row.get("item_type") in ("Others", "Bag"):
        extra_details = dmc.Text(
            [dmc.Text(f"Description: ", fw="bold", span=True), row.get("extra_description")] if row.get("extra_description") else []
        )

    summary = dmc.Text(
        [
            dmc.Text(["Consignment ", dmc.Text(f'PP{row.get("consignment_id")} ', fw="bold", span=True), " dengan data sebagai berikut:"]),
            dmc.Text([dmc.Text("Barang Consignment: ", fw="bold", span=True), f'{row.get("item_type").upper()} - {row.get("item_name")}']),
            dmc.Text([dmc.Text("Kondisi Barang: ", fw="bold", span=True), f'{row.get("item_condition")} ({row.get("item_rating")}/10)' if row.get("item_condition") == "Used" else "New"]),
            extra_details,
            dmc.Text([dmc.Text("Owner: ",              fw="bold", span=True), f'{row.get("seller_name")} ({row.get("seller_location")}) | ({row.get("seller_wa")})'], mt=20),
            dmc.Text([dmc.Text("Harga dari Owner: ",   fw="bold", span=True), dmc.NumberFormatter(value=row.get("price_modal"),  thousandSeparator=",", prefix="Rp. ")]),
            dmc.Text([dmc.Text("Harga di post di IG: ",fw="bold", span=True), dmc.NumberFormatter(value=row.get("price_posted"), thousandSeparator=",", prefix="Rp. ")]),
            dmc.Text([dmc.Text("Extra Note: ", fw="bold", span=True), dmc.Text(row.get("extra_note") if row.get("extra_note") else "-")]),
        ],
        size="xs",
        mb=10,
    )

    # ── Instagram link block ───────────────────────────────────────────────
    ig_section = [
        dmc.Divider(label="Link Instagram Post", variant="dashed", my=10),
        dmc.Text(
            [
                dmc.Text("Instagram Link: ", fw="bold", span=True),
                dmc.Anchor(row.get("link_ig"), href=row.get("link_ig"), target="_blank") if row.get("link_ig") else "-",
            ],
            size="xs",
        ),
        dmc.Text([dmc.Text("Tanggal Posted: ", fw="bold", span=True), (pd_to_timestamp(row.get("consignment_date")).strftime("%d %B %Y") if row.get("consignment_date") else "-")], size="xs")
    ]

    # ── Sale info block ────────────────────────────────────────────────────
    sale_section = [
        dmc.Divider(label="Informasi Penjualan", variant="dashed", my=10),
        dmc.Text(
            [
                dmc.Text([dmc.Text("Tanggal Terjual: ", fw="bold", span=True), pd_to_timestamp(row.get("sold_date")).strftime("%d %B %Y") if row.get("sold_date") else "-"]),
                dmc.Text([dmc.Text("Pembeli: ",         fw="bold", span=True), f'{row.get("buyer_name")} ({row.get("buyer_location")}) | ({row.get("buyer_wa")})' if row.get("buyer_wa") else "-"]),
                dmc.Text([dmc.Text("Nama Sales: ",      fw="bold", span=True), row.get("sales_name") or "-"]),
                dmc.Text([dmc.Text("Harga Terjual: ",   fw="bold", span=True), dmc.NumberFormatter(value=row.get("price_sold"), thousandSeparator=",", prefix="Rp. ")]),
            ],
            size="xs",
            mb=10,
        ),
    ]

    # ── Shipping info block ────────────────────────────────────────────────
    shipping_section = [
        dmc.Divider(label="Informasi Pengiriman", variant="dashed", my=10),
        dmc.Text([dmc.Text("Tracking ID: ", fw="bold", span=True), row.get("tracking_id") or "-"], size="xs"),
    ]

    # Edit price is disabled once the item is in a post-sale status
    is_sold = row.get("status") in ("Sold", "Shipped", "Completed", "Completed Elsewhere")

    details = [
        summary,
        generate_button("button-edit-price-consignment", "Edit Harga", "Edit harga dari owner / harga yang di post di IG", "second", "typcn-edit", disabled=is_sold),
        *ig_section,
        *sale_section,
        *shipping_section,
        dmc.Grid(
            [
                dmc.GridCol(
                    generate_button(
                        "button-unsold-consignment",
                        "Batalkan Penjualan",
                        "Batalkan penjualan dan kembalikan status ke Posted",
                        "third",
                        "ic-round-cancel",
                        disabled=row.get("status") in ("New", "Posted", "Completed"),
                    ),
                    span=6,
                ),
                dmc.GridCol(
                    generate_button(
                        "button-delete-consignment",
                        "Delete Consignment",
                        "Hapus data consignment",
                        "fifth",
                        "fluent-mdl2:delete",
                        disabled=row.get("status") == "Completed",
                    ),
                    span=6,
                ),
            ],
            mt=10,
        ),
    ]

    return True, no_update, details, row.get("price_posted"), row.get("price_modal")


# ── Edit price modal ──────────────────────────────────────────────────────────
@callback(
    Output("modal-edit-price-consignment", "opened", allow_duplicate=True),
    Input("button-edit-price-consignment", "n_clicks"),
    prevent_initial_call=True,
)
def open_modal_edit_price(n_clicks):
    return True if n_clicks else False


@callback(
    Output("modal-edit-price-consignment",        "opened",           allow_duplicate=True),
    Output("consignment-notification",            "sendNotifications",allow_duplicate=True),
    Output("modal-consignment-details",           "opened",           allow_duplicate=True),
    Output("signal-to-refresh-consignment-table", "data",             allow_duplicate=True),
    Input("button-confirm-edit-price-consignment","n_clicks"),
    State("numberinput-price-posted-changes",     "value"),
    State("numberinput-price-modal-changes",      "value"),
    State("aggrid-consignment-table",             "selectedRows"),
    prevent_initial_call=True,
)
def close_modal_edit_price(n_confirm, price_posted, price_modal, selrows):
    """Save updated prices and close both the price modal and the details modal."""
    if n_confirm:
        row     = selrows[0] if selrows else None
        cons_id = row.get("consignment_id") if row else None
        run_query_from_sql("update_consignment_price.sql", consignment_id=cons_id, price_posted=price_posted, price_modal=price_modal)
        return False, [dict(
            title="Consignment berhasil diupdate",
            id="show-notify",
            action="show",
            message="Data Consignment telah berhasil diupdate harganya, mohon refresh data.",
            icon=DashIconify(icon="fluent-mdl2:completed-solid"),
        )], False, str(datetime.now())
    return True, no_update, no_update, no_update


# ── Unsell / Delete consignment ───────────────────────────────────────────────
@callback(
    Output("modal-consignment-details",           "opened",           allow_duplicate=True),
    Output("consignment-notification",            "sendNotifications",allow_duplicate=True),
    Output("signal-to-refresh-consignment-table", "data",             allow_duplicate=True),
    Input("button-unsold-consignment",            "n_clicks"),
    State("aggrid-consignment-table",             "selectedRows"),
    prevent_initial_call=True,
)
def unsold_data(n_clicks, selrows):
    """Reverse a sale — reset the consignment status back to Posted."""
    if n_clicks:
        row     = selrows[0] if selrows else None
        cons_id = row.get("consignment_id") if row else None
        run_query_from_sql("unsold_consignment.sql", consignment_id=cons_id)
        return False, [dict(
            title="Penjualan consignment berhasil dibatalkan",
            id="show-notify",
            action="show",
            message="Data Consignment telah berhasil dibatalkan penjualannya, mohon refresh data.",
            icon=DashIconify(icon="fluent-mdl2:completed-solid"),
        )], str(datetime.now())
    return no_update, no_update, no_update


@callback(
    Output("modal-consignment-details",           "opened",           allow_duplicate=True),
    Output("consignment-notification",            "sendNotifications",allow_duplicate=True),
    Output("signal-to-refresh-consignment-table", "data",             allow_duplicate=True),
    Input("button-delete-consignment",            "n_clicks"),
    State("aggrid-consignment-table",             "selectedRows"),
    prevent_initial_call=True,
)
def delete_data(n_clicks, selrows):
    """Permanently delete the selected consignment record."""
    if n_clicks:
        row     = selrows[0] if selrows else None
        cons_id = row.get("consignment_id") if row else None
        run_query_from_sql("delete_consignment.sql", consignment_id=cons_id)
        return False, [dict(
            title="Penjualan consignment berhasil dihapus",
            id="show-notify",
            action="show",
            message="Data Consignment telah berhasil dihapus, mohon refresh data.",
            icon=DashIconify(icon="fluent-mdl2:completed-solid"),
        )], str(datetime.now())
    return no_update, no_update, no_update

# ── End of File ───────────────────────────────────────────────────────────────
