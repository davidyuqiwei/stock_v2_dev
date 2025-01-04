from email.charset import add_alias
from shiny.express import module, input, render, ui, expressify
from streamlit import sidebar
from scripts_stock.analysis.ui.load_sample_data.load_data_v1 import *
from shinywidgets import render_widget
import plotly.express as px

from shiny.ui import output_ui
from shiny import reactive
from scripts_stock.analysis.ui.fun_data_health_check.data_check_v1 import *
from scripts_stock.analysis.ui.fun_data_health_check.data_check_prod import *

from scripts_stock.analysis.ui.shiny_v1.cfg_p0 import *


@module
def ui_page0(input, output, session, label="Increment counter", starting_value=0):
    df_daily_kdj_last, df_weekly_kdj_last, df_weekly_kdj_last5 = get_sample_data()
    # ui.page_opts(title="Stock explorer", fillable=True)

    with ui.nav_panel("Data Table Health"):
        with ui.layout_sidebar(height=3000, width=60):
            with ui.sidebar(id="t1", width=300):
                ui.input_select("var", "Select variable", choices=DataCheck().all_table)
                ui.input_date_range(
                    "daterange", "Date range", start="2020-01-01")
                ui.input_select(
                    "select",
                    "Select an option below:",
                    print_sample_data_json
                )
            with ui.layout_column_wrap(fill=False):
                with ui.value_box(showcase=output_ui("232"), heigh=200):
                    "Data Update Time"

                    @render.ui
                    def change2():
                        stock_date = str(
                            df_daily_kdj_last["update_time"].unique()[0])
                        return stock_date[0:10]

                with ui.value_box(showcase=output_ui("change_icon")):
                    "Data Date"

                    @render.ui
                    def change():
                        stock_date = str(df_daily_kdj_last["date"].unique()[0])
                        return stock_date
                    
            with ui.layout_column_wrap(fill=False, width=1, height=400):
                with ui.card(height=1):
                    ui.card_header("Prod DB table check")

                    @render.data_frame
                    def table_prod1():
                        df1, _ = DataCheckProd().main_run()
                        return df1

                with ui.card():
                    ui.card_header("Prod DB table check v2")

                    @render.data_frame
                    def table_prod2():
                        _, df2 = DataCheckProd().main_run()
                        return df2

            with ui.layout_column_wrap(fill=False, width=1, height=600):
                with ui.card(height=1):
                    ui.card_header("Test DB table check")

                    @render.data_frame
                    def table1():
                        df1, _ = DataCheck().main_run()
                        return df1

            
                with ui.card():
                    ui.card_header("Test DB table check v2")

                    @render.data_frame
                    def table_weekly():
                        _, df2 = DataCheck().main_run()
                        return df2
                    
            with ui.layout_column_wrap(fill=False, width=1, height=400):
                with ui.card(height=200):
                    ui.card_header("Data Sample")

                    @render.data_frame
                    def table_weekly_last5():
                        return DataCheck.sample_data(input.select())
                            

                    
