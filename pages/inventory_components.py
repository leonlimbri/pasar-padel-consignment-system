import dash_ag_grid as dag
import dash_mantine_components as dmc
import json
from dash_iconify import DashIconify

# Racket Table
racketColumnDefs=[
    {"field": "Brand", "headerName": "Brand", "filter": True, "minWidth": 150},
    {"field": "Nama Raket", "headerName": "Nama Raket", "filter": True, "minWidth": 150},
    {"field": "Woman", "headerName": "Woman's Racket", "filter": True, "minWidth": 150},
    {"field": "Shape", "headerName": "Shape", "filter": True, "minWidth": 150},
    {"field": "Additional Specification", "headerName": "Additional Specs", "filter": True, "minWidth": 150},
    {"field": "Surface Material", "headerName": "Face", "filter": True, "minWidth": 150},
    {"field": "Core Material", "headerName": "Core", "filter": True, "minWidth": 150},
    {"field": "Count", "headerName": "Jumlah ter-consign", "filter": "agNumberColumnFilter", "minWidth": 150},
]

tb_racket=dag.AgGrid(
    id="table-racket",
    columnDefs=racketColumnDefs,
    rowData=[],
    defaultColDef={"sortable": True, "filter": True},
    dashGridOptions={
        "rowSelection": {
            "mode": "singleRow",
            "enableClickSelection": True
        },
        "suppressColumnVirtualisation": True
    }
)

# Other Items Table
otherColumnDefs=[
    {"field": "Tipe Barang", "headerName": "Tipe Barang", "filter": True},
    {"field": "Brand", "headerName": "Brand", "filter": True},
    {"field": "Nama Barang", "headerName": "Nama Barang", "filter": True},
    {"field": "Count", "headerName": "Jumlah ter-consign", "filter": "agNumberColumnFilter"},
]

tb_other=dag.AgGrid(
    id="table-other",
    columnDefs=otherColumnDefs,
    rowData=[],
    columnSize="responsiveSizeToFit",
    defaultColDef={"sortable": True},
    dashGridOptions={
        "rowSelection": {
            "mode": "singleRow",
            "enableClickSelection": True
        },
        "suppressColumnVirtualisation": True
    }
)

# Inventory Modal (Add New Racket)
invmodal_racket_text=json.load(open("assets/texts.json")).get("inventory-modal").get("racket")
modal_new_racket=dmc.Modal(
    id="modal-new-racket",
    size="lg",
    title=dmc.Text(invmodal_racket_text.get("title"), fw="bold"),
    children=[
        dmc.Text(invmodal_racket_text.get("subtitle"), fz="xs"),        
        dmc.Divider(mt=5, mb=5),
        
        # Racket Brand
        dmc.Autocomplete(
            id="textinput-new-racket-brand",
            label=invmodal_racket_text.get("brand-title"),
            withAsterisk=True,
            size="xs",
        ),

        # Racket Name
        dmc.Autocomplete(
            id="textinput-new-racket-name",
            label=invmodal_racket_text.get("name-title"),
            withAsterisk=True,
            size="xs"
        ),

        # Identifier Woman's Racket 
        dmc.Switch(
            id="switch-new-woman-racket",
            label=invmodal_racket_text.get("woman-racket-title"),
            description=invmodal_racket_text.get("woman-racket-description"),
            size="xs", 
            mt=10, mb=10,
        ),

        # Racket Shape
        dmc.Autocomplete(
            id="textinput-new-racket-shape",
            label=invmodal_racket_text.get("shape-title"),
            withAsterisk=True,
            size="xs",
        ),

        # Racket Face
        dmc.Autocomplete(
            id="textinput-new-racket-face",
            label=invmodal_racket_text.get("face-title"),
            withAsterisk=True,
            size="xs",
        ),

        # Racket Core
        dmc.Autocomplete(
            id="textinput-new-racket-core",
            label=invmodal_racket_text.get("core-title"),
            withAsterisk=True,
            size="xs",
        ),

        # Racket Additional Specs
        dmc.MultiSelect(
            id="multiselect-new-racket-additionalspecs",
            label=invmodal_racket_text.get("additional-specs-title"),
            searchable=True,
            size="xs",
        ),

        # Racket Weight
        dmc.TextInput(
            id="textinput-new-racket-weight",
            label=invmodal_racket_text.get("weight-title"), 
            size="xs", 
            placeholder=invmodal_racket_text.get("weight-placeholder"),
        ),

        # Button to submit
        dmc.Button(
            id="button-add-new-racket",
            children=invmodal_racket_text.get("button-add-new").get("title"),
            leftSection=DashIconify(icon=invmodal_racket_text.get("button-add-new").get("icon")),
            color=invmodal_racket_text.get("button-add-new").get("color"),
            fullWidth=True,
            mt=20,
        ),
    ],
)

# Inventory Modal (View Racket)
modal_racket_view=dmc.Modal(
    id="modal-racket-view",
    size="md",
    title=dmc.Text(invmodal_racket_text.get("modal-racket-view-name"), fw="bold"),
    children=[
        dmc.Text(invmodal_racket_text.get("subtitle-view"), fz="xs"),        
        dmc.Divider(mt=5, mb=5),
        
        # Racket Brand and Model Name
        dmc.Text(
            id="text-view-racket-brand-model",
            size="sm",
        ),

        # Identifier Woman's Racket 
        dmc.Switch(
            id="switch-view-woman-racket",
            label=invmodal_racket_text.get("woman-racket-title"),
            description=invmodal_racket_text.get("woman-racket-description"),
            size="xs", 
            mt=10, mb=10,
        ),

        # Racket Shape
        dmc.Autocomplete(
            id="textinput-view-racket-shape",
            label=invmodal_racket_text.get("shape-title"),
            withAsterisk=True,
            size="xs",
        ),

        # Racket Face
        dmc.Autocomplete(
            id="textinput-view-racket-face",
            label=invmodal_racket_text.get("face-title"),
            withAsterisk=True,
            size="xs",
        ),

        # Racket Core
        dmc.Autocomplete(
            id="textinput-view-racket-core",
            label=invmodal_racket_text.get("core-title"),
            withAsterisk=True,
            size="xs",
        ),

        # Racket Additional Specs
        dmc.MultiSelect(
            id="multiselect-view-racket-additionalspecs",
            label=invmodal_racket_text.get("additional-specs-title"),
            searchable=True,
            size="xs",
        ),

        # Racket Weight
        dmc.TextInput(
            id="textinput-view-racket-weight",
            label=invmodal_racket_text.get("weight-title"), 
            size="xs", 
            placeholder=invmodal_racket_text.get("weight-placeholder"),
        ),

        # Button to save
        dmc.Button(
            id="button-save-view-racket",
            children=invmodal_racket_text.get("button-save-view").get("title"),
            leftSection=DashIconify(icon=invmodal_racket_text.get("button-save-view").get("icon")),
            color=invmodal_racket_text.get("button-save-view").get("color"),
            fullWidth=True,
            mt=20,
        ),
    ],
)

# Inventory Modal (Add New Item)
invmodal_others_text=json.load(open("assets/texts.json")).get("inventory-modal").get("others")
modal_new_item=dmc.Modal(
    id="modal-new-item",
    size="lg",
    title=dmc.Text(invmodal_racket_text.get("title"), fw="bold"),
    children=[
        dmc.Text(invmodal_racket_text.get("subtitle"), fz="xs"),        
        dmc.Divider(mt=5, mb=5),
        
        # Item Type
        dmc.Select(
            id="select-new-item-type",
            label=invmodal_others_text.get("type-title"),
            data=["Bag", "Shoes", "Shirt", "Others"],
            withAsterisk=True,
            searchable=True,
            size="xs",
        ),

        # Item Brand
        dmc.Autocomplete(
            id="textinput-new-item-brand",
            label=invmodal_others_text.get("brand-title"),
            withAsterisk=True,
            size="xs",
        ),

        # Item Name
        dmc.Autocomplete(
            id="textinput-new-item-name",
            label=invmodal_others_text.get("name-title"),
            withAsterisk=True,
            size="xs"
        ),

        # Button to submit
        dmc.Button(
            id="button-add-new-item",
            children=invmodal_others_text.get("button-add-new").get("title"),
            leftSection=DashIconify(icon=invmodal_others_text.get("button-add-new").get("icon")),
            color=invmodal_others_text.get("button-add-new").get("color"),
            fullWidth=True,
            mt=20,
        ),
    ],
)