from shiny.express import input, render, ui
from streamlit import sidebar
from scripts_stock.analysis.ui.load_sample_data.load_data_v1 import * 
from shinywidgets import render_widget
import plotly.express as px

from shiny.ui import output_ui





df1 = get_sample_data()
ui.page_opts(title="Stock explorer", fillable=True)
#ui = ui_page1(ui)
from scripts_stock.analysis.ui.shiny_v1.page1 import ui_page1,counter_express

ui_page1("counter1", label="Counter 1 (Express)", starting_value=5)
#ui_page1("1")
"""
with ui.nav_panel("Table"):
    with ui.layout_sidebar(height=3000): 
        with ui.sidebar(id="t1"):
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
                    stock_date = str(df1["update_time"].unique()[0])
                    return stock_date
                
            with ui.value_box(showcase=output_ui("change_icon")):
                "Data Date"
                
                @render.ui
                def change():
                    stock_date = str(df1["date"].unique()[0])
                    return stock_date

        with ui.card():
            @render.data_frame
            def table():
                if input.var() == "important_kpi":
                    return df1[["stock_index","stock_name","kdjj","macdh"]]
                else:
                    return df1
"""

"""

"""
