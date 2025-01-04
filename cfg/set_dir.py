import os
# from scripts_stock.utils.logging_set import *


class ProjectDir():

    """
    Level 1 dir
    """
    current_dir = os.path.abspath(__file__)
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    data_dir = os.path.join(project_dir, "data")
    model_dir = os.path.join(project_dir, "model")

    parse_data_dir = os.path.join(data_dir, "parse_data")
    download_sample_data_dir = os.path.join(data_dir, "download_sample_data")
    download_data_dir = os.path.join(data_dir, "download_data")
    analysis_data_dir = os.path.join(data_dir, "analysis_data")
    log_dir = os.path.join(project_dir, "log")
    database_dir = os.path.join(project_dir, "db")
    """
    Level 2 dir
    """

    parse_data_dir_fuquan = os.path.join(parse_data_dir , "fuquan")
    download_data_dir_fuquan = os.path.join(download_data_dir,"fuquan")

    parse_data_dir_owner_sina = os.path.join(parse_data_dir,"owner_sina")
    download_data_dir_owner_sina = os.path.join(download_data_dir,"owner_sina")

    parse_data_dir_owner_dfcf = os.path.join(parse_data_dir,"owner_dfcf")
    download_data_dir_owner_dfcf = os.path.join(download_data_dir,"owner_dfcf")

    download_data_dir_cash_flow = os.path.join(download_data_dir,"cash_flow")
    parse_data_dir_cash_flow = os.path.join(parse_data_dir,"cash_flow")

    download_data_dir_fin_report = os.path.join(download_data_dir,"fin_report")
    parse_data_dir_fin_report = os.path.join(parse_data_dir,"fin_report")

    download_data_dir_hs300 = os.path.join(download_data_dir,"hs300")
    parse_data_dir_hs300 = os.path.join(parse_data_dir,"hs300")

    download_data_owner_dfcf = os.path.join(download_data_dir,"owner_dfcf")
    parse_data_owner_dfcf = os.path.join(parse_data_dir,"owner_dfcf")

    download_data_dir_bankuai_cash_flow = os.path.join(download_data_dir, "cash_flow","bankuai")
    parse_data_dir_bankuai_cash_flow = os.path.join(
        parse_data_dir, "cash_flow", "bankuai")
    
    download_data_dir_hangye_cash_flow = os.path.join(
        download_data_dir, "cash_flow", "hangye")
    parse_data_dir_hangye_cash_flow = os.path.join(
        parse_data_dir, "cash_flow", "hangye")

    """
    Level 2 dir
    """
    parse_data_dir_fuquan_all = os.path.join(parse_data_dir,"fuquan","all")
    download_data_dir_fuquan_all = os.path.join(download_data_dir,"fuquan","all")

    download_profit_data_dir = os.path.join(download_data_dir_fin_report,"profit_data")
    parse_data_dir_profit_data = os.path.join(parse_data_dir_fin_report,"profit_data")

    download_basic_data_dir = os.path.join(download_data_dir_fin_report, "basic_data")
    parse_data_basic_dir = os.path.join(parse_data_dir_fin_report, "basic_data")
    @staticmethod
    def tt():
        return os.path.abspath(__file__)
    
    @staticmethod
    def create_dir(dir_input):
        # if the demo_folder directory is not present 
        # then create it.
        import os
        if not os.path.exists(dir_input):
            os.makedirs(dir_input)
            print(f"====== create dir {dir_input} =======")

    @staticmethod
    def create_data_folder():
        for folders in ProjectDir.__dict__.keys():
            dir_in = ProjectDir.__dict__[folders]
            #print(dir_in)
            try:
                if "vscode" in dir_in:
                    try:
                        ProjectDir.create_dir(dir_in)
                    except:
                        pass
                        print(dir_in)
            except:
                pass
                print(" not a folder")

if __name__ == '__main__':
    #ProjectDir.create_dir(ProjectDir.parse_data_dir_cash_flow)
    #print(ProjectDir.download_data_dir_cash_flow)
    ProjectDir().create_data_folder()
    print(ProjectDir.project_dir)
    #print(ProjectDir.__dict__.keys())
    """
    for aa in ProjectDir.__dict__.keys():
    #print(ProjectDir.__dict__[aa])
    dir_in = ProjectDir.__dict__[aa]
    try:
        if "vscode" in dir_in:
            CommonScript.create_dir(dir_in)
            print(dir_in)
    except:
        pass
    """
