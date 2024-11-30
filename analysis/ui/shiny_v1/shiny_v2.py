from shiny.express import input, render, ui
from streamlit import sidebar
from scripts_stock.analysis.ui.load_sample_data.load_data_v1 import * 
from shinywidgets import render_widget
import plotly.express as px



df1 = get_sample_data()

with ui.nav_panel("Table"):
    with ui.layout_sidebar(height=3000): 
        with ui.sidebar(id="t1"):
            ui.input_select("var", "Select variable", choices=[ "important_kpi","full_data"])
            ui.input_date_range("daterange", "Date range", start="2020-01-01")  
            ui.input_select(
                "select",
                "Select an option below:",
                {
                    "1": {"1A": "Choice 1A", "1B": "Choice 1B", "1C": "Choice 1C"},
                    "2": {"2A": "Choice 2A", "2B": "Choice 2B", "2C": "Choice 2C"},
                },
            )

        with ui.card():
            @render.data_frame
            def table():
                if input.var() == "important_kpi":
                    return df1[["stock_index","stock_name","kdjj","macdh"]]
                else:
                    return df1


with ui.nav_panel("Table2"):
    with ui.sidebar(id="tt"):
        ui.input_select("var2", "Select variable", choices=[ "important_kpi2","full_data2"])
        
    @render.data_frame
    def table2():
        if input.var() == "important_kpi":
            return df1[["stock_index","stock_name","kdjj","macdh"]]
        else:
            return df1
