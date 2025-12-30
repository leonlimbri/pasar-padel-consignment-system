import dash_mantine_components as dmc
from dash_iconify import DashIconify

# Navigation Bar Component
page_navbar=dmc.AppShellNavbar(
    [
        dmc.Divider(label="Navigation", labelPosition="left"),
        dmc.NavLink(
            label="Consignments", href="/", active="partial",
            leftSection=DashIconify(icon="material-symbols-light:padel-outline"), 
        ),
        dmc.NavLink(
            label="Inventory", href="/inventory", active="partial",
            leftSection=DashIconify(icon="material-symbols-light:padel-outline"), 
        ),
        dmc.NavLink(
            label="Buat Caption IG", href="/caption-ig", active="partial",
            leftSection=DashIconify(icon="ri:instagram-line"), 
        ),
        dmc.NavLink(
            label="Dashboard", href="/dashboard", active="partial",
            leftSection=DashIconify(icon="tabler:dashboard"), 
        ),
        dmc.Divider(mt=10, mb=10),
        dmc.NavLink(
            label="Logout", href="/logout",
            leftSection=DashIconify(icon="mynaui:logout"), 
        ),
    ],
    p="md",
)