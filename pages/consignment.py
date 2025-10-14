from dash import register_page, callback, Output, Input, State, dcc, no_update
from connection import *
from dash_iconify import DashIconify
from .consignment_components import *
from .utils import *
import dash_mantine_components as dmc
import json, datetime

register_page(__name__, path="/")
consignment_text=json.load(open("assets/texts.json")).get("consignments")

# Desktop layouts
desktop_layout=[
    dmc.Divider(
        label=consignment_text.get("divider-one"), 
        labelPosition="center",
        visibleFrom="sm"
    ),
    dmc.Grid(
        [
            dmc.GridCol(
                children=dmc.MultiSelect(
                    id="multiselect-filter-type-desktop", 
                    label=consignment_text.get("input-filter-item-type").get("title"), 
                    data=consignment_text.get("input-filter-item-type").get("option"), 
                    placeholder=consignment_text.get("input-filter-item-type").get("placeholder"),
                    w="100%"
                ),
                span=3
            ),
            dmc.GridCol(
                children=dmc.MultiSelect(
                    id="multiselect-filter-status-desktop", 
                    label=consignment_text.get("input-filter-status").get("title"), 
                    data=consignment_text.get("input-filter-status").get("option"), 
                    placeholder=consignment_text.get("input-filter-status").get("placeholder"),
                    w="100%"
                ),
                span=3
            ),
            dmc.GridCol(
                [
                    dmc.Button(
                        id="button-register-consignment-desktop",
                        children=consignment_text.get("button-register-consignment").get("title"),
                        leftSection=DashIconify(icon=consignment_text.get("button-register-consignment").get("icon")),
                        color=consignment_text.get("button-register-consignment").get("color"),
                        fullWidth=True,
                        mt=20,
                    ),
                    dmc.Tooltip(
                        target="#button-register-consignment-desktop",
                        label=consignment_text.get("button-register-consignment").get("tooltip"),
                        color=consignment_text.get("button-register-consignment").get("color"),
                        transitionProps={
                            "transition": "slide-up", 
                            "duration": 200,
                            "timingFunction": "ease"
                        },
                        position="top",
                        withArrow=True,
                    ),
                ],
                span=3
            ),
            dmc.GridCol(
                [
                    dmc.Button(
                        id="button-refresh-desktop", 
                        children=consignment_text.get("button-refresh").get("title"), 
                        leftSection=DashIconify(icon=consignment_text.get("button-refresh").get("icon")), 
                        fullWidth=True,
                        color=consignment_text.get("button-refresh").get("color"),
                        mt=20
                    ),
                    dmc.Tooltip(
                        target="#button-refresh-desktop",
                        label=consignment_text.get("button-refresh").get("tooltip"),
                        color=consignment_text.get("button-refresh").get("color"),
                        transitionProps={
                            "transition": "slide-up", 
                            "duration": 200,
                            "timingFunction": "ease"
                        },
                        position="top",
                        withArrow=True,
                    ),
                ],
                span=3
            )
        ],
        justify="space-between",
        visibleFrom="sm",
        mb=20
    )
]

desktop_buttons=[
    dmc.Grid(
        [
            dmc.GridCol(
                [
                    dmc.Button(
                        id="button-posted-consignment-desktop",
                        children=consignment_text.get("button-posted-consignment").get("title"),
                        leftSection=DashIconify(icon=consignment_text.get("button-posted-consignment").get("icon")),
                        color=consignment_text.get("button-posted-consignment").get("color"),
                        fullWidth=True,
                        mt=20,
                    ),
                    dmc.Tooltip(
                        target="#button-posted-consignment-desktop",
                        label=consignment_text.get("button-posted-consignment").get("tooltip"),
                        color=consignment_text.get("button-posted-consignment").get("color"),
                        transitionProps={
                            "transition": "slide-up", 
                            "duration": 200,
                            "timingFunction": "ease"
                        },
                        position="top",
                        withArrow=True,
                    ),
                ],
                span=3
            ),
            dmc.GridCol(
                [
                    dmc.Button(
                        id="button-sold-consignment-desktop",
                        children=consignment_text.get("button-sold-consignment").get("title"),
                        leftSection=DashIconify(icon=consignment_text.get("button-sold-consignment").get("icon")),
                        color=consignment_text.get("button-sold-consignment").get("color"),
                        fullWidth=True,
                        mt=20,
                    ),
                    dmc.Tooltip(
                        target="#button-sold-consignment-desktop",
                        label=consignment_text.get("button-sold-consignment").get("tooltip"),
                        color=consignment_text.get("button-sold-consignment").get("color"),
                        transitionProps={
                            "transition": "slide-up", 
                            "duration": 200,
                            "timingFunction": "ease"
                        },
                        position="top",
                        withArrow=True,
                    ),
                ],
                span=3
            ),
            dmc.GridCol(
                [
                    dmc.Button(
                        id="button-shipped-consignment-desktop",
                        children=consignment_text.get("button-shipped-consignment").get("title"),
                        leftSection=DashIconify(icon=consignment_text.get("button-shipped-consignment").get("icon")),
                        color=consignment_text.get("button-shipped-consignment").get("color"),
                        fullWidth=True,
                        mt=20,
                    ),
                    dmc.Tooltip(
                        target="#button-shipped-consignment-desktop",
                        label=consignment_text.get("button-shipped-consignment").get("tooltip"),
                        color=consignment_text.get("button-shipped-consignment").get("color"),
                        transitionProps={
                            "transition": "slide-up", 
                            "duration": 200,
                            "timingFunction": "ease"
                        },
                        position="top",
                        withArrow=True,
                    ),
                ],
                span=3
            ),
            dmc.GridCol(
                [
                    dmc.Button(
                        id="button-completed-consignment-desktop",
                        children=consignment_text.get("button-completed-consignment").get("title"),
                        leftSection=DashIconify(icon=consignment_text.get("button-completed-consignment").get("icon")),
                        color=consignment_text.get("button-completed-consignment").get("color"),
                        fullWidth=True,
                        mt=20,
                    ),
                    dmc.Tooltip(
                        target="#button-completed-consignment-desktop",
                        label=consignment_text.get("button-completed-consignment").get("tooltip"),
                        color=consignment_text.get("button-completed-consignment").get("color"),
                        transitionProps={
                            "transition": "slide-up", 
                            "duration": 200,
                            "timingFunction": "ease"
                        },
                        position="top",
                        withArrow=True,
                    ),
                ],
                span=3
            ),
        ],
        justify="space-between",
        visibleFrom="sm",
        mb=20
    )
]

# Mobile layouts
mobile_layout=[
    dmc.Group(
        [
            dmc.Button(
                id="button-register-consignment-mobile",
                children=consignment_text.get("button-register-consignment").get("title"),
                leftSection=DashIconify(icon=consignment_text.get("button-register-consignment").get("icon")),
                color=consignment_text.get("button-register-consignment").get("color"),
                fullWidth=True,
            ),
            dmc.Divider(label=consignment_text.get("divider-one"), labelPosition="center"),
            dmc.Button(
                id="button-refresh-mobile", 
                children=consignment_text.get("button-refresh").get("title"), 
                leftSection=DashIconify(icon=consignment_text.get("button-refresh").get("icon")), 
                color=consignment_text.get("button-refresh").get("color"),
                fullWidth=True,
            ),
            dmc.Grid(
                [
                    dmc.GridCol(
                        children=dmc.MultiSelect(
                            id="multiselect-filter-type-mobile", 
                            label=consignment_text.get("input-filter-item-type").get("title"), 
                            data=consignment_text.get("input-filter-item-type").get("option"), 
                            placeholder=consignment_text.get("input-filter-item-type").get("placeholder"), 
                            w="43vw"
                        ),
                        span=6
                    ),
                    dmc.GridCol(
                        children=dmc.MultiSelect(
                            id="multiselect-filter-status-mobile", 
                            label=consignment_text.get("input-filter-status").get("title"), 
                            data=consignment_text.get("input-filter-status").get("option"), 
                            placeholder=consignment_text.get("input-filter-status").get("placeholder"), 
                            w="43vw"
                        ),
                        span=6
                    ),
                ]
            ),
        ],
        justify="center",
        hiddenFrom="sm",
        mb=20
    )
]

mobile_buttons=[
    dmc.Grid(
        [
            dmc.GridCol(
                dmc.Button(
                    id="button-posted-consignment-mobile",
                    children=consignment_text.get("button-posted-consignment").get("title"),
                    leftSection=DashIconify(icon=consignment_text.get("button-posted-consignment").get("icon")),
                    color=consignment_text.get("button-posted-consignment").get("color"),
                    fullWidth=True,
                    mt=20,
                ),
                span=6
            ),
            dmc.GridCol(
                dmc.Button(
                    id="button-sold-consignment-mobile",
                    children=consignment_text.get("button-sold-consignment").get("title"),
                    leftSection=DashIconify(icon=consignment_text.get("button-sold-consignment").get("icon")),
                    color=consignment_text.get("button-sold-consignment").get("color"),
                    fullWidth=True,
                    mt=20,
                ),
                span=6
            ),
        ],
        justify="space-between",
        hiddenFrom="sm",
    ),
    dmc.Grid(
        [
            dmc.GridCol(
                dmc.Button(
                    id="button-shipped-consignment-mobile",
                    children=consignment_text.get("button-shipped-consignment").get("title"),
                    leftSection=DashIconify(icon=consignment_text.get("button-shipped-consignment").get("icon")),
                    color=consignment_text.get("button-shipped-consignment").get("color"),
                    fullWidth=True,
                ),
                span=6
            ),
            dmc.GridCol(
                dmc.Button(
                    id="button-completed-consignment-mobile",
                    children=consignment_text.get("button-completed-consignment").get("title"),
                    leftSection=DashIconify(icon=consignment_text.get("button-completed-consignment").get("icon")),
                    color=consignment_text.get("button-completed-consignment").get("color"),
                    fullWidth=True,
                ),
                span=6
            ),
        ],
        justify="space-between",
        hiddenFrom="sm",
        mb=10
    )
]

layout=dmc.AppShellMain(
    [
        dmc.NotificationContainer(id="consignment-notification"),
        dmc.Title(consignment_text.get("title")),
        dmc.Text(consignment_text.get("subtitle"), mb=10, visibleFrom="sm"),
        dmc.Text(consignment_text.get("subtitle"), mb=10, hiddenFrom="sm", size="xs"),
        dcc.Store(id="data-persistent-posted"),

        *desktop_layout,
        *mobile_layout,

        dmc.Box(
            [
                dmc.LoadingOverlay(
                    visible=False,
                    id="loading-overlay-modal",
                    overlayProps={"radius": "sm", "blur": 2},
                    zIndex=210
                ),
                modal_register_new,
                modal_view_consignment,
                modal_post_consignment,
                modal_sold_consignment,
                modal_shipped_consignment,
                modal_completed_consignment,
                modal_view_consignment
            ]
        ),

        dmc.Box(
            [
                dmc.LoadingOverlay(
                    visible=False,
                    id="loading-overlay-table",
                    overlayProps={"radius": "sm", "blur": 2},
                    zIndex=10
                ),
                tb_consignments,
            ]
        ),

        *desktop_buttons,
        *mobile_buttons,

        dmc.Divider(
            label=consignment_text.get("divider-two"), 
            labelPosition="center", 
            mt=20
        ),
    ]
)

@callback(
    Output("data-persistent-data", "data"),
    Input("url", "pathname"),
    Input("button-refresh-desktop", "n_clicks"),
    Input("button-refresh-mobile", "n_clicks"),
    State("data-persistent-data", "data"),
    running=[Output("loading-overlay-table", "visible"), True, False],
)
def callback_consignments(urls, n_clicks_desktop, n_clicks_mobile, data):
    if urls=="/" or n_clicks_mobile or n_clicks_desktop:
        if n_clicks_mobile or n_clicks_desktop or (urls=="/" and data is None):
            header, data_consignment=get_data(SPREADSHEET_ID, "Data_Consignment")
            header_raket, data_raket=get_data(SPREADSHEET_ID, "Data_Raket")
            header_other, data_other=get_data(SPREADSHEET_ID, "Data_Others")

            rowData=[
                {head: parse_consignment(head, val) for i, (head, val) in enumerate(zip(header, datum))} 
                for datum in data_consignment
            ]
            
            racket={
                "list-raket": [
                    {"label": f"{dat[1].upper()}-{dat[0].upper()}", "value": str(ind)}
                    for ind, dat in enumerate(data_raket)
                ],
                "data-raket": data_raket
            }

            barang={
                "list-barang": [
                    {"label": f"{dat[2].upper()}-{dat[1].upper()}", "value": str(ind), "tipe": dat[0]}
                    for ind, dat in enumerate(data_other)
                ],
                "data-barang": data_other
            }

            return {
                "rowdata-consignment": rowData, 
                "data-raket": racket, 
                "data-barang": barang, 
                "data-consignment": data_consignment
            }
        else:
            return no_update
    else:
        return no_update
        
@callback(
    Output("table-consignment", "rowData"),
    Input("data-persistent-data", "data"),
    Input("url", "pathname"),
    running=[Output("loading-overlay-table", "visible"), True, False]
)
def callback_consignments(data, urls):
    if data:
        return data.get("rowdata-consignment")
    else:
        return no_update
    
@callback(
    Output("table-consignment", "filterModel"),
    Input("multiselect-filter-type-desktop", "value"),
    Input("multiselect-filter-status-desktop", "value"),
    Input("multiselect-filter-type-mobile", "value"),
    Input("multiselect-filter-status-mobile", "value"),
    State("table-consignment", "filterModel"),
)
def update_filter_consignment(type_desktop, status_desktop, type_mobile, status_mobile, model):
    types=type_desktop if type_desktop else type_mobile
    status=status_desktop if status_desktop else status_mobile
    
    if types:
        model["Item Type"]={
            "filterType": "text",
            "operator": "OR",
            "conditions": [
                {"filterType": "text", "type": "contains", "filter": t}
                for t in types
            ] 
        }
    else:
        model["Item Type"]={}
    if status:
        model["Status"]={
            "filterType": "text",
            "operator": "OR",
            "conditions": [
                {"filterType": "text", "type": "contains", "filter": s}
                for s in status
            ] 
        }
    else:
        model["Status"]={}

    return model

@callback(
    Output("modal-register-consignment", "opened"),
    Output("textinput-owner-whatsapp", "data"),
    Output("textinput-owner-location", "data"),
    Input("button-register-consignment-desktop", "n_clicks"),
    Input("button-register-consignment-mobile", "n_clicks"),
    State("modal-register-consignment", "opened"),
    State("data-persistent-data", "data"),
    running=[Output("loading-overlay-modal", "visible"), True, False]
)
def open_register_consignment(n_clicks_desktop, n_clicks_mobile, modal, data):
    if n_clicks_desktop or n_clicks_mobile:
        no_wa=[dat[1] for dat in data.get("data-consignment")]
        lokasi_owner=[dat[3].upper() for dat in data.get("data-consignment")]
        return not modal, list(set(no_wa)), list(set(lokasi_owner))
    else:
        return False, [], []

@callback(
    Output("inputbox-racket", "style"),
    Output("select-item-name", "style"),
    Output("textinput-shoe-size", "style"),
    Output("textinput-shirt-size", "style"),
    Output("textinput-others-description", "style"),

    Output("select-racket-name", "data"),
    Output("select-item-name", "data"),

    Input("select-consignment-type", "value"),
    State("data-persistent-data", "data"),
    running=[Output("loading-overlay-modal", "visible"), True, False]
)
def unhide_register_consignment(tipe_consignment, data):
    disp, notdisp={"display": ""}, {"display": "none"}
    if tipe_consignment:
        if tipe_consignment=="Racket":
            list_raket=data.get("data-raket").get("list-raket")
            return disp, notdisp, notdisp, notdisp, notdisp, list_raket, []
        else:
            list_barang=data.get("data-barang").get("list-barang")
            if tipe_consignment=="Shoes":
                list_sepatu=[
                    {"label": lb["label"], "value": lb["value"]}
                    for lb in list_barang if lb["tipe"]=="Shoes"
                ]
                return notdisp, disp, disp, notdisp, notdisp, [], list_sepatu
            elif tipe_consignment=="Shirt":
                list_baju=[
                    {"label": lb["label"], "value": lb["value"]}
                    for lb in list_barang if lb["tipe"]=="Shirt"
                ]
                return notdisp, disp, notdisp, disp, notdisp, [], list_baju
            elif tipe_consignment=="Bag":
                list_tas=[
                    {"label": lb["label"], "value": lb["value"]}
                    for lb in list_barang if lb["tipe"]=="Bag"
                ]
                return notdisp, disp, notdisp, notdisp, notdisp, [], list_tas
            elif tipe_consignment=="Others":
                list_lain=[
                    {"label": lb["label"], "value": lb["value"]}
                    for lb in list_barang if lb["tipe"]=="Others"
                ]
                return notdisp, disp, notdisp, notdisp, disp, [], list_lain
            else:
                return notdisp, disp, notdisp, notdisp, notdisp, [], []
    else:
        return notdisp, notdisp, notdisp, notdisp, notdisp, [], []
    
@callback(
    Output("text-racket-details", "children"),
    Output("textinput-racket-weight", "value"),
    Input("select-racket-name", "value"),
    State("select-consignment-type", "value"),
    State("data-persistent-data", "data"),
)
def detail_raket(nama_raket, tipe_consignment, data):
    if tipe_consignment=="Racket" and nama_raket:
        info_raket=data.get("data-raket").get("data-raket")[int(nama_raket)]
        childrens=[
            dmc.Box([dmc.Text("Woman's Racket: ", fw="bold"), dmc.Text(info_raket[2])]),
            dmc.Box([dmc.Text("Shape: ", fw="bold"), dmc.Text(info_raket[3])]),
            dmc.Box([dmc.Text("Face / Core Material: ", fw="bold"), dmc.Text(f"{info_raket[6]} / {info_raket[7]}")]),
            dmc.Box([dmc.Text("Additional Specifications: ", fw="bold"), dmc.Text(info_raket[4] if info_raket[4] else "None")]),
        ]
        return childrens, info_raket[5]
    else:
        return "", ""
        
@callback(
    Output("textinput-owner-name", "value"),
    Output("textinput-owner-location", "value"),
    Input("textinput-owner-whatsapp", "value"),
    State("data-persistent-data", "data"),
)
def add_new_seller(owner_wa, data):
    if data:
        no_wa=[dat[1] for dat in data.get("data-consignment")]
        if owner_wa:
            if owner_wa in no_wa:
                for dat in reversed(data.get("data-consignment")):
                    if dat[1]==owner_wa:
                        return dat[2].upper(), dat[3].upper()
            else: return "", ""
        else:
            return "", ""
    else:
        return "", ""

@callback(
    Output("numberinput-rating", "style"),
    Input("switch-old-racket", "checked")
)
def is_used(used):
    return {"display": ""} if used else {"display": "none"}

@callback(
    Output("button-add-consignment", "disabled"),
    Input("select-consignment-type", "value"),
    Input("select-racket-name", "value"),
    Input("select-item-name", "value"),
    Input("textinput-shoe-size", "value"),
    Input("textinput-shirt-size", "value"),
    Input("textinput-others-description", "value"),
    Input("textinput-owner-whatsapp", "value"),
    Input("textinput-owner-name", "value"),
    Input("textinput-owner-location", "value"),
    Input("numberinput-owner-price", "value"),
    Input("numberinput-owner-sell-price", "value"),
    Input("switch-old-racket", "checked"),
    Input("numberinput-rating", "value"),
    State("textinput-owner-whatsapp", "data"),
)
def check_add_consignment(type, racket, item, shoesize, shirtsize, othersdesc, ownerwa, ownername, ownerloc, ownerprice, sellprice, oldracket, rating, ownerwadata):
    # Check Consigned item type
    if type=="Racket":
        if oldracket:
            disable_item=False if racket and rating else True
        else:
            disable_item=False if racket else True
    elif type=="Bag":
        disable_item=False if item else True
    elif type=="Shirt":
        disable_item=False if item and shirtsize else True
    elif type=="Shoes":
        disable_item=False if item and shoesize else True
    elif type=="Others":
        disable_item=False if item and othersdesc else True
    else:
        disable_item=True
    
    # Check WA
    if ownerwa:
        if ownerwa in ownerwadata:
            disable_wa=False
        else:
            disable_wa=False if ownername and ownerloc else True
    else:
        disable_wa=True
    
    # Check Prices
    disable_prices=False if ownerprice>0 and sellprice>0 else True

    return disable_item or disable_prices or disable_wa

@callback(
    Output("modal-register-consignment", "opened", allow_duplicate=True),
    Output("consignment-notification", "sendNotifications", allow_duplicate=True),
    Input("button-add-consignment", "n_clicks"),
    State("modal-register-consignment", "opened"),
    State("select-consignment-type", "value"),
    State("select-racket-name", "value"),
    State("select-item-name", "value"),
    State("textarea-extranote", "value"),
    State("textinput-racket-weight", "value"),
    State("textinput-shoe-size", "value"),
    State("textinput-shirt-size", "value"),
    State("textinput-others-description", "value"),
    State("textinput-owner-whatsapp", "value"),
    State("textinput-owner-name", "value"),
    State("textinput-owner-location", "value"),
    State("numberinput-owner-price", "value"),
    State("numberinput-owner-sell-price", "value"),
    State("switch-old-racket", "checked"),
    State("numberinput-rating", "value"),
    State("select-racket-name", "data"),
    State("select-item-name", "data"),

    prevent_initial_call=True,
    running=[Output("loading-overlay-modal", "visible"), True, False]
)
def add_consignment(n_clicks, modal, type, racket, item, extranote, weight, shoesize, shirtsize, othersdesc, ownerwa, ownername, ownerlocation, ownerprice, sellprice, oldracket, rating, data_raket, data_item):
    if n_clicks:
        # Add Consignment
        if type=="Racket":
            descs=""
            name=data_raket[int(racket)].get("label")
        else:
            name=data_item[int(item)].get("label")
            if type=="Shoes":
                descs=shoesize
            elif type=="Shirt":
                descs=shirtsize
            elif type=="Others":
                descs=othersdesc
            elif type=="Bag":
                descs=""

        append_data(
            SPREADSHEET_ID,
            "Data_Consignment!B3",
            [
                [
                    None, ownerwa, ownername, ownerlocation, type, name, 
                    weight if type=="Racket" else "...", "Used" if oldracket else "New", rating if oldracket else 10,
                    descs, extranote, ownerprice, sellprice,
                ]
            ]
        )
        return not modal, [
            dict(
                title="Consignment berhasil ditambahkan",
                id="show-notify",
                action="show",
                message="Data Consignment telah berhasil ditambah, mohon refresh data.",
                icon=DashIconify(icon="fluent-mdl2:completed-solid"),
            )
        ]
    else:
        return False, no_update

@callback(
    Output("button-posted-consignment-desktop", "disabled"),
    Output("button-posted-consignment-mobile", "disabled"),
    Input("table-consignment", "selectedRows")
)
def disable_post(selected_consignments):
    if selected_consignments:
        for consignment in selected_consignments:
            if consignment.get("Status")!="New":
                return True, True
        return False, False
    else:
        return True, True

@callback(
    Output("modal-post-consignment", "opened"),
    Output("text-posted-consignments", "children"),
    Input("button-posted-consignment-desktop", "n_clicks"),
    Input("button-posted-consignment-mobile", "n_clicks"),
    State("table-consignment", "selectedRows"),
    State("modal-post-consignment", "opened"),
)
def open_post_consignments(n_click_desktop, n_click_mobile, consignments, modal):
    if n_click_desktop or n_click_mobile:
        consignmentids=", ".join([f"PP{con.get('ID')}" for con in consignments])
        texts=f"Mengupdate consignment dengan id {consignmentids} dengan instagram link sebagai berikut."
        return not modal, texts
    else:
        return False, ""
    
@callback(
    Output("button-submit-post-consignment", "disabled"),
    Input("textinput-posted-link", "value"),
)
def disable_submit_post_consignments(iglink):
    if iglink:
        return "instagram" not in iglink
    else:
        return True

@callback(
    Output("modal-post-consignment", "opened", allow_duplicate=True),
    Output("consignment-notification", "sendNotifications", allow_duplicate=True),
    Input("button-submit-post-consignment", "n_clicks"),
    State("textinput-posted-link", "value"),
    State("table-consignment", "rowData"),
    State("table-consignment", "selectedRows"),
    State("modal-post-consignment", "opened"),
    prevent_initial_call=True,
    running=[Output("loading-overlay-modal", "visible"), True, False]
)
def update_post_consignments(n_clicks, iglink, data, selected, modal):
    if n_clicks:
        for row in selected:
            update_data_range(
                SPREADSHEET_ID, "Data_Consignment", data.index(row),
                [14, 15], 
                [iglink, datetime.date.today().strftime("%d-%b-%Y")]
            )
        return not modal, [
            dict(
                title="Consignment berhasil di Post",
                id="show-notify",
                action="show",
                message="Data Consignment telah berhasil di edit, mohon refresh data.",
                icon=DashIconify(icon="fluent-mdl2:completed-solid"),
            )
        ]
    else:
        return False, no_update

@callback(
    Output("button-sold-consignment-desktop", "disabled"),
    Output("button-sold-consignment-mobile", "disabled"),
    Input("table-consignment", "selectedRows")
)
def disable_sold(selected_consignments):
    if selected_consignments:
        if len(selected_consignments)>1: return True, True
        for consignment in selected_consignments:
            if consignment.get("Status")!="Posted":
                return True, True
        return False, False
    else:
        return True, True

@callback(
    Output("modal-sold-consignment", "opened"),
    Output("text-sold-details", "children"),
    Output("textinput-sales-name", "data"),
    Output("textinput-buyer-whatsapp", "data"),
    Output("textinput-buyer-location", "data"),
    Input("button-sold-consignment-desktop", "n_clicks"),
    Input("button-sold-consignment-mobile", "n_clicks"),
    State("table-consignment", "rowData"),
    State("table-consignment", "selectedRows"),
    State("modal-post-consignment", "opened"),
)
def open_sold_consignments(n_click_desktop, n_click_mobile, conrowdata, consignments, modal):
    if n_click_desktop or n_click_mobile:
        con=consignments[0]
        condition=con.get("Item Condition")

        sales, nowa, location=[], [], []
        for row in conrowdata:
            nowa.append(row.get("Buyer WA"))
            sales.append(row.get("Nama Sales"))
            location.append(row.get("Seller Location"))
            location.append(row.get("Buyer Location"))

        if condition=="Used":
            condition+=f" - {con.get("Item Rating")}"
        context=[dmc.Text(f"Mengupdate consignment PP{con.get('ID')} dengan data sebagai berikut:", size="xs")]
        context.append(
            dmc.Text(
                [
                    dmc.Text("Barang Consignment: ", fw="bold", span=True),
                    dmc.Text(f"{'-'.join(con.get('Item Name').split('-')[1:])} ({condition})", span=True)
                ], size="xs"
            )
        )
        context.append(
            dmc.Text(
                [
                    dmc.Text("Owner: ", fw="bold", span=True),
                    dmc.Text(f"{con.get('Seller Name')} - {con.get('Seller Location')} ({con.get('Seller WA')})", span=True)
                ], size="xs"
            )
        )
        context.append(
            dmc.Text(
                [
                    dmc.Text("Harga dari Owner: ", fw="bold", span=True),
                    dmc.Text(f"Rp. {con.get('Price Seller'):,d}", span=True)
                ], size="xs"
            )
        )
        context.append(
            dmc.Text(
                [
                    dmc.Text("Harga di post di IG: ", fw="bold", span=True),
                    dmc.Text(f"Rp. {con.get('Price Posted'):,d}", span=True)
                ], size="xs"
            )
        )

        if con.get("Extra Note"):
            context.append(dmc.Text(con.get("Extra Note"), size="xs"))

        sales.remove("")
        nowa.remove("")
        return not modal, context, list(set(sales)), list(set(nowa)), list(set(location))
    else:
        return False, "", [], [], []

@callback(
    Output("textinput-buyer-name", "value"),
    Output("textinput-buyer-location", "value"),
    Input("textinput-buyer-whatsapp", "value"),
    State("textinput-buyer-whatsapp", "data"),
    State("table-consignment", "rowData"),
)
def check_nowa(nowa, allwa, rowdat):
    if nowa:
        if nowa in allwa:
            for rd in reversed(rowdat):
                if rd.get("Buyer WA")==nowa:
                    return rd.get("Buyer Name").upper(), rd.get("Buyer Location").upper()
            return "", ""
        else:
            return "", ""
    else:
        return "", ""

@callback(
    Output("inputbox-buyers", "style"),
    Output("numberinput-final-price", "style"),
    Input("switch-pasar-padel", "checked")
)
def is_sold_in_pasarpadel(switch):
    if switch:
        return {"display": ""}, {"display": ""}
    else:
        return {"display": "none"}, {"display": "none"}

@callback(
    Output("modal-sold-consignment", "opened", allow_duplicate=True),
    Output("consignment-notification", "sendNotifications", allow_duplicate=True),
    Input("button-submit-sold-consignment", "n_clicks"),
    State("textinput-sales-name", "value"),
    State("textinput-buyer-whatsapp", "value"),
    State("textinput-buyer-name", "value"),
    State("textinput-buyer-location", "value"),
    State("numberinput-final-price", "value"),
    State("switch-pasar-padel", "checked"),
    State("table-consignment", "rowData"),
    State("table-consignment", "selectedRows"),
    State("modal-sold-consignment", "opened"),
    prevent_initial_call=True,
    running=[Output("loading-overlay-modal", "visible"), True, False]
)
def update_sold_consignments(n_clicks, sales, buyerwa, buyername, buyerloc, finalprice, switch, data, selected, modal):
    if n_clicks:
        for row in selected:
            if switch:
                update_data_range(
                    SPREADSHEET_ID, "Data_Consignment", data.index(row),
                    [16, 21],
                    [datetime.date.today().strftime("%d-%b-%Y"), buyerwa, buyername, buyerloc, sales, finalprice]
                )
            else:
                update_data(
                    SPREADSHEET_ID, "Data_Consignment", data.index(row),
                    23,
                    "Elsewhere"
                )
        return not modal, [
            dict(
                title="Consignment Terjual",
                id="show-notify",
                action="show",
                message="Data Consignment telah berhasil di edit, mohon refresh data.",
                icon=DashIconify(icon="fluent-mdl2:completed-solid"),
            )
        ]
    else:
        return False, no_update

@callback(
    Output("button-shipped-consignment-desktop", "disabled"),
    Output("button-shipped-consignment-mobile", "disabled"),
    Input("table-consignment", "selectedRows")
)
def disable_shipped(selected_consignments):
    if selected_consignments:
        for consignment in selected_consignments:
            if consignment.get("Status")!="Sold":
                return True, True
        return False, False
    else:
        return True, True

@callback(
    Output("modal-shipped-consignment", "opened"),
    Output("text-shipped-consignments", "children"),
    Input("button-shipped-consignment-desktop", "n_clicks"),
    Input("button-shipped-consignment-mobile", "n_clicks"),
    State("table-consignment", "selectedRows"),
    State("modal-shipped-consignment", "opened"),
)
def open_shipped_consignments(n_click_desktop, n_click_mobile, consignments, modal):
    if n_click_desktop or n_click_mobile:
        consignmentids=", ".join([f"PP{con.get('ID')}" for con in consignments])
        texts=f"Mengupdate consignment dengan id {consignmentids} dengan tracking ID sebagai berikut."
        return not modal, texts
    else:
        return False, ""

@callback(
    Output("modal-shipped-consignment", "opened", allow_duplicate=True),
    Output("consignment-notification", "sendNotifications", allow_duplicate=True),
    Input("button-submit-shipped-consignment", "n_clicks"),
    State("textinput-shipped-trackingid", "value"),
    State("table-consignment", "rowData"),
    State("table-consignment", "selectedRows"),
    State("modal-shipped-consignment", "opened"),
    prevent_initial_call=True,
    running=[Output("loading-overlay-modal", "visible"), True, False]
)
def update_shipped_consignments(n_clicks, trackingid, data, selected, modal):
    if n_clicks:
        for row in selected:
            update_data(
                SPREADSHEET_ID, "Data_Consignment", data.index(row),
                22, 
                trackingid
            )
        return not modal, [
            dict(
                title="Consignment Ter-shipped",
                id="show-notify",
                action="show",
                message="Data Consignment telah berhasil di edit, mohon refresh data.",
                icon=DashIconify(icon="fluent-mdl2:completed-solid"),
            )
        ]
    else:
        return False, no_update

@callback(
    Output("button-completed-consignment-desktop", "disabled"),
    Output("button-completed-consignment-mobile", "disabled"),
    Input("table-consignment", "selectedRows")
)
def disable_complete(selected_consignments):
    if selected_consignments:
        for consignment in selected_consignments:
            if consignment.get("Status")!="Shipped":
                return True, True
        return False, False
    else:
        return True, True
    
@callback(
    Output("modal-completed-consignment", "opened"),
    Output("text-completed-consignments", "children"),
    Input("button-completed-consignment-desktop", "n_clicks"),
    Input("button-completed-consignment-mobile", "n_clicks"),
    State("table-consignment", "selectedRows"),
    State("modal-completed-consignment", "opened"),
)
def open_completed_consignments(n_click_desktop, n_click_mobile, consignments, modal):
    if n_click_desktop or n_click_mobile:
        consignmentids=", ".join([f"PP{con.get('ID')}" for con in consignments])
        texts=f"Mengupdate consignment dengan id {consignmentids} menjadi selesai, apakah anda yakin?"
        return not modal, texts
    else:
        return False, ""

@callback(
    Output("modal-completed-consignment", "opened", allow_duplicate=True),
    Output("consignment-notification", "sendNotifications", allow_duplicate=True),
    Input("button-submit-completed-consignment", "n_clicks"),
    State("table-consignment", "rowData"),
    State("table-consignment", "selectedRows"),
    State("modal-completed-consignment", "opened"),
    prevent_initial_call=True,
    running=[Output("loading-overlay-modal", "visible"), True, False]
)
def update_shipped_consignments(n_clicks, data, selected, modal):
    if n_clicks:
        for row in selected:
            update_data(
                SPREADSHEET_ID, "Data_Consignment", data.index(row),
                23, 
                "Pasar Padel"
            )
        return not modal, [
            dict(
                title="Consignment Selesai",
                id="show-notify",
                action="show",
                message="Data Consignment telah berhasil di edit, mohon refresh data.",
                icon=DashIconify(icon="fluent-mdl2:completed-solid"),
            )
        ]
    else:
        return False, no_update
    
@callback(
    Output("consignment-notification", "sendNotifications"),
    Input("button-save-price-change", "n_clicks"),
    State("numberinput-view-owner-price", "value"),
    State("numberinput-view-owner-buyer-price", "value"),
    State("table-consignment", "cellDoubleClicked"),
    running=[Output("loading-overlay-modal", "visible"), True, False]
)
def change_input(n_clicks, ownerprice, igprice, selected):
    if n_clicks:
        update_data_range(
            SPREADSHEET_ID, "Data_Consignment", int(selected.get("rowId")),
            [12, 13],
            [ownerprice, igprice]
        )
        return [
            dict(
                title="Harga Terupdate",
                id="show-notify",
                action="show",
                message="Harga telah berhasil di-update",
                icon=DashIconify(icon="fluent-mdl2:completed-solid"),
            )
        ]
    else:
        return no_update

@callback(
    Output("modal-view-consignment", "opened"),
    Output("text-view-consignment-details", "children"),
    Output("numberinput-view-owner-price", "value"),
    Output("numberinput-view-owner-price", "disabled"),
    Output("numberinput-view-owner-buyer-price", "value"),
    Output("numberinput-view-owner-buyer-price", "disabled"),
    Output("button-save-price-change", "disabled"),
    Output("text-view-iglink", "children"),
    Output("text-view-sold-details", "children"),
    Output("text-view-shipped-details", "children"),
    Input("table-consignment", "cellDoubleClicked"),
    State("table-consignment", "rowData"),
    State("modal-view-consignment", "opened"),
)
def view_consignment(cell_clicked, data, modal):
    if cell_clicked:
        data_selected=data[int(cell_clicked.get("rowId"))]
        condition=data_selected.get("Item Condition")
        if condition=="Used":
            condition+=f" - {data_selected.get("Item Rating")}"
        context=[dmc.Text(f"Consignment PP{data_selected.get('ID')} dengan data sebagai berikut:", size="xs")]
        context.append(
            dmc.Text(
                [
                    dmc.Text("Barang Consignment: ", fw="bold", span=True),
                    dmc.Text(f"{'-'.join(data_selected.get('Item Name').split('-')[1:])} ({condition})", span=True)
                ], size="xs"
            )
        )
        context.append(
            dmc.Text(
                [
                    dmc.Text("Owner: ", fw="bold", span=True),
                    dmc.Text(f"{data_selected.get('Seller Name')} - {data_selected.get('Seller Location')} ({data_selected.get('Seller WA')})", span=True)
                ], size="xs"
            )
        )
        context.append(
            dmc.Text(
                [
                    dmc.Text("Harga dari Owner: ", fw="bold", span=True),
                    dmc.Text(f"Rp. {data_selected.get('Price Seller'):,d}", span=True)
                ], size="xs"
            )
        )
        context.append(
            dmc.Text(
                [
                    dmc.Text("Harga di post di IG: ", fw="bold", span=True),
                    dmc.Text(f"Rp. {data_selected.get('Price Posted'):,d}", span=True)
                ], size="xs"
            )
        )

        if data_selected.get("Extra Note"):
            context.append(dmc.Text(data_selected.get("Extra Note"), size="xs"))

        ownerprice=int(data_selected.get("Price Seller"))
        igprice=int(data_selected.get("Price Posted"))
        iglink=[
            dmc.Text("Instagram Link: ", span=True, fw="bold"),
        ]
        if data_selected.get("IG Link"):
            iglink.append(
                dmc.Text(dcc.Link(href=data_selected.get("IG Link"), children=data_selected.get("IG Link")), span=True)
            )
        else:
            iglink.append(
                dmc.Text("N/a", span=True)
            )

        if data_selected.get("Status") in ["Sold", "Shipped", "Completed"]:
            sold_details=[]
            sold_details.append(dmc.Text([
                dmc.Text("Tanggal Terjual: ", span=True, fw="bold"),
                dmc.Text(data_selected.get("Tanggal Sold"), span=True)
            ]))
            sold_details.append(dmc.Text([
                dmc.Text("Pembeli: ", span=True, fw="bold"),
                dmc.Text(f"{data_selected.get("Buyer Name").upper()} - {data_selected.get("Buyer Location").upper()} ({data_selected.get("Buyer WA")})", span=True)
            ]))
            sold_details.append(dmc.Text([
                dmc.Text("Nama Sales: ", span=True, fw="bold"),
                dmc.Text(data_selected.get("Nama Sales"), span=True)
            ]))
            sold_details.append(dmc.Text([
                dmc.Text("Harga Terjual: ", span=True, fw="bold"),
                dmc.Text(f"Rp. {data_selected.get('Price - Sold'):,d}", span=True)
            ]))
        elif data_selected.get("Status")=="Completed Elsewhere":
            sold_details="Consignment terjual diluar"
        else:
            sold_details="Consignment belum terjual."

        shipped_details=[
            dmc.Text("Tracking ID: ", span=True, fw="bold"),
            dmc.Text(data_selected.get("Tracking ID") if data_selected.get("Tracking ID") else "N/a", span=True)
        ]

        disable_change=data_selected.get("Status") not in ["New", "Posted"]

        return not modal, context, ownerprice, disable_change, igprice, disable_change, disable_change, iglink, sold_details, shipped_details

    else:
        return False, "", 0, False, 0, False, False, "", "", ""