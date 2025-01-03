from shiny.express import module,input, render, ui,expressify
from streamlit import sidebar
from scripts_stock.analysis.ui.load_sample_data.load_data_v1 import * 
from shinywidgets import render_widget
import plotly.express as px

from shiny.ui import output_ui
from shiny import reactive

from scripts_stock.utils.datetime.quater_end import *
from shinywidgets import render_plotly

# fin report - sina owner -> etl

owner_list = run_get_data_owner_list() 
owner_list_update_date = owner_list["update_date"].unique().tolist()
quater_list = get_last_day_of_quarter_range()
quater_list_in_owner = [x for x in quater_list if x in owner_list_update_date]
@module
def ui_page2(input, output, session, label="Increment counter22", starting_value=0):
    
    with ui.nav_panel("股本股东沪深300"):
        with ui.layout_sidebar(height=3000,width=60): 
            with ui.sidebar(id="tt232"):
                ui.input_select("var2", "选择股东", choices=owner_list["owner_name"].unique().tolist()+["full"])
                ui.input_select("quater_end", "Select Quater End", choices=format_dates(quater_list_in_owner))
                ui.input_select("owner_update_date", "Select date", choices=format_dates(owner_list_update_date))


                ui.input_select(
                "date_test",
                "Select an option below:",
                    {
                        "2024": {"1A": "2024-06-30", "1B": "2024-04-31", "1C": "Choice 1C"},
                        "2023": {"2A": "Choice 2A", "2B": "Choice 2B", "2C": "Choice 2C"},
                    },
                )
                ui.input_text("text", "Input_stock_name", "")  
            with ui.layout_columns(col_widths=[200,60],row_heights=[3,10]):
                with ui.card():
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
                            df2 = get_sample_data_owner("sina_owner_keweite")
                            return df2
                        
                #with ui.layout_columns(col_widths=[200,6],row_heights=[1,3]):
                with ui.layout_column_wrap(fill=False):
                    with ui.card(full_screen=True,height=6):
                        ui.card_header("Price history")
                        @render_plotly
                        def price_history():
                            # df = get_sample_data_owner(input.var2())
                            # df1 = df[df["stock_name"]=="TCL中环"].sort_values("update_date")
                            fig = px.line(get_data_this(), x='update_date', y='cash_hold', title='Time Series with Plotly')
                            # fig.update_layout(
                            #     hovermode="x unified",
                            #     paper_bgcolor="rgba(0,0,0,0)",
                            #     plot_bgcolor="rgba(0,0,0,0)",
                            # )
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
        df2 = get_sample_data_owner(input.var2())
        df3 = df2[df2["stock_name"]==input.text().strip()].sort_values("update_date")
        print("2323")
        return df3


