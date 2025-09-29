from dash import register_page, callback, Output, Input, State
from connection import *
from dash_iconify import DashIconify
from .consignment_components import *
from .utils import *
import dash_mantine_components as dmc
import json

register_page(__name__, path = "/")
consignment_text = json.load(open("assets/texts.json")).get("consignments")

# Desktop layouts
desktop_layout=[
    dmc.Divider(
        label = consignment_text.get("divider-one"), 
        labelPosition = "center",
        visibleFrom = "sm"
    ),
    dmc.Grid(
        [
            dmc.GridCol(
                children = dmc.MultiSelect(
                    id = "filter-tipe-desktop", 
                    label = consignment_text.get("input-filter-tipe-barang").get("title"), 
                    data = consignment_text.get("input-filter-tipe-barang").get("option"), 
                    placeholder = "Hit Refresh after Filtering",
                    w = "100%"
                ),
                span = 3
            ),
            dmc.GridCol(
                children = dmc.MultiSelect(
                    id = "filter-status-desktop", 
                    label = consignment_text.get("input-filter-status").get("title"), 
                    data = consignment_text.get("input-filter-status").get("option"), 
                    placeholder = "Hit Refresh after Filtering",
                    w = "100%"
                ),
                span = 3
            ),
            dmc.GridCol(
                [
                    dmc.Button(
                        id = "button-register-consignment-desktop",
                        children = consignment_text.get("button-register-consignment").get("title"),
                        leftSection = DashIconify(icon = consignment_text.get("button-register-consignment").get("icon")),
                        color = consignment_text.get("button-register-consignment").get("color"),
                        fullWidth = True,
                        mt = 20,
                    ),
                    dmc.Tooltip(
                        target = "#button-register-consignment-desktop",
                        label = consignment_text.get("button-register-consignment").get("tooltip"),
                        color = consignment_text.get("button-register-consignment").get("color"),
                        transitionProps = {
                            "transition": "slide-up", 
                            "duration": 200,
                            "timingFunction": "ease"
                        },
                        position = "top",
                        withArrow = True,
                    ),
                ],
                span = 3
            ),
            dmc.GridCol(
                [
                    dmc.Button(
                        id = "button-refresh-desktop", 
                        children = consignment_text.get("button-refresh").get("title"), 
                        leftSection = DashIconify(icon = consignment_text.get("button-refresh").get("icon")), 
                        fullWidth = True,
                        color = consignment_text.get("button-refresh").get("color"),
                        mt = 20
                    ),
                    dmc.Tooltip(
                        target = "#button-refresh-desktop",
                        label = consignment_text.get("button-refresh").get("tooltip"),
                        color = consignment_text.get("button-refresh").get("color"),
                        transitionProps = {
                            "transition": "slide-up", 
                            "duration": 200,
                            "timingFunction": "ease"
                        },
                        position = "top",
                        withArrow = True,
                    ),
                ],
                span = 3
            )
        ],
        justify = "space-between",
        visibleFrom = "sm",
        mb = 20
    )
]

# Mobile layouts
mobile_layout=[
    dmc.Group(
        [
            dmc.Button(
                id = "button-register-consignment-mobile",
                children = consignment_text.get("button-register-consignment").get("title"),
                leftSection = DashIconify(icon = consignment_text.get("button-register-consignment").get("icon")),
                color = consignment_text.get("button-register-consignment").get("color"),
                fullWidth = True,
            ),
            dmc.Divider(label = consignment_text.get("divider-one"), labelPosition = "center"),
            dmc.Button(
                id = "button-refresh-mobile", 
                children = consignment_text.get("button-refresh").get("title"), 
                leftSection = DashIconify(icon = consignment_text.get("button-refresh").get("icon")), 
                color = consignment_text.get("button-refresh").get("color"),
                fullWidth = True,
            ),
            dmc.Grid(
                [
                    dmc.GridCol(
                        children = dmc.MultiSelect(
                            id = "filter-tipe-mobile", 
                            label = consignment_text.get("input-filter-tipe-barang").get("title"), 
                            data = consignment_text.get("input-filter-tipe-barang").get("option"), 
                            placeholder = "Hit Refresh after Filtering",
                            w = "43vw"
                        ),
                        span = 6
                    ),
                    dmc.GridCol(
                        children = dmc.MultiSelect(
                            id = "filter-status-mobile", 
                            label = consignment_text.get("input-filter-status").get("title"), 
                            data = consignment_text.get("input-filter-status").get("option"), 
                            placeholder = "Hit Refresh after Filtering",
                            w = "43vw"
                        ),
                        span = 6
                    ),
                ]
            ),
        ],
        justify = "center",
        hiddenFrom = "sm",
        mb = 20
    )
]

modal_register_new = dmc.Modal(
    id = "modal-register-consignment",
    size = "lg",
    title = dmc.Text("Form Consignment Baru", fw="bold"),
    children = [
        dmc.Text("Gunakan form dibawah ini untuk menginputkan data consignment baru. Setelah input data terbuat, data consignment bisa dipakai untuk pembuatan caption dan lainnya.", fz="xs"),
        dmc.Divider(mt=5, mb=5),
        dmc.Select(
            id = "tipe-consignment",
            label = "Consignment Type", 
            data = consignment_text.get("input-filter-tipe-barang").get("option"),
            withAsterisk = True,
            size="xs"
        ),
        
        # If Type is Racket
        dmc.Box(
            id = "input-racket", 
            children = [
                dmc.Select(
                    id = "item-name-racket",
                    label = "Racket's Brand and Model",
                    withAsterisk = True,
                    data = [],
                    size = "xs",
                ),

                dmc.Divider(
                    label = "Lihat dibawah untuk detail racket diatas yang telah disimpan: ", 
                    labelPosition = "center", 
                    mt = 20,
                ),
                
                ## Or actual weight
                dmc.TextInput(
                    id = "item-weight",
                    label="Actual Weight", 
                    size="xs", 
                    placeholder="###-###G",
                ),
            ],
            style = {"display": "none"}
        ),

        # If Type is other than Racket
        dmc.Select(
            id = "item-name-others",
            label = "Item's Brand and Model",
            withAsterisk = True,
            data = [],
            size = "xs",
            style = {"display": "none"}
        ),

        # If Shoe
        dmc.TextInput(
            id = "item-shoe-size",
            label="Size", 
            size="xs", 
            placeholder="Masukan ukuran sepatu dengan sizing EUR. Contoh: EUR 41 (Pastikan formatnya sama dengan contoh)",
            style = {"display": "none"}
        ),
        
        # If Shirt
        dmc.TextInput(
            id = "item-shirt-size",
            label="Size", 
            size="xs", 
            placeholder="Masukkan ukuran baju. Contoh: Small)",
            style = {"display": "none"}
        ),
        
        # If Others
        dmc.TextInput(
            id = "item-others-description",
            label="Description", 
            size="xs", 
            placeholder="Masukkan detail tambahan tentang barang kali ini.",
            style = {"display": "none"}
        ),
            # style = {"display": "none"}
    ],
)

layout = dmc.AppShellMain(
    [
        dmc.Title(consignment_text.get("title")),
        dmc.Text(consignment_text.get("subtitle"), mb = 10, visibleFrom="sm"),
        dmc.Text(consignment_text.get("subtitle"), mb = 10, hiddenFrom="sm", size = "xs"),

        *desktop_layout,
        *mobile_layout,
        modal_register_new,

        dmc.Box([
            dmc.LoadingOverlay(
                visible=False,
                id="tb-loading-overlay",
                overlayProps={"radius": "sm", "blur": 2},
                zIndex=10,
            ),
            tb_consignments,
        ]),

        dmc.Divider(
            label = consignment_text.get("divider-two"), 
            labelPosition = "center", 
            mt = 20
        ),

    ]
)

@callback(
    Output("tb_consignment", "rowData"),
    Input("button-refresh-desktop", "n_clicks"),
    Input("button-refresh-mobile", "n_clicks"),
    Input("url", "pathname"),
    State("filter-tipe-desktop", "value"),
    State("filter-status-desktop", "value"),
    State("filter-tipe-mobile", "value"),
    State("filter-status-mobile", "value"),
    running=[Output("tb-loading-overlay", "visible"), True, False]
)
def callback_consignments(n_clicks_desktop, n_clicks_mobile, urls, filter_tipe_desktop, filter_status_desktop, filter_tipe_mobile, filter_status_mobile):
    if urls or n_clicks_desktop or n_clicks_mobile:
        header, data = get_data(SPREADSHEET_ID, "Data_Consignment")
        rowData = [
            {head: parse_consignment(head, val) if i>0 else int(val[2:]) for i, (head, val) in enumerate(zip(header, datum))} 
            for datum in data
        ]

        if filter_tipe_desktop or filter_tipe_mobile:
            filter_tipe = filter_tipe_desktop if filter_tipe_desktop else filter_tipe_mobile
            rowData = [
                rowdat
                for rowdat in rowData
                if rowdat["Item Type"] in filter_tipe
            ]

        if filter_status_desktop or filter_status_mobile:
            filter_status = filter_status_desktop if filter_status_desktop else filter_status_mobile
            rowData = [
                rowdat
                for rowdat in rowData
                if rowdat["Status"] in [parse_consignment("Status", fs) for fs in filter_status]
            ]

        return rowData

@callback(
    Output("modal-register-consignment", "opened"),
    Input("button-register-consignment-desktop", "n_clicks"),
    Input("button-register-consignment-mobile", "n_clicks"),
    State("modal-register-consignment", "opened"),
)
def open_register_consignment(n_clicks_desktop, n_clicks_mobile, modal):
    if n_clicks_desktop or n_clicks_mobile:
        return not modal

@callback(
    Output("input-racket", "style"),
    Output("item-name-others", "style"),
    Output("item-shoe-size", "style"),
    Output("item-shirt-size", "style"),
    Output("item-others-description", "style"),
    Input("tipe-consignment", "value"),
)
def unhide_register_consignment(tipe_consignment):
    disp, notdisp = {"display": ""}, {"display": "none"}
    if tipe_consignment:
        if tipe_consignment == "Racket":
            return disp, notdisp, notdisp, notdisp, notdisp
        elif tipe_consignment == "Shoes":
            return notdisp, disp, disp, notdisp, notdisp
        elif tipe_consignment == "Shirt":
            return notdisp, disp, notdisp, disp, notdisp
        elif tipe_consignment == "Others":
            return notdisp, disp, notdisp, notdisp, disp
        else:
            return notdisp, disp, notdisp, notdisp, notdisp
    else:
        return notdisp, notdisp, notdisp, notdisp, notdisp


# header, data = get_data(SPREADSHEET_ID, "Data_Raket")