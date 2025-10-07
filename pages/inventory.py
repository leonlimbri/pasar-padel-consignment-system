from dash import register_page, callback, Output, Input, State, dcc, no_update
from connection import *
from dash_iconify import DashIconify
from .inventory_components import *
from .utils import *
import dash_mantine_components as dmc
import json

register_page(__name__, path="/inventory")
inventory_text=json.load(open("assets/texts.json")).get("inventory")

# Desktop layouts
desktop_layout=[
    dmc.Grid(
        [
            dmc.GridCol(
                [
                    dmc.Button(
                        id="button-add-racket-desktop",
                        children=inventory_text.get("button-add-racket").get("title"),
                        leftSection=DashIconify(icon=inventory_text.get("button-add-racket").get("icon")),
                        color=inventory_text.get("button-add-racket").get("color"),
                        fullWidth=True,
                        mt=20,
                    ),
                    dmc.Tooltip(
                        target="#button-add-racket-desktop",
                        label=inventory_text.get("button-add-racket").get("tooltip"),
                        color=inventory_text.get("button-add-racket").get("color"),
                        transitionProps={
                            "transition": "slide-up", 
                            "duration": 200,
                            "timingFunction": "ease"
                        },
                        position="top",
                        withArrow=True,
                    ),
                ],
                span=4
            ),
            dmc.GridCol(
                [
                    dmc.Button(
                        id="button-add-item-desktop", 
                        children=inventory_text.get("button-add-item").get("title"), 
                        leftSection=DashIconify(icon=inventory_text.get("button-add-item").get("icon")), 
                        fullWidth=True,
                        color=inventory_text.get("button-add-item").get("color"),
                        mt=20
                    ),
                    dmc.Tooltip(
                        target="#button-add-item-desktop",
                        label=inventory_text.get("button-add-item").get("tooltip"),
                        color=inventory_text.get("button-add-item").get("color"),
                        transitionProps={
                            "transition": "slide-up", 
                            "duration": 200,
                            "timingFunction": "ease"
                        },
                        position="top",
                        withArrow=True,
                    ),
                ],
                span=4
            ),
            dmc.GridCol(
                [
                    dmc.Button(
                        id="button-refresh-inventory-desktop", 
                        children=inventory_text.get("button-refresh-inventory").get("title"), 
                        leftSection=DashIconify(icon=inventory_text.get("button-refresh-inventory").get("icon")), 
                        fullWidth=True,
                        color=inventory_text.get("button-refresh-inventory").get("color"),
                        mt=20
                    ),
                    dmc.Tooltip(
                        target="#button-refresh-inventory-desktop",
                        label=inventory_text.get("button-refresh-inventory").get("tooltip"),
                        color=inventory_text.get("button-refresh-inventory").get("color"),
                        transitionProps={
                            "transition": "slide-up", 
                            "duration": 200,
                            "timingFunction": "ease"
                        },
                        position="top",
                        withArrow=True,
                    ),
                ],
                span=4
            )
        ],
        justify="space-between",
        visibleFrom="sm",
        mb=20
    )
]

layout=dmc.AppShellMain(
    [
        dcc.Interval(id="inventory-interval", interval=5000),
        dmc.NotificationContainer(id="inventory-notification"),
        dmc.Title(inventory_text.get("title")),
        dmc.Text(inventory_text.get("subtitle"), mb=10, visibleFrom="sm"),
        dmc.Text(inventory_text.get("subtitle"), mb=10, hiddenFrom="sm", size="xs"),
        *desktop_layout,

        dmc.Button(
            id="button-refresh-inventory-mobile", 
            children=inventory_text.get("button-refresh-inventory").get("title"), 
            leftSection=DashIconify(icon=inventory_text.get("button-refresh-inventory").get("icon")), 
            color=inventory_text.get("button-refresh-inventory").get("color"),
            fullWidth=True,
            hiddenFrom="sm",
            mb=20
        ),

        dmc.LoadingOverlay(
            visible=False,
            id="loading-overlay-modal-inventory",
            overlayProps={"radius": "sm", "blur": 2},
            zIndex=10
        ),

        dmc.Box(
            [
                modal_new_racket,
                modal_new_item,
                modal_racket_view,
            ]
        ),

        dmc.Box(
            [
                dmc.Button(
                    id="button-add-racket-mobile",
                    children=inventory_text.get("button-add-racket").get("title"),
                    leftSection=DashIconify(icon=inventory_text.get("button-add-racket").get("icon")),
                    color=inventory_text.get("button-add-racket").get("color"),
                    fullWidth=True,
                    hiddenFrom="sm",
                    mb=10
                ),
                tb_racket,
            ]
        ),
        
        dmc.Box(
            [
                dmc.Button(
                    id="button-add-item-mobile", 
                    children=inventory_text.get("button-add-item").get("title"), 
                    leftSection=DashIconify(icon=inventory_text.get("button-add-item").get("icon")), 
                    color=inventory_text.get("button-add-item").get("color"),
                    fullWidth=True,
                    hiddenFrom="sm",
                    mb=10
                ),
                tb_other,
            ],
            mt=15
        ),

        dmc.Divider(
            label=inventory_text.get("divider-two"), 
            labelPosition="center", 
            mt=20
        ),
    ]
)
    
@callback(
    Output("data-persistent-inventory", "data"),
    Input("url", "pathname"),
    Input("button-refresh-inventory-desktop", "n_clicks"),
    Input("button-refresh-inventory-mobile", "n_clicks"),
    State("data-persistent-inventory", "data"),
    prevent_initial_call=True,
    running=[Output("loading-overlay-modal-inventory", "visible"), True, False],
)
def refresh_data_inventory(urls, n_clicks_desktop, n_clicks_mobile, data):
    if urls=="/inventory" or n_clicks_mobile or n_clicks_desktop:
        if n_clicks_mobile or n_clicks_desktop or (urls=="/inventory" and data is None):
            header_raket, data_raket=get_data(SPREADSHEET_ID, "Data_Raket")
            rowDataRaket=[
                {head: parse_consignment(head, val) for head, val in zip(header_raket, datum)} 
                for datum in data_raket
            ]

            header_other, data_other=get_data(SPREADSHEET_ID, "Data_Others")
            rowDataOther=[
                {head: parse_consignment(head, val) for head, val in zip(header_other, datum)} 
                for datum in data_other
            ]

            return {
                "rowdata-racket": rowDataRaket, 
                "data-racket": data_raket, 
                "rowdata-item": rowDataOther, 
                "data-item": data_other
            }
        else:
            return no_update
    else:
        return no_update

@callback(
    Output("table-racket", "rowData"),
    Output("table-other", "rowData"),
    Input("url", "pathname"),
    Input("data-persistent-inventory", "data"),
    running=[Output("loading-overlay-modal-inventory", "visible"), True, False],
)
def callback_inventory(urls, data):
    if data:
        return data.get("rowdata-racket"), data.get("rowdata-item")
    else:
        return no_update, no_update

@callback(
    Output("textinput-new-racket-name", "data", allow_duplicate=True),
    Input("textinput-new-racket-brand", "value"),
    State("data-persistent-inventory", "data"),
    prevent_initial_call=True
)
def filter_racket(racket_brand, data):
    data_racket=data.get("data-racket")
    all_brands=[dat[1] for dat in data_racket]
    if racket_brand in all_brands:
        return [dat[0] for dat in data_racket if dat[1]==racket_brand]
    else:
        return [dat[0] for dat in data_racket]

@callback(
    Output("modal-new-racket", "opened"),
    Output("textinput-new-racket-brand", "data"),
    Output("textinput-new-racket-name", "data"),
    Output("textinput-new-racket-shape", "data"),
    Output("textinput-new-racket-face", "data"),
    Output("textinput-new-racket-core", "data"),
    Output("multiselect-new-racket-additionalspecs", "data"),
    Input("button-add-racket-desktop", "n_clicks"),
    Input("button-add-racket-mobile", "n_clicks"),
    State("modal-new-racket", "opened"),
    State("data-persistent-inventory", "data"),
)
def open_add_racket(n_clicks_desktop, n_clicks_mobile, modal, data):
    if n_clicks_desktop or n_clicks_mobile:
        data_racket=data.get("data-racket")
        brands=[dat[1] for dat in data_racket]
        names=[dat[0] for dat in data_racket]
        shapes=[dat[3] for dat in data_racket]
        faces=[dat[6] for dat in data_racket]
        cores=[dat[7] for dat in data_racket]
        additionalspecs=[]
        for dat in data_racket:
            additionalspecs+=dat[4].split(",")
        return not modal, list(set(brands)), list(set(names)), list(set(shapes)), list(set(faces)), list(set(cores)), list(set(additionalspecs))
    else:
        return False, [], [], [], [], [], []

@callback(
    Output("textinput-new-item-name", "data", allow_duplicate=True),
    Input("select-new-item-type", "value"),
    Input("textinput-new-item-brand", "value"),
    State("data-persistent-inventory", "data"),
    prevent_initial_call=True
)
def filter_barang(item_type, item_brand, data):
    data_racket=data.get("data-item")
    data_racket=[dat for dat in data_racket if dat[0] == item_type]
    all_brands=[dat[2] for dat in data_racket]
    if item_brand in all_brands:
        return [dat[1] for dat in data_racket if dat[2]==item_brand]
    else:
        return [dat[1] for dat in data_racket]
    
@callback(
    Output("modal-new-item", "opened"),
    Output("textinput-new-item-brand", "data"),
    Output("textinput-new-item-name", "data"),
    Input("button-add-item-desktop", "n_clicks"),
    Input("button-add-item-mobile", "n_clicks"),
    State("modal-new-item", "opened"),
    State("data-persistent-inventory", "data"),
)
def open_add_item(n_clicks_desktop, n_clicks_mobile, modal, data):
    if n_clicks_desktop or n_clicks_mobile:
        data_item=data.get("data-item")
        brands=[dat[2] for dat in data_item]
        names=[dat[1] for dat in data_item]
        return not modal, list(set(brands)), list(set(names))
    else:
        return False, [], []

@callback(
    Output("modal-racket-view", "opened"),
    Output("text-view-racket-brand-model", "children"),
    Output("switch-view-woman-racket", "checked"),
    Output("textinput-view-racket-weight", "value"),
    Output("textinput-view-racket-shape", "data"),
    Output("textinput-view-racket-shape", "value"),
    Output("textinput-view-racket-face", "data"),
    Output("textinput-view-racket-face", "value"),
    Output("textinput-view-racket-core", "data"),
    Output("textinput-view-racket-core", "value"),
    Output("multiselect-view-racket-additionalspecs", "data"),
    Output("multiselect-view-racket-additionalspecs", "value"),
    Input("table-racket", "cellDoubleClicked"),
    State("modal-racket-view", "opened"),
    State("data-persistent-inventory", "data"),
)
def open_view_racket(cell_clicked, modal, data):
    if cell_clicked:
        data_racket=data.get("data-racket")
        racket_selected=data_racket[int(cell_clicked.get("rowId"))]
        brand=racket_selected[1].upper()
        name=racket_selected[0].upper()
        woman=racket_selected[2]=="Yes"
        shape=racket_selected[3]
        face=racket_selected[6]
        core=racket_selected[7]
        weight=racket_selected[5]
        additional_spec=racket_selected[4].split(",") if racket_selected[4] else None
        detil_raket=dmc.Text(f"{brand}-{name}", fw="bold")

        shapes=[dat[3] for dat in data_racket]
        faces=[dat[6] for dat in data_racket]
        cores=[dat[7] for dat in data_racket]
        additionalspecs=[]
        for dat in data_racket:
            additionalspecs+=dat[4].split(",")

        return not modal, detil_raket, woman, weight, list(set(shapes)), shape, list(set(faces)), face, list(set(cores)), core, list(set(additionalspecs)), additional_spec
    else:
        return False, "", False, "", [], "", [], "", [], "", [], ""

@callback(
    Output("button-add-new-racket", "disabled"),
    Input("textinput-new-racket-brand", "value"),
    Input("textinput-new-racket-name", "value"),
    Input("textinput-new-racket-shape", "value"),
    Input("textinput-new-racket-face", "value"),
    Input("textinput-new-racket-core", "value"),
    State("textinput-new-racket-name", "data")
)
def disable_add_racket(brand, name, shape, face, core, name_all):
    if brand and name and shape and face and core:
        if name in name_all:
            return True
        return False
    else:
        return True
    
@callback(
    Output("modal-new-racket", "opened", allow_duplicate=True),
    Output("inventory-notification", "sendNotifications", allow_duplicate=True),
    Input("button-add-new-racket", "n_clicks"),
    State("textinput-new-racket-brand", "value"),
    State("textinput-new-racket-name", "value"),
    State("switch-new-woman-racket", "checked"),
    State("textinput-new-racket-weight", "value"),
    State("textinput-new-racket-shape", "value"),
    State("textinput-new-racket-face", "value"),
    State("textinput-new-racket-core", "value"),
    State("multiselect-new-racket-additionalspecs", "value"),
    State("modal-new-racket", "opened"),
    prevent_initial_call=True,
    running=[Output("loading-overlay-modal-inventory", "visible"), True, False]
)
def add_racket(n_clicks, brand, name, woman, weight, shape, face, core, additionalspecs, modal):
    if n_clicks:
        # Add Racket
        append_data(
            SPREADSHEET_ID,
            "Data_Raket!B3",
            [
                [name.upper(), brand.upper(), "Yes" if woman else "No", shape, ",".join(additionalspecs), weight, face, core, None]
            ]
        )
        return not modal, [
            dict(
                title="Raket berhasil ditambahkan",
                id="show-notify",
                action="show",
                message="Data Raket telah berhasil ditambah, mohon refresh data.",
                icon=DashIconify(icon="fluent-mdl2:completed-solid"),
            )
        ]
    else:
        return False, no_update
    
@callback(
    Output("button-save-view-racket", "disabled"),
    Input("textinput-view-racket-shape", "value"),
    Input("textinput-view-racket-face", "value"),
    Input("textinput-view-racket-core", "value"),
)
def disable_save_racket(shape, face, core):
    if shape and face and core:
        return False
    else:
        return True
    
@callback(
    Output("modal-racket-view", "opened", allow_duplicate=True),
    Output("inventory-notification", "sendNotifications", allow_duplicate=True),
    Input("button-save-view-racket", "n_clicks"),
    State("switch-view-woman-racket", "checked"),
    State("textinput-view-racket-weight", "value"),
    State("textinput-view-racket-shape", "value"),
    State("textinput-view-racket-face", "value"),
    State("textinput-view-racket-core", "value"),
    State("multiselect-view-racket-additionalspecs", "value"),
    State("modal-racket-view", "opened"),
    State("table-racket", "cellDoubleClicked"),
    prevent_initial_call=True,
    running=[Output("loading-overlay-modal-inventory", "visible"), True, False]
)
def save_racket(n_clicks, woman, weight, shape, face, core, additionalspecs, modal, cell_clicked):
    if n_clicks:
        # Edit Racket
        column_indexes=[3, 4, 5, 6, 7, 8]
        column_values=["Yes" if woman else "No", shape, ",".join(additionalspecs), weight, face, core]
        for col, col_val in zip(column_indexes, column_values):
            update_data(
                SPREADSHEET_ID,
                "Data_Raket",
                int(cell_clicked.get("rowId")),
                col,
                col_val
            )
        return not modal, [
            dict(
                title="Raket berhasil diedit",
                id="show-notify",
                action="show",
                message="Data Raket telah berhasil diedit, mohon refresh data.",
                icon=DashIconify(icon="fluent-mdl2:completed-solid"),
            )
        ]
    else:
        return False, no_update

@callback(
    Output("button-add-new-item", "disabled"),
    Input("select-new-item-type", "value"),
    Input("textinput-new-item-brand", "value"),
    Input("textinput-new-item-name", "value"),
    State("textinput-new-item-name", "data")
)
def disable_add_item(type, brand, name, name_all):
    if type and brand and name:
        if name in name_all:
            return True
        return False
    else:
        return True
    
@callback(
    Output("modal-new-item", "opened", allow_duplicate=True),
    Output("inventory-notification", "sendNotifications", allow_duplicate=True),
    Input("button-add-new-item", "n_clicks"),
    State("select-new-item-type", "value"),
    State("textinput-new-item-brand", "value"),
    State("textinput-new-item-name", "value"),
    State("modal-new-item", "opened"),
    prevent_initial_call=True,
    running=[Output("loading-overlay-modal-inventory", "visible"), True, False]
)
def add_item(n_clicks, type, brand, name, modal):
    if n_clicks:
        # Add Racket
        append_data(
            SPREADSHEET_ID,
            "Data_Others!B3",
            [
                [type, name, brand, None]
            ]
        )
        return not modal, [
            dict(
                title="Barang berhasil ditambahkan",
                id="show-notify",
                action="show",
                message="Data Barang telah berhasil ditambah, mohon refresh data.",
                icon=DashIconify(icon="fluent-mdl2:completed-solid"),
            )
        ]
    else:
        return False, no_update