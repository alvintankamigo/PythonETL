import os
from unittest import TestCase
from util.file_util import get_dir_files_list, get_new_by_compare_list, get_new_by_compare_list2


class TestFileUtil(TestCase):
    def setUp(self):  # 當單元測試函數啟動前會調用
        # os.getcwd()  # 當前文件的路徑
        # os.path.dirname(dir_names)  # 當前文件的父路徑
        self.project_root_path = os.path.dirname(os.getcwd())
        pass

    def test_get_dir_files_list(self):
        # 測試recursive 關閉的狀態
        result1 = get_dir_files_list(path=self.project_root_path + '/' + 'test_dir', recursive=False)
        predict_result = ['1', '2']
        result = []
        for p in predict_result:
            result.append(self.project_root_path + '/' + 'test_dir/' + p)
        result1.sort()
        result.sort()
        self.assertEqual(result1, result)
        # 測試recursive 開啟的狀態
        result2 = get_dir_files_list(path=self.project_root_path + '/' + 'test_dir', recursive=True)
        # print(result2)
        predict_result = ['1', '2', 'inner1/3', 'inner1/4', 'inner1/inner2/5']
        result = []
        for p in predict_result:
            result.append(self.project_root_path + '/' + 'test_dir/' + p)
        result2 = result2.sort()
        result = result.sort()
        self.assertEqual(result2, result)
        print(result)

    def test_get_new_by_compare_list(self):
        """測試get_new_by_compare_list的方法"""
        a_list = ['e:/a.txt', 'e:/b.txt', 'e:/c.txt', 'e:/d.txt', 'e:/e.txt']
        b_list = ['e:/a.txt', 'e:/b.txt']
        result1 = get_new_by_compare_list(a_list, b_list).sort()
        expected = ['e:/c.txt', 'e:/d.txt', 'e:/e.txt'].sort()
        self.assertEqual(result1, expected)

    def test_get_new_by_compare_list2(self):
        a_list = ['e:/a.txt', 'e:/b.txt', 'e:/c.txt', 'e:/d.txt', 'e:/e.txt']
        b_list = ['e:/a.txt', 'e:/b.txt']
        result1 = get_new_by_compare_list(a_list, b_list).sort()
        expected = ['e:/c.txt', 'e:/d.txt', 'e:/e.txt'].sort()
        self.assertEqual(result1, expected)

    def tearDown(self):
        pass
