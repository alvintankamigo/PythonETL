"""
將時間戳轉換為字符串格式
"""
import time


def ts10_to_date_str(ts, formate='%Y-%m-%d %H:%M:%S'):
    """
    將10位數字的時間戳轉換為時間格式的字符串
    :param ts: 要轉換的時間戳
    :param formate: 轉換的格式
    :return: 轉換好的時間格式字符串
    """
    # 將時間戳轉換為時間數組
    time_array = time.localtime(ts)
    return time.strftime(formate, time_array)


def ts13_to_date_str(ts, formate='%Y-%m-%d %H:%M:%S'):
    """
    將13位數字的時間戳轉換為時間格式的字符串
    :param ts:
    :param formate:
    :return:
    """
    # todo:如果輸入的時間單位小於13位給警告訊息
    if ts<1000000000000:
        print('時間格式不太對')
    ts10 = int(ts/1000)
    return ts10_to_date_str(ts10, formate)
