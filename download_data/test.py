import sys
import traceback


def print_exception_info():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print("Exception Type:", exc_type)
    print("Exception Message:", exc_value)

    # 获取回溯对象中的帧列表
    tb_frames = traceback.extract_tb(exc_traceback)

    for frame in tb_frames:
        filename, line_number, function_name, text = frame
        print(
            f'File: {filename}, Line: {line_number}, In Function: {function_name}')
        print(f'  {text}')

def tt():
    print(1/0)


try:
    # 可能引发异常的代码
    tt()  # 示例：除零错误
except Exception:
    print_exception_info()
