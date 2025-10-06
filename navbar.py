import dash_mantine_components as dmc
from dash_iconify import DashIconify

# Navigation Bar Component
NavigationBar=dmc.AppShellNavbar(
    id="navbar",
    children=[
        dmc.Divider(
            label="Navigation", 
            labelPosition="left"
        ),
        dmc.NavLink(
            label="Consignments", 
            leftSection=DashIconify(icon="material-symbols-light:padel-outline"), 
            href="/", 
            active="partial"
        ),
        dmc.NavLink(
            label="Inventory", 
            leftSection=DashIconify(icon="lsicon:inventory-outline"), 
            href="/inventory", 
            active="partial"
        ),
        dmc.NavLink(
            label="Buat Caption IG", 
            leftSection=DashIconify(icon="ri:instagram-line"), 
            href="/caption-ig", 
            active="partial"
        ),
        dmc.NavLink(
            label="Dashboard", 
            leftSection=DashIconify(icon="tabler:dashboard"), 
            href="/dashboard", 
            active="partial"
        ),
    ],
    p="md",
)


        # dmc.Title("Buat Caption Instagram", mt=20),
        # dmc.Text("Buat caption ig ...", mb=10, visibleFrom="sm"),
        # dmc.Grid(
        #     [
        #         dmc.GridCol(
        #             [
        #                 dmc.MultiSelect(
        #                     id="multiselect-caption-ig",
        #                     label="Consignment IDs"
        #                 )
        #             ],
        #             span=4
        #         ),
        #         dmc.Divider(orientation="vertical"),
        #         dmc.GridCol(
        #             [
        #                 dmc.Text(
        #                     "asdasdasd"
        #                 )
        #             ],
        #             span=7
        #         )
        #     ]
        # ),