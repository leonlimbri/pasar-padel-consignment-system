import dash_mantine_components as dmc
from dash_iconify import DashIconify

def generate_multi_select(_id, label, description, options):
    return dmc.MultiSelect(
        id=_id, clearable=True, 
        label=label, description=description,
        data=options,
    )

def generate_button(_id, label, popover, color, icon, disabled:bool=False):
    return dmc.Box([
        dmc.Button(
            id=_id,
            children=dmc.Text(label, size="sm"),
            leftSection=DashIconify(icon=icon),
            fullWidth=True,
            color=color,
            disabled=disabled
        ),
        dmc.Tooltip(
            target=f"#{_id}",
            label=popover,
            position="top",
            withArrow=True,
            transitionProps={
                "transition": "slide-up", 
                "duration": 200,
                "timingFunction": "ease"
            },
            color=color
        )
    ])