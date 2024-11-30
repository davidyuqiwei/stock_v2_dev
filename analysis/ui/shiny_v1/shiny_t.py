from shiny.express import input, render, ui
from scripts_stock.analysis.ui.load_sample_data.load_data_v1 import * 
from shinywidgets import render_widget
import plotly.express as px


df1 = get_sample_data()
# print(df1.head(10))


ui.page_opts(title="David Yu's Stock Dashboard", fillable=True)
# ui.input_slider("val", "Slider label", min=0, max=100, value=50)

# @render.text
# def slider_val():
#     return f"Slider value: {input.val()}"

with ui.sidebar():
    ui.input_select("var", "Select variable", choices=[ "important_kpi","full_data"])

    ui.input_checkbox_group(  
            "checkbox_group",  
            "Checkbox group",  
            {  
                "a": "A",  
                "b": "B",  
                "c": "C",  
            },  
        )  
    
    ui.input_date_range("daterange", "Date range", start="2020-01-01")  


    ui.input_select(
    "select",
    "Select an option below:",
    {
        "1": {"1A": "Choice 1A", "1B": "Choice 1B", "1C": "Choice 1C"},
        "2": {"2A": "Choice 2A", "2B": "Choice 2B", "2C": "Choice 2C"},
    },
    )

# @render.data_frame
# def head():
#     return df1[["stock_index", input.var()]]


with ui.nav_panel("Table"):
    @render.data_frame
    def table():
        if input.var() == "important_kpi":
            return df1[["stock_index","stock_name","kdjj","macdh"]]
        else:
            return df1

# with ui.card(full_screen=True):
# ui.card_header("important index")
# @render.plot
# def plot():
#     import matplotlib.pyplot as plt
#     return df1[["stock_index","stock_name"]]


# with ui.sidebar():
#     ui.input_checkbox_group(  
#         "checkbox_group",  
#         "Checkbox group",  
#         {  
#             "a": "A",  
#             "b": "B",  
#             "c": "C",  
#         },  
#     )  


    

with ui.nav_panel("Table2"):
    @render_widget
    def hist():
        print("=========================")
        print(input.var())
        return px.histogram(df1[["kdjj"]], input.var())
    
    # @render.text
    # def value():
    #     return ", ".join(input.checkbox_group())
