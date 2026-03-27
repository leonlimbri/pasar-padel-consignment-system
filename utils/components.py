"""utils/components.py
Reusable Dash Mantine component factory functions used across pages.
"""

import dash_mantine_components as dmc
from dash_iconify import DashIconify


def generate_multi_select(_id, label, description, options):
    """Return a clearable MultiSelect dropdown component."""
    return dmc.MultiSelect(
        id=_id,
        clearable=True,
        label=label,
        description=description,
        data=options,
    )


def generate_button(_id, label, popover, color, icon, disabled: bool = False):
    """Return a full-width Button wrapped with a tooltip popover.

    Args:
        _id:      Component ID for the button (tooltip targets #{_id}).
        label:    Text displayed on the button.
        popover:  Tooltip text shown on hover.
        color:    Mantine color string (e.g. "first", "gray", "fourth").
        icon:     Iconify icon string (e.g. "gg:add").
        disabled: Whether the button starts in a disabled state.
    """
    return dmc.Box([
        dmc.Button(
            id=_id,
            children=dmc.Text(label, size="sm"),
            leftSection=DashIconify(icon=icon),
            fullWidth=True,
            color=color,
            disabled=disabled,
        ),
        dmc.Tooltip(
            target=f"#{_id}",
            label=popover,
            position="top",
            withArrow=True,
            transitionProps={
                "transition": "slide-up",
                "duration": 200,
                "timingFunction": "ease",
            },
            color=color,
        ),
    ])
