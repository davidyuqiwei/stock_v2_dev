from shiny.express import module,input, render, ui,expressify
from streamlit import sidebar
from scripts_stock.analysis.ui.load_sample_data.load_data_v1 import * 
from shinywidgets import render_widget
import plotly.express as px

from shiny.ui import output_ui
from shiny import reactive


@module
def ui_page1(input, output, session, label="Increment counter", starting_value=0):
    df_daily_kdj_last, df_weekly_kdj_last, df_weekly_kdj_last5 = get_sample_data()
    #ui.page_opts(title="Stock explorer", fillable=True)

    with ui.nav_panel("MACD_KDJ排名-短线"):
        with ui.layout_sidebar(height=3000,width=60): 
            with ui.sidebar(id="t1",width=300):
                ui.input_select("var", "Select variable", choices=[ "important_kpi","full_data","test"])
                ui.input_date_range("daterange", "Date range", start="2020-01-01")  
                ui.input_select(
                    "select",
                    "Select an option below:",
                    {
                        "1": {"1A": "Choice 1A", "1B": "Choice 1B", "1C": "Choice 1C"},
                        "2": {"2A": "Choice 2A", "2B": "Choice 2B", "2C": "Choice 2C"},
                    },
                )
            with ui.layout_column_wrap(fill=False):
                with ui.value_box(showcase=output_ui("232"),heigh=200):
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
                    
            with ui.layout_column_wrap(fill=False, width=1,height=600):
                with ui.card(height=3):
                    ui.card_header("Daily KJD MACD")
                    @render.data_frame
                    def table():
                        if input.var() == "important_kpi":
                            df_back = df_daily_kdj_last[["stock_index", "stock_name", "kdjj", "macdh"]].sort_values(
                                "kdjj")
                            return render.DataTable(df_back, filters=True)
                        else:
                            return render.DataTable(df_daily_kdj_last, filters=True)
                        
            with ui.layout_column_wrap(fill=False, height=600):
                    with ui.card():
                        ui.card_header("Weekly KJD MACD")
                        @render.data_frame
                        def table_weekly():
                            if input.var() == "important_kpi":
                                df_back = df_weekly_kdj_last[[
                                    "date", "stock_index", "stock_name", "kdjj", "macdh"]].sort_values("kdjj")
                                return render.DataTable(df_back, filters=True)
                            else:
                                return render.DataTable(df_weekly_kdj_last, filters=True)
                    
                    with ui.card():
                        ui.card_header("Weekly KJD MACD - Last 5 week")
                        @render.data_frame
                        def table_weekly_last5():
                            if input.var() == "important_kpi":
                                df_back = df_weekly_kdj_last5[[
                                    "date", "stock_index", "stock_name", "kdjj", "macdh"]].sort_values("kdjj")
                                return render.DataTable(df_back, filters=True)
                            else:
                                return render.DataTable(df_weekly_kdj_last5, filters=True)
                        






#     count = reactive.value(starting_value)
#     @reactive.effect
#     @reactive.event(input.button)
#     def _():
#         count.set(count() + 1)

# @module
# def counter_express(input, output, session, label="Increment counter", starting_value=0):
#     count = reactive.value(starting_value)
#     with ui.card():
#         ui.card_header("This is " + label)
#         ui.input_action_button(id="button", label=label)

#         @render.code
#         def out():
#             return f"Click count is {count()}"

#     @reactive.effect
#     @reactive.event(input.button)
#     def _():
#         count.set(count() + 1)