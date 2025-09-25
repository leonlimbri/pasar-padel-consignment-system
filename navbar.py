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