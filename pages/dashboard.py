"""pages/dashboard.py
Dashboard page showing consignment performance metrics.

Only accessible to users with the 'Admin' role.
Charts include: status breakdown, sale percentages, omzet/profit over time,
favorite consignment items, and per-sales performance.
"""

import dash_mantine_components as dmc
import plotly.graph_objs as go
import dash_ag_grid as dag
from pandas import to_datetime as pd_to_timestamp
from dash import Output, Input, callback, register_page, dcc, no_update
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from flask import session
from utils import run_query_from_sql, create_card

register_page(__name__, "/dashboard")

# ── Access-denied layout (non-Admin users) ────────────────────────────────────
empty_dashboard_layout = [
    dmc.Title("Dashboard Performa Consignments Pasar Padel"),
    dmc.Text(
        [
            "Anda tidak memiliki akses untuk melihat dashboard ini. ",
            dcc.Link("Kembali ke halaman utama", href="/"),
        ],
        c="dimmed",
    ),
]

# ── AG Grid value formatters ──────────────────────────────────────────────────
value_formatter_currency = {"function": "`Rp. `+d3.format(',.0f')(params.value)"}
value_formatter_number   = {"function": "d3.format(',.0f')(params.value)"}

# ── Favorite consignment table ────────────────────────────────────────────────
consignment_favorit_table_columns = [
    {"headerName": "Nama Barang",      "field": "item_name"},
    {"headerName": "# Consigned",      "field": "total_consigned",  "valueFormatter": value_formatter_number},
    {"headerName": "# Terjual",        "field": "total_sold",       "valueFormatter": value_formatter_number},
    {"headerName": "Rata-rata Omzet",  "field": "average_omzet",   "valueFormatter": value_formatter_currency},
    {"headerName": "Rata-rata Profit", "field": "average_profit",  "valueFormatter": value_formatter_currency},
]

consignment_favorite_table = dag.AgGrid(
    id="aggrid-consignment-favorite-table",
    className="ag-theme-quartz",
    columnDefs=consignment_favorit_table_columns,
    rowData=run_query_from_sql(
        "chart_consignment_favorite.sql",
        start_date=(date.today() - timedelta(days=7)).isoformat(),
        end_date=date.today().isoformat(),
    ),
    defaultColDef={
        "sortable":   True,
        "filter":     True,
        "resizable":  True,
    },
    dashGridOptions={
        "pagination":              True,
        "paginationPageSize":      250,
        "paginationPageSizeSelector": False,
        "rowBuffer":               0,
        "suppressHorizontalScroll": True,
    },
    style={"height": "300px", "width": "100%", "--ag-font-size": "0.8rem"},
    persistence=True,
    persisted_props=["filterModel", "columnState"],
    dangerously_allow_code=True,
    columnSize="sizeToFit",
)

# ── Main dashboard layout ─────────────────────────────────────────────────────
dashboard_layout = [
    # Mobile warning banner (dashboard is not optimised for small screens)
    dmc.Box(
        [
            dmc.Title("Dashboard Pasar Padel"),
            dmc.Text(
                "Mobile View tidak disarankan karena dashboard ini akan menampilkan banyak data dan grafik yang mungkin sulit untuk dilihat di layar kecil.",
                size="xs",
                c="dimmed",
            ),
        ],
        hiddenFrom="sm",
    ),

    dcc.Store(id="signal-to-refresh-consfav-table", storage_type="memory"),
    dmc.LoadingOverlay(id="loading-overlay-dashboard-financial-performance", visible=False),

    # ── Header row: title + date range picker ─────────────────────────────────
    dmc.Grid(
        [
            dmc.GridCol(
                [
                    dmc.Title("Dashboard Pasar Padel"),
                    dmc.Text(
                        "Dashboard dibawah ini digunakan untuk melihat performa consignments di Pasar Padel, dari persentase penjualan hingga financial omzet dan profit dan performa sales. Data dibawah semuanya dihitung dengan periode yang dipilih.",
                        size="sm",
                        c="dimmed",
                        visibleFrom="sm",
                    ),
                ],
                span=8,
            ),
            dmc.GridCol(
                dmc.DatePickerInput(
                    id="datepicker-dashboard-consignment",
                    label="Pilih Tanggal",
                    description="Pilih tanggal untuk melihat data performa consignment",
                    type="range",
                    value=[
                        (date.today() - timedelta(days=7)).isoformat(),
                        date.today().isoformat(),
                    ],
                    valueFormat="D MMMM YYYY",
                    presets=[
                        {
                            "value": [
                                (date.today() - timedelta(days=7)).isoformat(),
                                date.today().isoformat(),
                            ],
                            "label": "Last 7 days",
                        },
                        {
                            "value": [
                                date.today().replace(day=1).isoformat(),
                                date.today().isoformat(),
                            ],
                            "label": "This month",
                        },
                        {
                            "value": [
                                (date.today() - relativedelta(months=1)).replace(day=1).isoformat(),
                                (date.today().replace(day=1) - timedelta(days=1)).isoformat(),
                            ],
                            "label": "Last month",
                        },
                        {
                            "value": [
                                date(date.today().year, 1, 1).isoformat(),
                                date.today(),
                            ],
                            "label": "This year",
                        },
                        {
                            "value": [
                                date(date.today().year - 1, 1, 1).isoformat(),
                                date(date.today().year - 1, 12, 31).isoformat(),
                            ],
                            "label": "Last year",
                        },
                        {
                            "value": ["2025-01-01", date.today().isoformat()],
                            "label": "All Time",
                        },
                    ],
                ),
                span=4,
            ),
        ],
        visibleFrom="sm",
    ),

    dmc.Divider(mt=5, mb=10, visibleFrom="sm"),

    # ── KPI cards row ─────────────────────────────────────────────────────────
    dmc.Grid(
        [
            # Notes panel explaining delta calculation
            dmc.GridCol(
                dmc.Paper(
                    [
                        dmc.Text("Catatan", size="sm", fw="bolder"),
                        dmc.Text(
                            "Metric di sebelah dihitung berdasarkan periode tanggal yang dipilih. Nilai perubahan (delta) dibandingkan dengan periode sebelumnya dengan durasi yang sama.",
                            size="xs",
                            mb=5,
                        ),
                        dmc.Text(
                            "Contoh: jika memilih 1 Jan 2026 – 31 Jan 2026, maka delta menunjukkan perubahan dibandingkan 1 Des 2025 – 31 Des 2025.",
                            size="xs",
                            c="dimmed",
                        ),
                    ],
                    withBorder=True, shadow="sm", radius="md", p="xs",
                ),
                span=2,
            ),
            dmc.GridCol(
                dmc.Paper(dcc.Graph(id="card-total-omzet"),
                          withBorder=True, shadow="sm", radius="md", p="xs"),
                span=3,
            ),
            dmc.GridCol(
                dmc.Paper(dcc.Graph(id="card-total-profit"),
                          withBorder=True, shadow="sm", radius="md", p="xs"),
                span=3,
            ),
            dmc.GridCol(
                dmc.Paper(dcc.Graph(id="card-total-barang-consigned"),
                          withBorder=True, shadow="sm", radius="md", p="xs"),
                span=2,
            ),
            dmc.GridCol(
                dmc.Paper(dcc.Graph(id="card-total-barang-terjual"),
                          withBorder=True, shadow="sm", radius="md", p="xs"),
                span=2,
            ),
        ],
        visibleFrom="sm",
    ),

    # ── Charts row: status / percentage / omzet+profit ────────────────────────
    dmc.Grid(
        [
            dmc.GridCol(
                dmc.Paper(
                    [
                        dmc.Text("Data Consignment", fw="bolder"),
                        dmc.Text("Total barang di tiap status consignment", c="dimmed", size="xs"),
                        dcc.Graph(id="chart-consignment-status", config={"displayModeBar": False}),
                    ],
                    withBorder=True, shadow="sm", radius="md", p="xs",
                ),
                span=4,
            ),
            dmc.GridCol(
                dmc.Paper(
                    [
                        dmc.Text("Persentase Penjualan", fw="bolder"),
                        dmc.Text("Persentase penjualan pasar padel vs tempat lain", c="dimmed", size="xs"),
                        dcc.Graph(id="chart-percentage-sales", config={"displayModeBar": False}),
                    ],
                    withBorder=True, shadow="sm", radius="md", p="xs",
                ),
                span=3,
            ),
            dmc.GridCol(
                dmc.Paper(
                    [
                        dmc.Text("Omzet dan Profit Consignments", fw="bolder"),
                        dmc.Text("Omzet dan profit dari consignments", c="dimmed", size="xs"),
                        dcc.Graph(id="chart-financial-performance", config={"displayModeBar": False}),
                    ],
                    withBorder=True, shadow="sm", radius="md", p="xs",
                ),
                span=5,
            ),
        ],
        visibleFrom="sm",
    ),

    # ── Bottom row: favorite items table + sales performance chart ────────────
    dmc.Grid(
        [
            dmc.GridCol(
                dmc.Paper(
                    [
                        dmc.Text("Barang Consignment Favorit", fw="bolder"),
                        dmc.Text(
                            "Barang consignment yang paling diminati (paling banyak terconsign) pada periode yang dipilih",
                            c="dimmed", size="xs", mb=10,
                        ),
                        consignment_favorite_table,
                    ],
                    withBorder=True, shadow="sm", radius="md", p="xs",
                ),
                span=6,
            ),
            dmc.GridCol(
                dmc.Paper(
                    [
                        dmc.Text("Performance Sales", fw="bolder"),
                        dmc.Text(
                            "Performance dihitung dari jumlah penjualan serta total omzet yang dihasilkan.",
                            c="dimmed", size="xs",
                        ),
                        dcc.Graph(id="chart-sales-performance", config={"displayModeBar": False}),
                    ],
                    withBorder=True, shadow="sm", radius="md", p="xs",
                ),
                span=6,
            ),
        ],
        visibleFrom="sm",
    ),
]

# ── Page layout wrapper ───────────────────────────────────────────────────────
layout = dmc.AppShellMain(children=[dmc.Box(id="dashboard-layout")])


# ── Callbacks ─────────────────────────────────────────────────────────────────

@callback(
    Output("dashboard-layout", "children"),
    Input("url", "pathname"),
)
def show_dashboard(pathname):
    """Gate the dashboard behind Admin role; show 404 for unrecognised paths."""
    if pathname == "/dashboard":
        return dashboard_layout if session.get("role") == "Admin" else empty_dashboard_layout
    # Fallback 404 for any unexpected path routed here
    return [
        dmc.Title("404 - Halaman Tidak Ditemukan!"),
        dmc.Text(
            [
                "Halaman yang anda cari tidak ada / belom terbuatkan. ",
                dcc.Link("Kembali ke halaman utama", href="/"),
            ],
        ),
    ]


@callback(
    Output("chart-consignment-status",    "figure"),
    Output("chart-percentage-sales",      "figure"),
    Output("chart-financial-performance", "figure"),
    Output("card-total-omzet",            "figure"),
    Output("card-total-profit",           "figure"),
    Output("card-total-barang-consigned", "figure"),
    Output("card-total-barang-terjual",   "figure"),
    Output("aggrid-consignment-favorite-table", "rowData"),
    Output("chart-sales-performance",     "figure"),
    Input("datepicker-dashboard-consignment", "value"),
    Input("signal-to-refresh-consfav-table",  "data"),
    Input("switch-color-scheme",              "checked"),
    running=[
        Output("loading-overlay-dashboard-financial-performance", "visible"), True, False,
    ],
)
def update_dashboard_charts(date_range, signal_refresh_consfav, switch_color_scheme):
    """Rebuild all dashboard charts whenever the date range or theme changes."""
    template = "plotly_dark" if switch_color_scheme else "plotly_white"
    no_updates = (no_update,) * 9

    if None in date_range:
        return no_updates

    # ── Status breakdown bar chart ────────────────────────────────────────────
    STATUS_COLORS = {
        "New":                 "#7a8500",
        "Posted":              "#4a5270",
        "Sold":                "#1a3db5",
        "Shipped":             "#1a6b4a",
        "Completed Elsewhere": "#4a4a4a",
        "Completed":           "#0d7a42",
    }

    df_status = run_query_from_sql(
        "chart_status_consignments.sql",
        start_date=date_range[0],
        end_date=date_range[1],
    )
    status_x = [d["cnt"]    for d in df_status]
    status_y = [d["status"] for d in df_status]

    chart_bar_status = go.Figure(
        data=[
            go.Bar(
                x=status_x,
                y=status_y,
                orientation="h",
                marker_color=[STATUS_COLORS.get(s, "#7b82a0") for s in status_y],
                marker_line_width=0,
                text=status_x,
                textposition="outside",
                hovertemplate="<b>%{y}</b><br>Count: %{x}<extra></extra>",
                textfont=dict(size=10),
            )
        ],
        layout=go.Layout(
            xaxis_title="Jumlah Barang",
            yaxis_title="Status Consignment",
            margin=dict(l=20, r=20, t=10, b=20),
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#2b2b2b" if switch_color_scheme else "#ebebeb",
            template=template,
        ),
    )
    chart_bar_status.update_layout(
        yaxis=dict(tickfont=dict(size=10), title=dict(font=dict(size=11))),
        xaxis=dict(
            tickfont=dict(size=10),
            title=dict(font=dict(size=11)),
            range=[0, max(status_x) * 1.2],
        ),
    )

    # ── Sale percentage pie chart ─────────────────────────────────────────────
    df_pct = run_query_from_sql(
        "chart_percentage_sold.sql",
        start_date=date_range[0],
        end_date=date_range[1],
    )
    pct_values  = [d["pcnt"]   for d in df_pct]
    pct_labels  = [d["label"]  for d in df_pct]
    pct_statuses = [d["status"] for d in df_pct]

    chart_pie_percentage = go.Figure(
        data=[
            go.Pie(
                labels=pct_labels,
                values=pct_values,
                marker_colors=[STATUS_COLORS.get(s, "#7b82a0") for s in pct_statuses],
                hoverinfo="label+value+percent",
                pull=[0.03, 0.03],
            )
        ],
        layout=go.Layout(
            margin=dict(l=20, r=20, t=10, b=20),
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(size=10),
            template=template,
        ),
    )
    chart_pie_percentage.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="center", x=0.5,
        ),
    )

    # ── Omzet & profit line/bar chart ─────────────────────────────────────────
    df_fin = run_query_from_sql(
        "chart_omzet_profit.sql",
        start_date=date_range[0],
        end_date=date_range[1],
    )
    fin_x  = [pd_to_timestamp(d["the_date"]).date() for d in df_fin]
    fin_y1 = [d["total_omzet"]    for d in df_fin]   # omzet line
    fin_y2 = [d["total_profit"]   for d in df_fin]   # profit line
    fin_y3 = [d["total_terjual"]  for d in df_fin]   # sold bar
    fin_y4 = [d["total_consigned"] for d in df_fin]  # consigned bar

    chart_omzet_profit = go.Figure(
        data=[
            go.Scatter(x=fin_x, y=fin_y1, name="Total Omzet",   marker_color="#1f77b4", yaxis="y1", line=dict(width=1)),
            go.Scatter(x=fin_x, y=fin_y2, name="Total Profit",  marker_color="#ff7f0e", yaxis="y1", line=dict(width=1)),
            go.Bar(    x=fin_x, y=fin_y3, name="# Sold",        marker_color="#2ca02c", yaxis="y2", opacity=0.5),
            go.Bar(    x=fin_x, y=fin_y4, name="# Consigned",   marker_color="#d62728", yaxis="y2", opacity=0.5),
        ],
        layout=go.Layout(
            margin=dict(l=20, r=20, t=10, b=20),
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#2b2b2b" if switch_color_scheme else "#ebebeb",
            font=dict(size=9),
            template=template,
            yaxis=dict(
                title="Omzet dan Profit (Rp)",
                tickfont=dict(size=10),
                tickformat=",.0f",
            ),
            yaxis2=dict(
                title="Consigned dan Terjual (#)",
                tickfont=dict(size=9),
                tickformat=",.0f",
                overlaying="y",  # overlay on the same plot area
                side="right",
                showgrid=False,  # avoid double gridlines
            ),
        ),
    )
    chart_omzet_profit.update_layout(
        hovermode="x unified",
        xaxis=dict(tickfont=dict(size=10), title=dict(font=dict(size=11))),
        yaxis=dict(tickfont=dict(size=10), title=dict(font=dict(size=11))),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="center", x=0.5,
        ),
    )

    # ── Previous-period data for KPI deltas ───────────────────────────────────
    date_start = pd_to_timestamp(date_range[0])
    date_end   = pd_to_timestamp(date_range[1])
    duration   = (date_end - date_start).days + 1

    df_fin_prev = run_query_from_sql(
        "chart_omzet_profit.sql",
        start_date=(date_start - relativedelta(days=duration)).date().isoformat(),
        end_date=(date_end   - relativedelta(days=duration)).date().isoformat(),
    )
    fin_prev_y1 = [d["total_omzet"]     for d in df_fin_prev]
    fin_prev_y2 = [d["total_profit"]    for d in df_fin_prev]
    fin_prev_y3 = [d["total_terjual"]   for d in df_fin_prev]
    fin_prev_y4 = [d["total_consigned"] for d in df_fin_prev]

    # Current-period totals
    omzet           = sum(fin_y1)
    profit          = sum(fin_y2)
    total_terjual   = sum(fin_y3)
    total_consigned = sum(fin_y4)

    # Previous-period totals (used as delta reference)
    omzet_prev           = sum(fin_prev_y1)
    profit_prev          = sum(fin_prev_y2)
    total_terjual_prev   = sum(fin_prev_y3)
    total_consigned_prev = sum(fin_prev_y4)

    # ── Favorite consignment table data ───────────────────────────────────────
    consignment_fav_rowdata = run_query_from_sql(
        "chart_consignment_favorite.sql",
        start_date=date_range[0],
        end_date=date_range[1],
    )

    # ── Sales performance chart ───────────────────────────────────────────────
    df_sales = run_query_from_sql(
        "chart_sales_performance.sql",
        start_date=date_range[0],
        end_date=date_range[1],
    )
    sales_x  = [d["sales_name"]  for d in df_sales]
    sales_y1 = [d["total_sold"]  for d in df_sales]
    sales_y2 = [d["total_omset"] for d in df_sales]
    sales_y3 = [d["total_profit"] for d in df_sales]

    chart_sales_performance = go.Figure(
        data=[
            go.Bar(    x=sales_x, y=sales_y2, name="Total Omzet",  marker_color="#1f77b4", yaxis="y2", opacity=0.5),
            go.Bar(    x=sales_x, y=sales_y3, name="Total Profit", marker_color="#ff7f0e", yaxis="y2", opacity=0.5),
            go.Scatter(x=sales_x, y=sales_y1, name="Total Sold",   marker_color="#d62728", yaxis="y1", opacity=0.5, line=dict(width=1)),
        ],
        layout=go.Layout(
            margin=dict(l=20, r=20, t=10, b=20),
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#2b2b2b" if switch_color_scheme else "#ebebeb",
            font=dict(size=9),
            template=template,
            yaxis=dict(
                title="Total Consigned / Sold",
                tickfont=dict(size=10),
                tickformat=",.0f",
            ),
            yaxis2=dict(
                title="Total Omzet (Rp.)",
                tickfont=dict(size=9),
                tickformat=",.0f",
                overlaying="y",
                side="right",
                showgrid=False,
            ),
        ),
    )
    chart_sales_performance.update_layout(
        hovermode="x unified",
        xaxis=dict(tickfont=dict(size=10), title=dict(font=dict(size=11))),
        yaxis=dict(tickfont=dict(size=10), title=dict(font=dict(size=11))),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="center", x=0.5,
        ),
    )

    return (
        chart_bar_status,
        chart_pie_percentage,
        chart_omzet_profit,
        create_card(omzet,           "Total Omzet",       delta=omzet_prev,           prefix="Rp. ", switch_color_scheme=switch_color_scheme),
        create_card(profit,          "Total Profit",      delta=profit_prev,          prefix="Rp. ", switch_color_scheme=switch_color_scheme),
        create_card(total_consigned, "Total # Consigned", delta=total_consigned_prev, switch_color_scheme=switch_color_scheme),
        create_card(total_terjual,   "Total # Terjual",   delta=total_terjual_prev,   switch_color_scheme=switch_color_scheme),
        consignment_fav_rowdata,
        chart_sales_performance,
    )


@callback(
    Output("signal-to-refresh-consfav-table", "data", allow_duplicate=True),
    Input("url", "pathname"),
    prevent_initial_call=True,
)
def refresh_consignment_favorite_table(pathname):
    """Trigger a table refresh whenever the user navigates to the dashboard."""
    if pathname == "/dashboard":
        return str(datetime.now())
    return no_update


@callback(
    Output("aggrid-consignment-favorite-table", "className"),
    Input("switch-color-scheme", "checked"),
    supress_callback_exceptions=True,
)
def toggle_color_scheme(switch_on):
    """Switch the AG Grid theme class between light and dark."""
    return "ag-theme-quartz-dark" if switch_on else "ag-theme-quartz"
