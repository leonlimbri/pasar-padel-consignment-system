import dash_mantine_components as dmc
from dash_iconify import DashIconify

# Navigation Bar Component
page_navbar=dmc.AppShellNavbar(
    [
        dmc.Switch(
            id="switch-color-scheme",labelPosition="left", persistence=True, persistence_type="local",
            offLabel=DashIconify(icon="radix-icons:sun", width=15, color="primary"),
            onLabel=DashIconify(icon="radix-icons:moon", width=15, color="primary"),
            label="Theme Toggle Switch",
            description="Toggle dark/light theme",
            checked=False
        ),
        dmc.Text(id="memory-usage-text", size="sm", mt=10,),
        dmc.Divider(label="Navigation", labelPosition="left", mt=10),
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