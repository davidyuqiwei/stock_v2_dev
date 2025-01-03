from scripts_stock.analysis.ui.shiny_v1.page4 import *
from shiny.express import input, render, ui
from streamlit import sidebar
from scripts_stock.analysis.ui.load_sample_data.load_data_v1 import * 
from shinywidgets import render_widget
import plotly.express as px

from shiny.ui import output_ui


df1 = get_sample_data()
ui.page_opts(title="Stock explorer", fillable=False)
#ui = ui_page1(ui)

from scripts_stock.analysis.ui.shiny_v1.page0 import ui_page0
ui_page0("w0")

from scripts_stock.analysis.ui.shiny_v1.page1 import ui_page1
ui_page1("ww")
from scripts_stock.analysis.ui.shiny_v1.page2 import *
ui_page2("www")

from scripts_stock.analysis.ui.shiny_v1.page3 import *
ui_page3("www3")

from scripts_stock.analysis.ui.shiny_v1.page4 import *
ui_page4("www4")

#get_data_this()from scripts_stock.analysis.ui.shiny_v1.page4 import *


#ui_page1("1")
