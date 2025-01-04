from shiny.express import module,input, render, ui,expressify
from streamlit import sidebar
from sympy import asec
from scripts_stock.analysis.ui.load_sample_data.load_data_v1 import * 
from shinywidgets import render_widget
import plotly.express as px
import plotly.graph_objects as go
from shiny.ui import output_ui
from shiny import reactive

from scripts_stock.utils.datetime.quater_end import *
from shinywidgets import render_plotly
from scripts_stock.analysis.ui.load_sample_data.load_owner_data import *
from typing import Literal
# fin report - sina owner -> etl

# owner_list = run_get_data_owner_list() 
# owner_list_update_date = owner_list["update_date"].unique().tolist()
# quater_list = get_last_day_of_quarter_range()
# quater_list_in_owner = [x for x in quater_list if x in owner_list_update_date]

owner_sql = OwnerSQl()
owner_list = owner_sql.get_holder_name().main_run()
owner_type_list = owner_sql.get_holder_type().main_run()
#owner_list = owner_sql.get_data_owner()

def get_hold_name_list_v2(holder_type):
    name_list = ['']
    try:
        df2 = owner_sql.get_holder_name_from_type(holder_type).main_run()
        name_list = df2["HOLDER_NAME"].to_list()
        #print(name_list)
    except:
        pass
    return df2,name_list


data_ii = {
    "QFII": ["Apple", "Banana", "Cherry"],
    "投资公司": ["Carrot", "Broccoli", "Spinach"],
    "私募基金": ["Wheat", "Rice", "Corn"]
}


@module
def ui_page2(input, output, session, label="Increment counter22", starting_value=0):
    
    with ui.nav_panel("股本股东沪深300"):
        with ui.layout_sidebar(height=3000,width=60): 
            with ui.sidebar(id="tt232"):
                ui.input_select(
                    "hold_type", "股东类型", choices=owner_type_list["HOLDER_TYPE"].unique().tolist())
                ui.input_text(
                    "input_holder_name", "选择股东", "阿布达比投资局")
            
                # ui.input_select(
                #     "holder", "股东名称", choices=[""])
                ui.input_selectize(
                    "holder", "股东名称", choices=[])
                

                #ui.input_select("quater_end", "Select Quater End", choices=format_dates(quater_list_in_owner))
                #ui.input_select("owner_update_date", "Select date", choices=format_dates(owner_list_update_date))


                ui.input_select(
                "date_test",
                "Select an option below:",
                    {
                        "2024": {"1A": "2024-06-30", "1B": "2024-04-31", "1C": "Choice 1C"},
                        "2023": {"2A": "Choice 2A", "2B": "Choice 2B", "2C": "Choice 2C"},
                    },
                )
                ui.input_text("input_stock_name", "Input_stock_name", "工商银行")
         
            with ui.layout_column_wrap(fill=False, height=1800, width=1):
                with ui.card(full_screen=True):
                    @render.data_frame
                    def table2():
                        try:
                            if input.text() !="":
                                # df2 = get_sample_data_owner(input.var2())
                                # df3 = df2[df2["stock_name"]==input.text().strip()]
                                df3 = get_data_this()
                                return df3
                            if input.var2() != "full":
                                df2 = get_sample_data_owner(input.var2())
                                return df2[df2["update_date"]==input.quater_end()]
                            if input.owner_update_date() == "full":
                                df2 = get_sample_data_owner(input.var2())
                                return df2
                            else:
                                df2 = get_sample_data_owner("sina_owner_keweite")
                                return df2
                        except:
                            df2 = owner_sql.get_data_owner(
                                input.input_holder_name()).main_run()
                            #df2 = run_get_data_v1(owner_sql.sql_str)
                            return df2
                with ui.card():
                    ui.card_header("Holder name table")
                    @render.data_frame
                    def table3():
                        df1,_ = get_hold_name_list_v2(input.hold_type())
                        df2 = df1.sort_values("cnt",ascending=False)
                        return render.DataTable(df2, filters=True, width="800px",
                        # penguins,
                        styles=[
                            # Center the text of each cell (using Bootstrap utility class)
                            {
                                "class": "text-center",
                                "style": {"border": "1px solid black", 
                                          "width":"200px"},
                            },
                            # Bold the first column
                            {
                                "cols": [0],
                                "style": {"font-weight": "bold"},
                            },
                            # Highlight the penguin colors
                            {
                                "rows": [0, 1],
                                "cols": [0],
                                "style": {"background-color": "#ffdbaf"},
                            },
                            {
                                "rows": [2, 3],
                                "cols": [0],
                                "style": {"background-color": "#b1d6d6"},
                            },
                            {
                                "rows": [4, 5],
                                "cols": [0],
                                "style": {"background-color": "#d6a9f2"},
                            },
                        ],
                        )
                    

                # with ui.layout_columns(col_widths=[200,6],row_heights=[1,3]):
                with ui.layout_column_wrap(fill=False, height=900, width=1):
                    with ui.card(full_screen=True,height=6):
                        ui.card_header("Price history")
                        @render_plotly
                        def price_history():
                            # df = get_sample_data_owner(input.var2())
                            # df1 = df[df["stock_name"]=="TCL中环"].sort_values("update_date")

                            # fig = px.line(get_data_this().sort_values("end_date",ascending=True), x='end_date',
                            #               y='hold_num', title='Time Series with Plotly')
                            df1 = get_data_this().sort_values("end_date", ascending=True)
                            x = df1['end_date'].tolist()
                            y = df1['hold_num'].tolist()
                            fig = go.Figure(data=go.Scatter(
                                x=x,
                                y=y,
                                mode='lines+markers'
                            ))
                            fig.update_xaxes(
                                    title={'font': {'size': 18},
                                            'text': 'Date', 'standoff': 10},
                                    automargin=True,
                                )
                            fig.update_yaxes(
                                    
                                    title={'font': {
                                        'size': 18}, 'text': 'Hold Num', 'standoff': 10},
                                    automargin=True,
                                )
                            return fig
                    
                #with ui.layout_columns(col_widths=[200,60],row_heights=[3,10]):
                    with ui.card(full_screen=True):
                        ui.card_header("Hold history")
                        @render_plotly
                        def hold_history():
                            fig = px.line(get_data_this(), x='update_date', y='hold_num', title='Time Series with Plotly')
                            # fig.update_layout(
                            #     hovermode="x unified",
                            #     paper_bgcolor="rgba(0,0,0,0)",
                            #     plot_bgcolor="rgba(0,0,0,0)",
                            # )
                            return fig
                    
    @reactive.calc
    def get_data_this():
        df2 = owner_sql.get_owner_holder_history(
            input.input_holder_name(), input.input_stock_name()).main_run()
        print("2323")
        return df2

    @reactive.effect
    def _():
        choices = input.hold_type() 
        _,name_list = get_hold_name_list_v2(choices)
        ui.update_selectize("holder", choices=name_list)




    # @reactive.calc
    # def get_hold_name_list_v1():
    #     name_list = ['']
    #     try:
    #         df2 = owner_sql.get_holder_name_from_type(
    #             input.hold_type()).main_run()
    #         name_list = df2["HOLDER_NAME"].to_list()
    #         print(name_list)
    #     except:
    #         pass
    #     return name_list
 
        
        

