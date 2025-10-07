from dash import register_page, callback, Output, Input, State, dcc, no_update
from connection import *
from .consignment_components import *
from .utils import *
from flask import session
import dash_mantine_components as dmc
import plotly.graph_objects as go
import pandas as pd
import numpy as np

register_page(__name__, path="/dashboard")
dashboard_text=json.load(open("assets/texts.json")).get("dashboard")
empty_dashboard_layout=[
    dmc.Title(dashboard_text.get("title-empty")),
    dmc.Text(dashboard_text.get("subtitle-empty"), mb=10),
]
dashboard_layout=[
    dmc.Title(dashboard_text.get("title")),
    dmc.Text(dashboard_text.get("subtitle"), mb=10),
    dmc.Button(
        id="button-refresh-dashboard", 
        children=dashboard_text.get("button-refresh").get("title"), 
        leftSection=DashIconify(icon=dashboard_text.get("button-refresh").get("icon")), 
        color=dashboard_text.get("button-refresh").get("color"),
        mb=20
    ),
    dcc.Store(id="data-persistent-consignment"),
    dmc.LoadingOverlay(
        visible=False,
        id="loading-overlay-dashboard",
        overlayProps={"radius": "sm", "blur": 2},
        style={"height": "200vh"},
        zIndex=10
    ),
    dmc.Grid(
        [
            dmc.GridCol(
                dmc.Paper(
                    children=[
                        dmc.Title(dashboard_text.get("dashboard-one").get("title")),
                        dmc.Text(dashboard_text.get("dashboard-one").get("subtitle"), size="xs"),
                        dcc.Graph(id="dashboard-one")
                    ],
                    shadow="sm",
                    p="sm",
                    withBorder=True,
                ),
                span={"base": 12, "sm": 7}
            ),
            dmc.GridCol(
                dmc.Paper(
                    children=[
                        dmc.Title(dashboard_text.get("dashboard-two").get("title")),
                        dmc.Text(dashboard_text.get("dashboard-two").get("subtitle"), size="xs"),
                        dcc.Graph(id="dashboard-two")
                    ],
                    shadow="sm",
                    p="sm",
                    withBorder=True,
                ),
                span={"base": 12, "sm": 5}
            )
        ]
    ),
    dmc.Divider(mt=10, mb=10),
    dmc.Title(dashboard_text.get("dashboard-finance").get("title")),
    dmc.Text(dashboard_text.get("dashboard-finance").get("subtitle"), size="sm"),
    dmc.Tabs(
        [
            dmc.TabsList(
                [
                    dmc.TabsTab("Rincian Mingguan", value="weekly"),
                    dmc.TabsTab("Rincian Bulanan", value="monthly")
                ],
                mb=20
            ),
            dmc.DatePickerInput(id="daterange-dashboard", type="range", label="Tanggal Rincian", mb=20),
            dmc.TabsPanel(
                dmc.Grid(
                    [
                        dmc.GridCol(
                            dmc.Paper(
                                children=[
                                    dmc.Title(dashboard_text.get("dashboard-finance").get("finance-one").get("title")),
                                    dmc.Text(dashboard_text.get("dashboard-finance").get("finance-one").get("subtitle"), size="xs"),
                                    dcc.Graph(id="dashboard-weekly-one")
                                ],
                                shadow="sm",
                                p="sm",
                                withBorder=True,
                            ),
                            span={"base": 12, "sm": 6}
                        ),
                        dmc.GridCol(
                            dmc.Paper(
                                children=[
                                    dmc.Title(dashboard_text.get("dashboard-finance").get("finance-two").get("title")),
                                    dmc.Text(dashboard_text.get("dashboard-finance").get("finance-two").get("subtitle"), size="xs"),
                                    dcc.Graph(id="dashboard-weekly-two")
                                ],
                                shadow="sm",
                                p="sm",
                                withBorder=True,
                            ),
                            span={"base": 12, "sm": 6}
                        )
                    ]
                ),
                value="weekly"
            ),
            dmc.TabsPanel(
                dmc.Grid(
                    [
                        dmc.GridCol(
                            dmc.Paper(
                                children=[
                                    dmc.Title(dashboard_text.get("dashboard-finance").get("finance-one").get("title")),
                                    dmc.Text(dashboard_text.get("dashboard-finance").get("finance-one").get("subtitle"), size="xs"),
                                    dcc.Graph(id="dashboard-monthly-one")
                                ],
                                shadow="sm",
                                p="sm",
                                withBorder=True,
                            ),
                            span={"base": 12, "sm": 6}
                        ),
                        dmc.GridCol(
                            dmc.Paper(
                                children=[
                                    dmc.Title(dashboard_text.get("dashboard-finance").get("finance-two").get("title")),
                                    dmc.Text(dashboard_text.get("dashboard-finance").get("finance-two").get("subtitle-monthly"), size="xs"),
                                    dcc.Graph(id="dashboard-monthly-two")
                                ],
                                shadow="sm",
                                p="sm",
                                withBorder=True,
                            ),
                            span={"base": 12, "sm": 6}
                        )
                    ]
                ),
                value="monthly"
            )
        ],
        value="weekly",
        orientation="horizontal"
    )
]

layout=dmc.AppShellMain(children=[dmc.Box(id="dashboard-layout")])

@callback(
    Output("dashboard-layout", "children"),
    Input("url", "pathname")
)
def show_dashboard(urls):
    if urls=="/dashboard":
        if session.get("role")=="admin":
            return dashboard_layout
        else:
            return empty_dashboard_layout
    else:
        return "NONE"

@callback(
    Output("data-persistent-consignment", "data"),
    Input("button-refresh-dashboard", "n_clicks"),
    Input("url", "pathname"),
    running=[Output("loading-overlay-dashboard", "visible"), True, False]
)
def update_data(n_clicks, url):
    if n_clicks or url=="/dashboard":
        header, data_consignments=get_data(SPREADSHEET_ID, "Data_Consignment")
        df_consignment=pd.DataFrame(data_consignments, columns=header)
        df_consignment.replace(['', ' '], np.nan, inplace=True)
        df_consignment.fillna(np.nan, inplace=True)
        df_consignment.fillna({"Sold in": "Belum Terkirim/Selesai"}, inplace=True)
        return df_consignment.to_dict("records")
    else:
        return {}

@callback(
    Output("dashboard-one", "figure"),
    Output("dashboard-two", "figure"),
    Output("dashboard-weekly-one", "figure"),
    Output("dashboard-weekly-two", "figure"),
    Output("dashboard-monthly-one", "figure"),
    Output("dashboard-monthly-two", "figure"),
    Input("data-persistent-consignment", "data"),
    Input("daterange-dashboard", "value"),
    running=[Output("loading-overlay-dashboard", "visible"), True, False]
)
def update_dashboard(data, dateranges):
    if data:
        df_consignment=pd.DataFrame(data)
        df_consignment["Consignment Date"]=pd.to_datetime(df_consignment["Consignment Date"])
        df_consignment["Price Seller"]=df_consignment["Price Seller"].apply(price_to_value)
        df_consignment["Price - Sold"]=df_consignment["Price - Sold"].apply(price_to_value)
        df_consignment["Profit"]=df_consignment["Profit"].apply(price_to_value)
        df_consignment["Consignment MonthDate"]=df_consignment["Consignment Date"].apply(lambda d: f"{d.year}-{d.month}")

        # Dashboard 1
        per_status=df_consignment.groupby("Status").count().ID
        per_status=per_status.reindex(["New", "Posted", "Shipped", "Completed", "Completed Elsewhere"])
        new_index=[]
        for status, value in zip(per_status.index, per_status.values):
            val=0 if np.isnan(value) else value
            pcnt=100*val/np.nansum(per_status.values)
            new_index.append(f"{status} ({pcnt:.2f}%)")
        per_status.index=new_index
        fig = go.Figure(data=[go.Bar(x=per_status.values, y=per_status.index, orientation="h", marker_color="#5F967D")])
        fig.update_layout(plot_bgcolor="white", margin=dict(l=20, r=20, t=20, b=20), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        fig.update_yaxes(tickfont=dict(weight="bold"), ticks="outside", ticklen=10, tickcolor="white")
        fig.update_xaxes(showgrid=True, gridcolor="lightgray", griddash="dot")
            
        # Dashboard 2
        per_padel=df_consignment.query("Status in ('Sold', 'Completed', 'Shipped', 'Completed Elsewhere')").groupby("Sold in").count().ID
        per_padel.rename(index={"": "Belum Terkirim/Selesai"}, inplace=True)
        color_map = {
            'Belum Terkirim/Selesai': '#C16759',
            'Terjual di luar': "#841414",
            'Pasar Padel': '#1DDC86',
        }

        figtwo = go.Figure(data=[go.Pie(labels=per_padel.index, values=per_padel.values, marker=dict(colors=[color_map[idx] for idx in per_padel.index]))])
        figtwo.update_layout(plot_bgcolor="white", margin=dict(l=20, r=20, t=20, b=20))

        if not dateranges:
            return fig, figtwo, None, None, None, None


        ###

        df_filtered=df_consignment.where(
            (df_consignment["Consignment Date"]>=dateranges[0])*(df_consignment["Consignment Date"]<=dateranges[1])
        ).dropna(how="all").reset_index(drop=True)
        df_filtered.replace(['', ' '], np.nan, inplace=True)
        df_filtered.fillna(np.nan, inplace=True)

        weeklyfinance=df_filtered.groupby("Consignment Day").agg(
            {
                "Price Seller": "sum",
                "Price - Sold": "sum",
                "Profit": "sum",
            }
        ).reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

        weeklyconsignedsold=df_filtered.groupby("Consignment Day").agg(
            {
                "Price Seller": "count",
                "Price - Sold": "count",
                "Profit": "count",
            }
        ).reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        
        # Dashboard 3
        figweeklyone = go.Figure(data=[
            go.Bar(x=weeklyfinance.index, y=weeklyfinance["Price - Sold"], name ="Omset", marker_color="#B7E2CF"),
            go.Bar(x=weeklyfinance.index, y=weeklyfinance["Profit"], name="Profit", marker_color="#447D63"),
        ])
        figweeklyone.update_layout(plot_bgcolor="white", margin=dict(l=20, r=20, t=20, b=20), yaxis_tickformat=",.0f", yaxis_tickprefix="Rp. ", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        figweeklyone.update_yaxes(tickfont=dict(weight="bold"), ticks="outside", ticklen=10, tickcolor="white")
        figweeklyone.update_xaxes(showgrid=True, gridcolor="lightgray", griddash="dot")

        # Dashboard 4
        figweeklytwo = go.Figure(data=[
            go.Bar(x=weeklyconsignedsold.index, y=weeklyconsignedsold["Price Seller"], name="Consigned", marker_color="#B7E2CF"),
            go.Bar(x=weeklyconsignedsold.index, y=weeklyconsignedsold["Price - Sold"], name="Sold", marker_color="#447D63"),
        ])
        figweeklytwo.update_layout(plot_bgcolor="white", margin=dict(l=20, r=20, t=20, b=20), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        figweeklytwo.update_yaxes(tickfont=dict(weight="bold"), ticks="outside", ticklen=10, tickcolor="white")
        figweeklytwo.update_xaxes(showgrid=True, gridcolor="lightgray", griddash="dot")

        df_filtered["Consignment MonthDate"]=df_filtered["Consignment Date"].apply(lambda d: f"{d.year}-{str(d.month).zfill(2)}")
        monthlyfinance=df_filtered.groupby(["Consignment MonthDate", "Consignment Month"]).agg(
            {
                "Price Seller": "sum",
                "Price - Sold": "sum",
                "Profit": "sum",
            }
        )
        monthlyfinance.sort_values(by="Consignment MonthDate", inplace=True)
        monthlyfinance.reset_index(inplace=True)

        monthlyconsignedsold=df_filtered.groupby(["Consignment MonthDate", "Consignment Month"]).agg(
            {
                "Price Seller": "count",
                "Price - Sold": "count",
                "Profit": "count",
            }
        )
        monthlyconsignedsold.sort_values(by="Consignment MonthDate", inplace=True)
        monthlyconsignedsold.reset_index(inplace=True)
        
        # Dashboard 5
        figmonthlyone = go.Figure(data=[
            go.Bar(x=monthlyfinance["Consignment Month"], y=monthlyfinance["Price - Sold"], name="Omset", marker_color="#B7E2CF"),
            go.Bar(x=monthlyfinance["Consignment Month"], y=monthlyfinance["Profit"], name="Profit", marker_color="#447D63"),
        ])
        figmonthlyone.update_layout(plot_bgcolor="white", margin=dict(l=20, r=20, t=20, b=20), yaxis_tickformat=",.0f", yaxis_tickprefix="Rp. ", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        figmonthlyone.update_yaxes(tickfont=dict(weight="bold"), ticks="outside", ticklen=10, tickcolor="white")
        figmonthlyone.update_xaxes(showgrid=True, gridcolor="lightgray", griddash="dot")

        # Dashboard 6
        figmonthlytwo = go.Figure(data=[
            go.Bar(x=monthlyconsignedsold["Consignment Month"], y=monthlyconsignedsold["Price Seller"], name="Consigned", marker_color="#B7E2CF"),
            go.Bar(x=monthlyconsignedsold["Consignment Month"], y=monthlyconsignedsold["Price - Sold"], name="Sold", marker_color="#447D63"),
        ])
        figmonthlytwo.update_layout(plot_bgcolor="white", margin=dict(l=20, r=20, t=20, b=20), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        figmonthlytwo.update_yaxes(tickfont=dict(weight="bold"), ticks="outside", ticklen=10, tickcolor="white")
        figmonthlytwo.update_xaxes(showgrid=True, gridcolor="lightgray", griddash="dot")

        return fig, figtwo, figweeklyone, figweeklytwo, figmonthlyone, figmonthlytwo
    else:
        return None, None, None, None, None, None