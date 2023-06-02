import os

current_dir = os.path.abspath(__file__)
project_dir = os.path.abspath(r"../")
data_dir = os.path.join(project_dir,"data")
parse_data_dir = os.path.join(data_dir,"parse_data")
download_data_dir = os.path.join(data_dir,"download_sample_data")


print(download_data_dir)