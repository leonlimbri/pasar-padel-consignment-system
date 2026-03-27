"""navbar.py
Defines the sidebar navigation bar component for the app shell.
Includes the dark/light theme toggle, memory usage display, and nav links.
"""

import dash_mantine_components as dmc
from dash_iconify import DashIconify

page_navbar = dmc.AppShellNavbar(
    [
        # ── Theme toggle switch ───────────────────────────────────────────────
        dmc.Switch(
            id="switch-color-scheme",
            labelPosition="left",
            persistence=True,
            persistence_type="local",
            offLabel=DashIconify(icon="radix-icons:sun",  width=15, color="gray"),
            onLabel=DashIconify(icon="radix-icons:moon", width=15, color="gray"),
            label="Theme Toggle Switch",
            description="Toggle dark/light theme",
            checked=False,
        ),

        # ── Memory usage display (only visible in local/dev mode) ─────────────
        dmc.Text(id="memory-usage-text", size="sm", mt=10),

        # ── Nav links ────────────────────────────────────────────────────────
        dmc.Divider(label="Navigation", labelPosition="left", mt=10),
        dmc.NavLink(
            label="Consignments",
            href="/",
            active="partial",
            leftSection=DashIconify(icon="material-symbols-light:padel-outline"),
        ),
        dmc.NavLink(
            label="Dashboard",
            href="/dashboard",
            active="partial",
            leftSection=DashIconify(icon="tabler:dashboard"),
        ),

        dmc.Divider(mt=10, mb=10),

        dmc.NavLink(
            label="Logout",
            href="/logout",
            leftSection=DashIconify(icon="mynaui:logout"),
        ),
    ],
    p="md",
)
