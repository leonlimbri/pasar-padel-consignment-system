from dash import dcc
import dash_ag_grid as dag
import dash_mantine_components as dmc
import json
from dash_iconify import DashIconify

# Consignment Table
columnDefs=[
    {"field": "ID", "headerName": "Consignment ID", "minWidth": 150, "filter": "agNumberColumnFilter", "valueFormatter": {"function": "`PP${params.value}`"}},
    {"field": "Item Type", "headerName": "Tipe Barang", "minWidth": 150, "suppressHeaderFilterButton": True, "filter": "agTextColumnFilter"},
    {"field": "Item Name", "headerName": "Nama Barang", "minWidth": 150, "filter": True},
    {"field": "Price Seller", "headerName": "Harga Modal", "minWidth": 150, "filter": "agNumberColumnFilter", "valueFormatter": {"function": "'Rp. ' + d3.format(',.0f')(params.value)"}},
    {"field": "Price Posted", "headerName": "Harga di Instagram", "minWidth": 150, "filter": "agNumberColumnFilter", "valueFormatter": {"function": "'Rp. ' + d3.format(',.0f')(params.value)"}},
    {"field": "Seller WA", "headerName": "WA Seller", "minWidth": 150, "filter": True},
    {"field": "Seller Name", "headerName": "Nama Seller", "minWidth": 150, "filter": True},
    {"field": "Seller Location", "headerName": "Lokasi", "minWidth": 150, "filter": True},
    {"field": "Item Condition", "headerName": "Kondisi Barang", "minWidth": 150, "filter": True},
    {"field": "Status", "headerName": "Status", "minWidth": 150, "suppressHeaderFilterButton": True, "filter": "agTextColumnFilter"},
]

# Conditional Row for styling based on status
getRowStyle = {
    "styleConditions": [
        {
            "condition": "params.data.Status == 'New'",
            "style": {"backgroundColor": "#E6FF42C7"},
        },
        {
            "condition": "params.data.Status == 'Posted'",
            "style": {"backgroundColor": "#FFFFFFB5"}
        },
        {
            "condition": "params.data.Status == 'Sold'",
            "style": {"backgroundColor": "#3265FF80"}
        },
        {
            "condition": "params.data.Status == 'Shipped'",
            "style": {"backgroundColor": "#46B98580"}
        },
        {
            "condition": "params.data.Status == 'Completed Elsewhere'",
            "style": {"backgroundColor": "#74747439", }
        },
        {
            "condition": "params.data.Status == 'Completed'",
            "style": {"backgroundColor": "#1DDC8680"}
        },
    ],
    "defaultStyle": {"backgroundColor": "grey", "color": "white"}
}

tb_consignments=dag.AgGrid(
    id="table-consignment",
    className="ag-theme-alpine borders",
    columnDefs=columnDefs,
    rowData=[],
    # columnSize="responsiveSizeToFit",
    defaultColDef={"sortable": True},
    getRowStyle=getRowStyle,
    dashGridOptions={
        "rowSelection": {
            "mode": "multiRow",
            "enableClickSelection": True
        },
        "suppressColumnVirtualisation": True
    }
)

# Consignment Modal
consignment_text=json.load(open("assets/texts.json")).get("consignments")
conmodal_text=json.load(open("assets/texts.json")).get("consignments-modal")
modal_register_new=dmc.Modal(
    id="modal-register-consignment",
    size="lg",
    title=dmc.Text(conmodal_text.get("title"), fw="bold"),
    children=[
        dmc.Text(conmodal_text.get("subtitle"), fz="xs"),        
        dmc.Divider(mt=5, mb=5),
        dmc.Select(
            id="select-consignment-type",
            label=conmodal_text.get("consignment-type-title"), 
            data=consignment_text.get("input-filter-item-type").get("option"),
            withAsterisk=True,
            size="xs"
        ),
        
        # Racket Consignment Inputs
        dmc.Box(
            id="inputbox-racket", 
            children=[
                
                # Racket Name
                dmc.Select(
                    id="select-racket-name",
                    label=conmodal_text.get("input-racket").get("name-title"),
                    withAsterisk=True,
                    searchable=True,
                    size="xs",
                ),

                dmc.Divider(
                    label=conmodal_text.get("input-racket").get("divider"), 
                    labelPosition="center", 
                    mt=20,
                ),
                dmc.Text(id="text-racket-details", size="xs"),
                
                # Actual Weight 
                dmc.TextInput(
                    id="textinput-racket-weight",
                    label=conmodal_text.get("input-racket").get("weight-title"), 
                    size="xs", 
                    placeholder=conmodal_text.get("input-racket").get("weight-placeholder"),
                ),
            ],
        ),

        # Other Inputs
        dmc.Box(
            id="inputbox-others",
            children=[

                # Item Name
                dmc.Select(
                    id="select-item-name",
                    label=conmodal_text.get("input-others").get("name-title"),
                    searchable=True,
                    withAsterisk=True,
                    size="xs",
                ),

                # Shoe Size
                dmc.TextInput(
                    id="textinput-shoe-size",
                    label=conmodal_text.get("input-others").get("shoe-size-title"), 
                    placeholder=conmodal_text.get("input-others").get("shoe-size-placeholder"),
                    size="xs", 
                ),
                
                # Shirt Size
                dmc.TextInput(
                    id="textinput-shirt-size",
                    label=conmodal_text.get("input-others").get("shirt-size-title"), 
                    placeholder=conmodal_text.get("input-others").get("shirt-size-placeholder"),
                    size="xs", 
                ),
                
                # Others Description
                dmc.Textarea(
                    id="textinput-others-description",
                    label=conmodal_text.get("input-others").get("others-description-title"), 
                    placeholder=conmodal_text.get("input-others").get("others-description-placeholder"),
                    size="xs", 
                ),
            ]
        ),

        # Owner Inputs
        dmc.Box(
            id="inputbox-owners",
            children=[
                
                dmc.Divider(
                    label=conmodal_text.get("input-owners").get("divider"),
                    labelPosition="center",
                    mt=20,
                ),

                # Owner WhatsApp
                dmc.Autocomplete(
                    id="textinput-owner-whatsapp",
                    label=conmodal_text.get("input-owners").get("owner-wa-title"), 
                    placeholder=conmodal_text.get("input-owners").get("owner-wa-placeholder"),
                    size="xs", 
                    withAsterisk=True,
                ),

                # Input new owners
                dmc.Box(
                    id="inputbox-owners-new",
                    children=[
                        dmc.TextInput(
                            id="textinput-owner-name",
                            label=conmodal_text.get("input-owners").get("owner-name-title"),
                            placeholder=conmodal_text.get("input-owners").get("owner-name-placeholder"),
                            size="xs",
                            withAsterisk=True
                        ),
                        dmc.Autocomplete(
                            id="textinput-owner-location",
                            label=conmodal_text.get("input-owners").get("owner-location-title"),
                            placeholder=conmodal_text.get("input-owners").get("owner-location-placeholder"),
                            size="xs",
                            withAsterisk=True
                        )
                    ]
                ),
                
                # Owner and Sell Prices
                dmc.NumberInput(
                    id="numberinput-owner-price",
                    label=conmodal_text.get("input-owners").get("owner-price-title"),
                    value=10000,
                    size="xs", 
                    thousandSeparator=",",
                    withAsterisk=True,
                    allowNegative=False,
                    prefix="Rp."
                ),
                dmc.NumberInput(
                    id="numberinput-owner-sell-price",
                    label=conmodal_text.get("input-owners").get("owner-buyer-price-title"),
                    value=10000,
                    size="xs", 
                    thousandSeparator=",",
                    withAsterisk=True,
                    allowNegative=False,
                    prefix="Rp."
                ),

                # Identifier barang 
                dmc.Switch(
                    id="switch-old-racket",
                    label=conmodal_text.get("input-owners").get("owner-switch-title"),
                    description=conmodal_text.get("input-owners").get("owner-switch-description"),
                    size="xs", 
                    mt=10, mb=10,
                ),

                # Rating
                dmc.NumberInput(
                    id="numberinput-rating",
                    label=conmodal_text.get("input-owners").get("owner-rating"), 
                    size="xs", 
                    withAsterisk=True,
                    min=0, max=10,
                    decimalScale=1,
                    fixedDecimalScale=True,
                    value=10,
                    suffix=" / 10.0",
                )
            ]
        ),

        # Extra Note
        dmc.Textarea(
            id="textarea-extranote",
            label=conmodal_text.get("extranote-title"),
            placeholder=conmodal_text.get("extranote-placeholder"),
            size="xs"
        ),

        # Button to submit
        dmc.Button(
            id="button-add-consignment",
            children=conmodal_text.get("button-add-consignment").get("title"),
            leftSection=DashIconify(icon=conmodal_text.get("button-add-consignment").get("icon")),
            color=conmodal_text.get("button-add-consignment").get("color"),
            fullWidth=True,
            mt=20,
        ),
    ],
)

# Modal Post Consignments
postedmodal_text=conmodal_text.get("posted")
modal_post_consignment=dmc.Modal(
    id="modal-post-consignment",
    size="md",
    title=dmc.Text(postedmodal_text.get("title"), fw="bold"),
    children=[
        dmc.Text(id="text-posted-consignments", fz="xs"),
        dmc.Divider(mt=10, mb=10),
        dmc.TextInput(
            id="textinput-posted-link",
            label=postedmodal_text.get("iglink-title"),
            placeholder=postedmodal_text.get("iglink-placeholder"),
            size="xs",
            withAsterisk=True
        ),
        dmc.Button(
            id="button-submit-post-consignment",
            children=postedmodal_text.get("button-submit").get("title"),
            leftSection=DashIconify(icon=postedmodal_text.get("button-submit").get("icon")),
            color=postedmodal_text.get("button-submit").get("color"),
            fullWidth=True,
            mt=20,
        )
    ]
)

# Modal Sold Consignments
soldmodal_text=conmodal_text.get("sold")
modal_sold_consignment=dmc.Modal(
    id="modal-sold-consignment",
    size="md",
    title=dmc.Text(soldmodal_text.get("title"), fw="bold"),
    children=[
        dmc.Text(id="text-sold-details", size="xs"),
        dmc.Divider(mt=10, mb=10),


        # Sales Name
        dmc.Autocomplete(
            id="textinput-sales-name",
            label=soldmodal_text.get("input-buyers").get("buyer-sales-title"), 
            placeholder=soldmodal_text.get("input-buyers").get("buyer-sales-placeholder"),
            size="xs", 
            withAsterisk=True,
        ),

        # Switch to check whether sold in Pasar Padel
        dmc.Switch(
            id="switch-pasar-padel",
            label=soldmodal_text.get("soldswitch-title"),
            description=soldmodal_text.get("soldswitch-description"),
            size="xs", 
            checked=True,
            mt=10, mb=10,
        ),

        # Owner Inputs
        dmc.Box(
            id="inputbox-buyers",
            children=[
                
                dmc.Divider(
                    label=soldmodal_text.get("input-buyers").get("divider"),
                    labelPosition="center",
                    mt=20,
                ),

                # buyer WhatsApp
                dmc.Autocomplete(
                    id="textinput-buyer-whatsapp",
                    label=soldmodal_text.get("input-buyers").get("buyer-wa-title"), 
                    placeholder=soldmodal_text.get("input-buyers").get("buyer-wa-placeholder"),
                    size="xs", 
                    withAsterisk=True,
                ),

                # Input new buyers
                dmc.Box(
                    id="inputbox-buyers-new",
                    children=[
                        dmc.TextInput(
                            id="textinput-buyer-name",
                            label=soldmodal_text.get("input-buyers").get("buyer-name-title"),
                            placeholder=soldmodal_text.get("input-buyers").get("buyer-name-placeholder"),
                            size="xs",
                            withAsterisk=True
                        ),
                        dmc.Autocomplete(
                            id="textinput-buyer-location",
                            label=soldmodal_text.get("input-buyers").get("buyer-location-title"),
                            placeholder=soldmodal_text.get("input-buyers").get("buyer-location-placeholder"),
                            size="xs",
                            withAsterisk=True
                        )
                    ]
                ),
                
                # Final Prices
                dmc.NumberInput(
                    id="numberinput-final-price",
                    label=soldmodal_text.get("input-buyers").get("final-price-title"),
                    value=10000,
                    size="xs", 
                    thousandSeparator=",",
                    withAsterisk=True,
                    allowNegative=False,
                    prefix="Rp."
                ),
            ]
        ),

        dmc.Button(
            id="button-submit-sold-consignment",
            children=soldmodal_text.get("button-submit").get("title"),
            leftSection=DashIconify(icon=soldmodal_text.get("button-submit").get("icon")),
            color=soldmodal_text.get("button-submit").get("color"),
            fullWidth=True,
            mt=20,
        )
    ]
)

# Modal Shipped Consignments
shippedmodal_text=conmodal_text.get("shipped")
modal_shipped_consignment=dmc.Modal(
    id="modal-shipped-consignment",
    size="md",
    title=dmc.Text(shippedmodal_text.get("title"), fw="bold"),
    children=[
        dmc.Text(id="text-shipped-consignments", fz="xs"),
        dmc.Divider(mt=10, mb=10),
        dmc.TextInput(
            id="textinput-shipped-trackingid",
            label=shippedmodal_text.get("trackingid-title"),
            placeholder=shippedmodal_text.get("trackingid-placeholder"),
            size="xs",
            withAsterisk=True
        ),
        dmc.Button(
            id="button-submit-shipped-consignment",
            children=shippedmodal_text.get("button-submit").get("title"),
            leftSection=DashIconify(icon=shippedmodal_text.get("button-submit").get("icon")),
            color=shippedmodal_text.get("button-submit").get("color"),
            fullWidth=True,
            mt=20,
        )
    ]
)

# Modal Completed Consignments
completedmodal_text=conmodal_text.get("completed")
modal_completed_consignment=dmc.Modal(
    id="modal-completed-consignment",
    size="md",
    title=dmc.Text(completedmodal_text.get("title"), fw="bold"),
    children=[
        dmc.Text(id="text-completed-consignments", fz="xs"),
        dmc.Divider(mt=10, mb=10),
        dmc.Button(
            id="button-submit-completed-consignment",
            children=completedmodal_text.get("button-submit").get("title"),
            leftSection=DashIconify(icon=completedmodal_text.get("button-submit").get("icon")),
            color=completedmodal_text.get("button-submit").get("color"),
            fullWidth=True,
            mt=20,
        )
    ]
)

# Modal confirmation
modal_confirm_consignment=dmc.Modal(
    id="modal-consignment-confirm",
    size="sm",
    title=dmc.Text("Konfirmasi Tindakan", fw="bold"),
    children=[
        dmc.Text(id="text-confirm", fz="xs"),
        dmc.Box(
            id="grid-unsold",
            children=[
                dmc.Grid(
                    children=[
                        dmc.GridCol(dmc.Button(id="button-confirm-unsold", leftSection=DashIconify(icon="ix:success-filled"), fullWidth=True, mt=20, color="#5B8710"), span=6),
                        dmc.GridCol(dmc.Button(id="button-cancel-unsold", leftSection=DashIconify(icon="material-symbols:cancel-rounded"), fullWidth=True, mt=20, color="#960f0f"), span=6)
                    ],
                )
            ]
        ),
        dmc.Box(
            id="grid-delete",
            children=[
                dmc.Grid(
                    children=[
                        dmc.GridCol(dmc.Button(id="button-confirm-delete", leftSection=DashIconify(icon="ix:success-filled"), fullWidth=True, mt=20, color="#5B8710"), span=6),
                        dmc.GridCol(dmc.Button(id="button-cancel-delete", leftSection=DashIconify(icon="material-symbols:cancel-rounded"), fullWidth=True, mt=20, color="#960f0f"), span=6)
                    ]
                )
            ]
        )
    ]
)

# Modal View Consignments
modal_view_consignment=dmc.Modal(
    id="modal-view-consignment",
    size="lg",
    title=dmc.Text(conmodal_text.get("title-view"), fw="bold"),
    children=[
        dmc.Text(conmodal_text.get("subtitle-view"), fz="xs"),        
        dmc.Divider(mt=10, mb=10),

        # Consignment Item Details
        dmc.Text(
            id="text-view-consignment-details",
            size="sm",
        ),

        # Owner and Sell Prices
        dmc.Divider(label="Ubah Harga buyer / Jual", mt=10, mb=10),
        dmc.NumberInput(
            id="numberinput-view-owner-price",
            label=conmodal_text.get("input-owners").get("owner-price-title"),
            size="xs", 
            thousandSeparator=",",
            withAsterisk=True,
            allowNegative=False,
            prefix="Rp."
        ),
        dmc.NumberInput(
            id="numberinput-view-owner-buyer-price",
            label=conmodal_text.get("input-owners").get("owner-buyer-price-title"),
            size="xs", 
            thousandSeparator=",",
            withAsterisk=True,
            allowNegative=False,
            prefix="Rp."
        ),

        # Button to Save
        dmc.Button(
            id="button-save-price-change",
            children=conmodal_text.get("button-price-change").get("title"),
            leftSection=DashIconify(icon=conmodal_text.get("button-price-change").get("icon")),
            color=conmodal_text.get("button-price-change").get("color"),
            fullWidth=True,
            mt=20,
        ),

        dmc.Divider(label="Link Instagram Post", mt=10, mb=10),
        dmc.Text(id="text-view-iglink", size="xs"),

        dmc.Divider(label="Data Penjualan", mt=10, mb=10),
        dmc.Text(id="text-view-sold-details", size="xs"),
        
        dmc.Divider(label="Data Shipment", mt=10, mb=10),
        dmc.Text(id="text-view-shipped-details", size="xs"),

        dmc.Grid(
            [
                # Button to Unsold
                dmc.GridCol(
                    dmc.Button(
                        id="button-unsold-consignment",
                        children=conmodal_text.get("button-unsold-consignment").get("title"),
                        leftSection=DashIconify(icon=conmodal_text.get("button-unsold-consignment").get("icon")),
                        color=conmodal_text.get("button-unsold-consignment").get("color"),
                        fullWidth=True,
                        mt=20,
                    ),
                    span=6
                ),
                # Button to Delete
                dmc.GridCol(
                    dmc.Button(
                        id="button-delete-consignment",
                        children=conmodal_text.get("button-delete-consignment").get("title"),
                        leftSection=DashIconify(icon=conmodal_text.get("button-delete-consignment").get("icon")),
                        color=conmodal_text.get("button-delete-consignment").get("color"),
                        fullWidth=True,
                        mt=20,
                    ),
                    span=6
                ),
            ]
        ),

    ],
)