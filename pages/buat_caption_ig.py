from dash import register_page, callback, Output, Input, State, dcc
from connection import *
from dash_iconify import DashIconify
from .inventory_components import *
from .utils import *
import dash_mantine_components as dmc
import json

register_page(__name__, path="/caption-ig")
caption_ig_text=json.load(open("assets/texts.json")).get("caption-ig")

#TODO: Create layout, layout must haves:
# - refresh consignment ids selections
# - multiselect box for selecting consignment ids
# - copy to clipboard

desktop_layout=[
    dmc.Grid(
        [
            dmc.GridCol(
                [
                    dmc.MultiSelect(
                        id="multiselect-consignment-caption-ig-desktop",
                        label=caption_ig_text.get("consignment-selection-title"),
                        description=dmc.Button(
                            id="button-refresh-consignment-selection-desktop",
                            children=caption_ig_text.get("button-refresh-selection").get("title"),
                            leftSection=DashIconify(icon=caption_ig_text.get("button-refresh-selection").get("icon")),
                            color=caption_ig_text.get("button-refresh-selection").get("color"),
                            size="xs",
                            fullWidth=True,
                        ),
                        searchable=True,
                        size="xs"
                    ),
                    dmc.Button(
                        id="button-create-ig-caption-desktop",
                        children=caption_ig_text.get("button-create-caption").get("title"),
                        leftSection=DashIconify(icon=caption_ig_text.get("button-create-caption").get("icon")),
                        color=caption_ig_text.get("button-create-caption").get("color"),
                        fullWidth=True,
                        size="xs",
                        mt=10
                    ),
                ],
                span=3
            ),
            dmc.GridCol(
                [
                    dmc.Textarea(
                        id="text-ig-caption-desktop",
                        label=caption_ig_text.get("textarea-title"),
                        description=dcc.Clipboard(id="clipboard-ig-caption-desktop", target_id="text-ig-caption-desktop"),
                        size="xs",
                        autosize=True,
                    ),
                ],
                span=9
            )
        ],
        visibleFrom="sm"
    ),
]

mobile_layout=[
    dmc.Box(
        [
            dmc.MultiSelect(
                id="multiselect-consignment-caption-ig-mobile",
                label=caption_ig_text.get("consignment-selection-title"),
                description=dmc.Button(
                    id="button-refresh-consignment-selection-mobile",
                    children=caption_ig_text.get("button-refresh-selection").get("title"),
                    leftSection=DashIconify(icon=caption_ig_text.get("button-refresh-selection").get("icon")),
                    color=caption_ig_text.get("button-refresh-selection").get("color"),
                    size="xs",
                    fullWidth=True,
                ),
                searchable=True,
                size="xs"
            ),
            dmc.Button(
                id="button-create-ig-caption-mobile",
                children=caption_ig_text.get("button-create-caption").get("title"),
                leftSection=DashIconify(icon=caption_ig_text.get("button-create-caption").get("icon")),
                color=caption_ig_text.get("button-create-caption").get("color"),
                fullWidth=True,
                size="xs",
                mt=10
            ),
            dmc.Textarea(
                id="text-ig-caption-mobile",
                label=caption_ig_text.get("textarea-title"),
                description=dcc.Clipboard(id="clipboard-ig-caption-mobile", target_id="text-ig-caption-mobile"),
                size="xs",
                autosize=True,
                mt=10,
            ),
        ],
        hiddenFrom="sm"
    ),
]

layout=dmc.AppShellMain(
    [
        dmc.Title(caption_ig_text.get("title")),
        dmc.Text(caption_ig_text.get("subtitle"), mb=10, size="xs"),
        dmc.Divider(mt=10, mb=10),
        dcc.Store(id="data-persistent-caption"),
        
        dmc.LoadingOverlay(
            visible=False,
            id="loading-overlay-caption",
            overlayProps={"radius": "sm", "blur": 2},
            zIndex=10
        ),

        *desktop_layout,
        *mobile_layout
    ]
)

@callback(
    Output("multiselect-consignment-caption-ig-desktop", "data"),
    Output("multiselect-consignment-caption-ig-mobile", "data"),
    Output("data-persistent-caption", "data"),
    Input("button-refresh-consignment-selection-desktop", "n_clicks"),
    Input("button-refresh-consignment-selection-mobile", "n_clicks"),
    Input("url", "pathname"),
    running=[Output("loading-overlay-caption", "visible"), True, False]
)
def refresh_consignments(n_clicks_desktop, n_clicks_mobile, urls):
    if urls=="/caption-ig" or n_clicks_desktop or n_clicks_mobile:
        _, data_consignment=get_data(SPREADSHEET_ID, "Data_Consignment")
        _, data_racket=get_data(SPREADSHEET_ID, "Data_Raket")
        list_consignment=[con[0] for con in data_consignment if con[-1]=="New"]
        return list_consignment, list_consignment, {"data-consignment": data_consignment, "data-racket": data_racket}
    else:
        return [], []
    
@callback(
    Output("text-ig-caption-desktop", "value"),
    Output("text-ig-caption-mobile", "value"),
    Input("button-create-ig-caption-desktop", "n_clicks"),
    Input("button-create-ig-caption-mobile", "n_clicks"),
    State("multiselect-consignment-caption-ig-desktop", "value"),
    State("multiselect-consignment-caption-ig-mobile", "value"),
    State("data-persistent-caption", "data"),
    running=[Output("loading-overlay-caption", "visible"), True, False]
)
def buat_caption(n_clicks_desktop, n_clicks_mobile, consignment_desktop, consignment_mobile, data):
    if n_clicks_desktop or n_clicks_mobile:
        if consignment_desktop:
            consignments=consignment_desktop
        else:
            consignments=consignment_mobile
        
        data_consignment=data.get("data-consignment")
        data_racket=data.get("data-racket")
        consignment_texts=[]
        for con_id in consignments:
            for consignment in data_consignment:
                if consignment[0]==con_id:
                    con=consignment
                    break
            item_type=con[4]
            consignment_text=[]
            item_name=con[5].split("-")[1]
            consignment_text.append(f"{con[0]} {item_name}")

            if item_type=="Racket":
                for r in data_racket:
                    if r[0]==item_name:
                        shape, face, core=r[3], r[6], r[7]
                        consignment_text.append(f"Shape: {shape}")
                        consignment_text.append(f"Weight: {con[6]}")
                        consignment_text.append(f"Core: {core}")
                        consignment_text.append(f"Face: {face}")
                        break
            elif item_type=="Shirt" or item_type=="Shoes":
                consignment_text.append(f"Size: {con[9]}")
            elif item_type=="Others":
                consignment_text.append(f"Description: {con[9]}")
            
            if con[7]=="New":
                condition="New"
            else:
                condition=f"Used ({con[8]})"
            consignment_text.append(f"Condition: {condition}")
            consignment_text.append(f"💵 {con[12]} 💵")
            consignment_text.append(f"Location: {con[3].title()}")
            if con[10]: consignment_text.append(con[10])
            consignment_texts.append("\n".join(consignment_text))

        return "\n\n".join(consignment_texts), "\n\n".join(consignment_texts)
    else:
        return [], []
    