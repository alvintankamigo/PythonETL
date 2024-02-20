import os


def get_dir_files_list(path, recursive=False):
    """
    獲取指定路徑下面的所有文件名
    :param path:  指定路徑（絕對值路徑）
    :param recursive: 是否要遞歸
    :return: 指定路徑下面的文件名稱列表
    """
    dirs_name = os.listdir(path)
    files = []
    for dir_name in dirs_name:
        absolute_path = f"{path}/{dir_name}"

        if not os.path.isdir(absolute_path):
            files.append(absolute_path)
        else:
            if recursive:
                recursive_file_list = get_dir_files_list(absolute_path, recursive=True)
                files += recursive_file_list
    return files


def get_new_by_compare_list(a_list, b_list):
    """
    # 比較兩個list之間的差異 目的：找出還未處理過的文件
    :param a_list:
    :param b_list:
    :return: 返回一個新的list (沒有被處理過的文件)
    """
    # 在a_list中且不在b_list中的元素
    return list(set(a_list) - set(b_list))





