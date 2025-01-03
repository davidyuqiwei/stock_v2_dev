from shiny.express import module, input, render, ui, expressify
from streamlit import sidebar
from scripts_stock.analysis.ui.load_sample_data.load_fin_report_data import *
from shinywidgets import render_widget
import plotly.express as px

from shiny.ui import output_ui
from shiny import reactive

from scripts_stock.utils.datetime.quater_end import *
from shinywidgets import render_plotly
from scripts_stock.analysis.ui.load_sample_data.load_data_v1 import *


@module
def ui_page4(input, output, session, label="cash_flow", starting_value=0):

    with ui.nav_panel("个股财务报表"):
        with ui.layout_sidebar(height=1000, width=60):
            with ui.sidebar(id="tt231"):
                ui.input_select(
                    "fin_data_type", "财务指标", choices=['BASIC_EPS', 'TOTAL_OPERATE_INCOME',
                                        'PARENT_NETPROFIT', 'XSMLL', 'WEIGHTAVG_ROE', 'BPS', 'MGJYXJJE'])
                
                ui.input_text("stock_index", "Input_stock_name", "601398")

            with ui.layout_column_wrap(fill=False, height=800, width=1):
                    # width=1 每行一个, width=1/3 每行3个card

                with ui.card(full_screen=True):
                    ui.card_header("长江电力-财务报表")

                    @render_plotly
                    def plt_fin_data():
                        # df = get_sample_data_owner(input.var2())
                        # df1 = df[df["stock_name"]=="TCL中环"].sort_values("update_date")
                        df1 = get_fin_report_stocks_benchmark()
                        
                        fig = plot_fin_data(df1)
                        return fig
                  
                with ui.card(full_screen=True):                    
                    ui.card_header("Fin Report compare")

                    @render_plotly
                    def plt_fin_data_compare():
                        # df = get_sample_data_owner(input.var2())
                        # df1 = df[df["stock_name"]=="TCL中环"].sort_values("update_date")
                        df1 = get_fin_report_stocks()
                        
                        fig = plot_fin_data(df1)
                        return fig

    @reactive.calc
    def get_fin_report_stocks_benchmark():
        # )
        df2 = load_fin_report_data()
        # default_col_name = "super_large_order_net_inflow_amount"
        df3 = df2.sort_values("report_date")
        # print(df3)
        return df3
    
    @reactive.calc
    def get_fin_report_stocks():
        #)
        df2 = load_fin_report_data(input.stock_index())
        # default_col_name = "super_large_order_net_inflow_amount"
        df3 = df2.sort_values("report_date")
        #print(df3)
        return df3
    

    def col_trans():
        fin_report_columns = {
            "BASIC_EPS": "每股收益",  # 每股收益的实际数值应放在这里
            "TOTAL_OPERATE_INCOME": "营业总收入",  # 营业总收入的实际数值应放在这里
            "PARENT_NETPROFIT": "净利润",  # 净利润的实际数值应放在这里
            "XSMLL": "销售毛利率",  # 销售毛利率的实际数值应放在这里
            "WEIGHTAVG_ROE": "净资产收益率",  # 净资产收益率的实际数值应放在这里
            "BPS": "每股净资产",  # 每股净资产的实际数值应放在这里
            "MGJYXJJE": "每股经营现金流" # 每股经营现金流的实际数值应放在这里
        }
        selected_column = fin_report_columns.get(
            input.fin_data_type())
        return selected_column
    

    def plot_fin_data(df1):
        stock_name = df1["stock_name"].values[0]
        fig = px.line(df1, x='report_date',
                      y=input.fin_data_type(), title=stock_name+'财务报表')

        fig.update_xaxes(
            title={'font': {'size': 18},
                   'text': 'Date', 'standoff': 10},
            automargin=True,
        )
        fig.update_yaxes(
            title={'font': {
                'size': 18}, 'text': col_trans(), 'standoff': 10},
            automargin=True,
        )
        return fig
    
    def plot_fin_data_v2(df1):
        fig = px.line(df1, x='report_date',
                      y=input.fin_data_type(), title='个股财务报表')

        fig.update_xaxes(
            title={'font': {'size': 18},
                   'text': 'Date', 'standoff': 10},
            automargin=True,
        )
        fig.update_yaxes(

            title={'font': {
                'size': 18}, 'text': input.fin_data_type(), 'standoff': 10},
            automargin=True,
        )
        return fig
