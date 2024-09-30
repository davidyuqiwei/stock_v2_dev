import os

def delete_files_in_folder(directory,file_type=".txt",if_print=False):
    # 遍历指定的目录
    for filename in os.listdir(directory):
        # 检查文件是否是.txt文件
        if filename.endswith(file_type):
            file_path = os.path.join(directory, filename)
            try:
                # 尝试删除文件
                os.remove(file_path)
                if if_print:
                    print(f"Deleted {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

