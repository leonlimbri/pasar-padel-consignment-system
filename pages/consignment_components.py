import dash_ag_grid as dag
import dash_mantine_components as dmc

# Consignment Table
columnDefs = [
    {"field": "ID", "headerName": "Consignment ID", "filter": "agNumberColumnFilter", "valueFormatter": {"function": "`PP${params.value}`"}},
    {"field": "Item Type", "headerName": "Tipe Barang"},
    {"field": "Item Name", "headerName": "Nama Barang", "filter": True},
    {"field": "Status", "headerName": "Status"},
]

tb_consignments = dag.AgGrid(
    id = "tb_consignment",
    columnDefs = columnDefs,
    rowData = [],
    columnSize = "responsiveSizeToFit",
    defaultColDef = {"sortable": True},
    dashGridOptions = {
        "rowSelection": {
            "mode": "singleRow",
            "enableClickSelection": True
        }
    }
)