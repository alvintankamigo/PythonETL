"""
定義字符串處理工具(因為總不能再要插入數據庫中時是插入空值)
"""


def check_null(data: str):
    """
    檢查字符串的內容是否為無意義內容，如果是則回傳true,反之false
    無意義內容定義：None,Null,undefined
    :param data: 傳入的字符串
    :return: true,false
    """
    # 如果是空的，完全是沒有的，不存在的，回傳true
    if not data:
        return True
    # 轉換為小寫None ->none
    data = data.lower()  # 如果data不是字串就不會有lower()函數
    # 去空格
    data = data.strip()
    if data == 'none' or data == '' or data == 'undefined' or data == 'null':
        return True
    return False


def check_str_null_and_transform_to_sql_null(data):
    """
    插入的數據對應的sql值是否為無意義內容，若是則為Null,反之則在字串的兩側加上單引號
    :param data:
    :return:
    """
    # 進入這個分支，代表內容無意義
    if check_null(str(data)):  # 必須確認傳進來的東西是字串，例如member_id應該要是字串但他是數字，就有可能是用int表示，所以要轉換
        return "null"
    else:
        # 內容有意義，就返回內容本身
        return f"'{data}'"  # 同上面一樣的道理


def clean_str(data: str):
    if check_null(data):
        return data
    data = data.replace("'", "")
    data = data.replace('"', "")
    data = data.replace("\\", "")
    data = data.replace('@', '')
    data = data.replace(',', '')
    data = data.replace(';', '')
    return data


def check_number_null_and_transform_to_sql_null(data):
    """檢查數字是否是空的，如果是空的則返回Null"""
    if data and not check_null(str(data)):
        return data
    return "null"
