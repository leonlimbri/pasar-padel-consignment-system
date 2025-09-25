from dash import register_page, html
from connection import *
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import dash_ag_grid as dag
import json

register_page(__name__, path = "/")

creds = create_connection()
header, data = get_data(creds, SPREADSHEET_ID, "Data_Consignment")
consignment_text = json.load(open("texts.json")).get("consignments")
consignment_status =  json.load(open("texts.json")).get("status-effect")

columnDefs = [
    {"field": "ID", "headerName": "Consignment ID", "filter": "agNumberColumnFilter", "valueFormatter": {"function": "`PP${params.value}`"}},
    {"field": "Item Type", "headerName": "Tipe Barang"},
    {"field": "Item Name", "headerName": "Nama Barang", "filter": True},
    {"field": "Status", "headerName": "Status"},
]

def parse_consignment(head, val):
    if head == "ID":
        return int(val[2:])
    elif head == "Status":
        consignment_stats_num = consignment_status.index(val) if consignment_status.index(val) else "X"
        return f"{consignment_stats_num}. {val}"
    else:
        return val
    
rowData = [
    {head: parse_consignment(head, val) if i>0 else int(val[2:]) for i, (head, val) in enumerate(zip(header, datum))} 
    for datum in data
]

tb_consignments = dag.AgGrid(
    id = "tb",
    columnDefs = columnDefs,
    rowData = rowData,
    columnSize = "responsiveSizeToFit",
    defaultColDef = {"sortable": True},
    dashGridOptions = {
        "rowSelection": {
            "mode": "singleRow",
            "enableClickSelection": True
        }
    }
)

layout = dmc.AppShellMain(
    [
        dmc.Title(consignment_text.get("title")),
        dmc.Text(consignment_text.get("subtitle"), mb = 10, visibleFrom="sm"),
        dmc.Text(consignment_text.get("subtitle"), mb = 10, hiddenFrom="sm", size = "xs"),

        # Desktop Version
        dmc.Divider(
            label = consignment_text.get("divider-one"), 
            labelPosition = "center",
            visibleFrom = "sm"
        ),
        dmc.Grid(
            [
                dmc.GridCol(
                    children = dmc.MultiSelect(
                        id = "filter-tipe", 
                        label = consignment_text.get("input-filter-tipe-barang").get("title"), 
                        data = consignment_text.get("input-filter-tipe-barang").get("option"), 
                        w = "100%"
                    ),
                    span = 3
                ),
                dmc.GridCol(
                    children = dmc.MultiSelect(
                        id = "filter-status", 
                        label = consignment_text.get("input-filter-status").get("title"), 
                        data = consignment_text.get("input-filter-status").get("option"), 
                        w = "100%"
                    ),
                    span = 3
                ),
                dmc.GridCol(
                    [
                        dmc.Button(
                            id = "button-register-consignment",
                            children = consignment_text.get("button-register-consignment").get("title"),
                            leftSection = DashIconify(icon = consignment_text.get("button-register-consignment").get("icon")),
                            color = consignment_text.get("button-register-consignment").get("color"),
                            fullWidth = True,
                            mt = 20,
                        ),
                        dmc.Tooltip(
                            target = "#button-register-consignment",
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
                            id = "button-refresh", 
                            children = consignment_text.get("button-refresh").get("title"), 
                            leftSection = DashIconify(icon = consignment_text.get("button-refresh").get("icon")), 
                            fullWidth = True,
                            color = consignment_text.get("button-refresh").get("color"),
                            mt = 20
                        ),
                        dmc.Tooltip(
                            target = "#button-refresh",
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
        ),
        
        # Mobile Version
        dmc.Group(
            [
                dmc.Button(
                    id = "button-register-consignment",
                    children = consignment_text.get("button-register-consignment").get("title"),
                    leftSection = DashIconify(icon = consignment_text.get("button-register-consignment").get("icon")),
                    color = consignment_text.get("button-register-consignment").get("color"),
                    fullWidth = True,
                ),
                dmc.Divider(label = consignment_text.get("divider-one"), labelPosition = "center"),
                dmc.Button(
                    id = "button-refresh", 
                    children = consignment_text.get("button-refresh").get("title"), 
                    leftSection = DashIconify(icon = consignment_text.get("button-refresh").get("icon")), 
                    color = consignment_text.get("button-refresh").get("color"),
                    fullWidth = True,
                ),
                dmc.Grid(
                    [
                        dmc.GridCol(
                            children = dmc.MultiSelect(
                                id = "filter-tipe", 
                                label = consignment_text.get("input-filter-tipe-barang").get("title"), 
                                data = consignment_text.get("input-filter-tipe-barang").get("option"), 
                                w = "43vw"
                            ),
                            span = 6
                        ),
                        dmc.GridCol(
                            children = dmc.MultiSelect(
                                id = "filter-status", 
                                label = consignment_text.get("input-filter-status").get("title"), 
                                data = consignment_text.get("input-filter-status").get("option"), 
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
        ),

        tb_consignments,

        dmc.Divider(
            label = consignment_text.get("divider-two"), 
            labelPosition = "center", 
            mt = 20
        ),

    ]
)