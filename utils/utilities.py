"""utils/utilities.py
General-purpose helper functions used across the app.
"""
from plotly import graph_objs as go

def check_any_input_is_empty(input):
    """Recursively check whether any value in `input` is considered empty.

    Rules:
    - None            → empty
    - int / float 0   → empty  (non-zero numbers are valid)
    - empty string    → empty
    - empty list      → empty
    - list with items → recurse into each element

    Returns True if any value is empty, False otherwise.
    """
    if input is None:
        return True

    if isinstance(input, (int, float)):
        # 0 is treated as "empty" (no value entered); other numbers are fine
        return input == 0

    if isinstance(input, list) and len(input) > 1:
        return any(check_any_input_is_empty(item) for item in input)

    return input == "" or len(input) == 0

def create_card(number, title, delta=None, prefix="", switch_color_scheme=False):
    """Return a Plotly Indicator figure styled as a KPI card.

    Args:
        number:              Current period value.
        title:               Card title shown above the number.
        delta:               Previous period value (enables delta arrow). Optional.
        prefix:              String prefix for the number (e.g. "Rp. ").
        switch_color_scheme: True = dark mode styling.
    """
    plot_bg = "#2b2b2b" if switch_color_scheme else "#ebebeb"
    template = "plotly_dark" if switch_color_scheme else "plotly_white"

    if delta is not None:
        indicator = go.Indicator(
            mode="number+delta",
            value=number,
            delta=dict(reference=delta, prefix=prefix, valueformat=",.0f", font=dict(size=14)),
            number=dict(prefix=prefix, valueformat=",.0f", font=dict(size=32)),
            title=dict(text=f"<b>{title}</b>", font=dict(size=20)),
            domain=dict(x=[0, 1], y=[0, 1]),
        )
        layout = go.Layout(
            margin=dict(l=10, r=10, t=40, b=5),
            height=140,
            plot_bgcolor=plot_bg,
            paper_bgcolor="rgba(0,0,0,0)",
            template=template,
        )
    else:
        indicator = go.Indicator(
            mode="number",
            value=number,
            number=dict(prefix=prefix, valueformat=",.0f", font=dict(size=32)),
            title=dict(text=f"<b>{title}</b>", font=dict(size=20)),
            domain=dict(x=[0, 1], y=[0, 1]),
        )
        layout = go.Layout(
            margin=dict(l=10, r=10, t=40, b=5),
            height=140,
        )

    return go.Figure(data=indicator, layout=layout)
