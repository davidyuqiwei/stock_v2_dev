from shiny.express import module, input, render, ui, expressify
from streamlit import sidebar
from scripts_stock.analysis.ui.load_sample_data.load_data_cash_flow import *
from shinywidgets import render_widget
import plotly.express as px

from shiny.ui import output_ui
from shiny import reactive

from scripts_stock.utils.datetime.quater_end import *
from shinywidgets import render_plotly
from scripts_stock.analysis.ui.load_sample_data.load_data_v1 import *


owner_list = run_get_data_owner_list()
owner_list_update_date = owner_list["update_date"].unique().tolist()
quater_list = get_last_day_of_quarter_range()
quater_list_in_owner = [x for x in quater_list if x in owner_list_update_date]


@module
def ui_page3(input, output, session, label="cash_flow", starting_value=0):

    with ui.nav_panel("cash_flow_data_v1"):
        with ui.layout_sidebar(height=1000, width=60):
            with ui.sidebar(id="tt231"):
                ui.input_select(
                    "cash_flow_type", "资金类型", choices=["超大单","大单","中单","小单"])
                # ui.input_select("quater_end", "Select Quater End",
                #                 choices=format_dates(quater_list_in_owner))
                # ui.input_select("owner_update_date", "Select date",
                #                 choices=format_dates(owner_list_update_date))

                # ui.input_select(
                #     "date_test",
                #     "Select an option below:",
                #     {
                #         "2024": {"1A": "2024-06-30", "1B": "2024-04-31", "1C": "Choice 1C"},
                #         "2023": {"2A": "Choice 2A", "2B": "Choice 2B", "2C": "Choice 2C"},
                #     },
                # )
                ui.input_text("text", "Input_stock_name", "601398")

            with ui.layout_column_wrap(fill=False, width=1/2, height=300):
                with ui.card(height=200):
                    @render.data_frame
                    def table2():
                        try:
                            if input.cash_flow_type() != "":
                                # df2 = get_sample_data_owner(input.var2())
                                # df3 = df2[df2["stock_name"]==input.text().strip()]
                                df2 , _ = get_data_this()
                                return df2
                            if input.var2() != "full":
                                df2 = get_sample_data_owner(input.var2())
                                return df2[df2["update_date"] == input.quater_end()]
                            if input.owner_update_date() == "full":
                                df2 = get_sample_data_owner(input.var2())
                                return df2
                            else:
                                df2 = get_sample_data_owner(
                                    "sina_owner_keweite")
                                return df2
                        except:
                            df2 = get_sample_data_owner("sina_owner_keweite")
                            return df2
                        
                with ui.card(height=200):
                    @render.data_frame
                    def table3():
                        df2 = get_cash_flow_ratio_significant()
                        return df2
                    
            with ui.layout_column_wrap(fill=False, height=600, width=1):
                # width=1 每行一个, width=1/3 每行3个card
            
                with ui.card(full_screen=True):
                    ui.card_header("Cash flow")

                    @render_plotly
                    def plt_cash_flow():
                        # df = get_sample_data_owner(input.var2())
                        # df1 = df[df["stock_name"]=="TCL中环"].sort_values("update_date")
                        df1,col_name = get_data_this()
                        fig = plot_cash_flow(df1, col_name)
                        return fig
                    
                with ui.card(full_screen=False, height=5):
                    ui.card_header("Cash Flow Ratio")
                    @render_plotly
                    def plot_cash_flow_ratio_in():
                        df1 = get_cash_flow_ratio()
                        fig = plot_fig_cash_flow_ratio(df1)
                        return fig
                    


    @reactive.calc
    def get_data_this():
        df2 = get_sample_cash_flow(int(input.text()))
        #default_col_name = "super_large_order_net_inflow_amount"
        cash_flow_columns = {
            '小单': "small_order_net_inflow_amount",
            '超大单': "super_large_order_net_inflow_amount",
            '大单': "large_order_net_inflow_amount",
            "中单": "medium_order_net_inflow_amount",
        }
        selected_column = cash_flow_columns.get(
            input.cash_flow_type())
        df3 = df2[["stock_index", "date", selected_column]].drop_duplicates()
        return df3, selected_column


    @reactive.calc
    def get_cash_flow_ratio():
        df2 = get_sample_cash_flow_ratio(int(input.text()))
        df3 = df2[["stock_index", "date",
                   "super_large_order_net_inflow_amount_ratio"]].drop_duplicates()
        return df3
    
    @reactive.calc
    def get_cash_flow_ratio_significant():
        df3 = get_ample_cash_flow_ratio_recent()
        return df3

    def plot_cash_flow(df1,col_name):
        fig = px.line(df1, x='date',
                    y=col_name, title='个股资金流')

        fig.update_xaxes(
            title={'font': {'size': 18},
                    'text': 'Date', 'standoff': 10},
            automargin=True,
        )
        fig.update_yaxes(
            
            title={'font': {
                'size': 18}, 'text': col_name, 'standoff': 10},
            automargin=True,
        )
        return fig
    

    def plot_fig_cash_flow_ratio(df1):
        fig = px.line(df1, x='date',
                      y="super_large_order_net_inflow_amount_ratio", title='个股资金流')

        fig.update_xaxes(
            title={'font': {'size': 18},
                   'text': 'Date', 'standoff': 10},
            automargin=True,
        )
        fig.update_yaxes(

            title={'font': {
                'size': 18}, 'text': "super_large_order_net_inflow_amount_ratio", 'standoff': 10},
            automargin=True,
        )
        return fig