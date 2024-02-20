from unittest import TestCase
from util.mysql_util import MysqlUtil, get_processed_file
from util.logger_util import init_logger
import config.project_config as config

logger = init_logger()


class TestMysqlUtil(TestCase):
    """
    許多單元測試經常藬用相同的測試設備，你可以在 TestCase 的子類別中定義 setUp 與 tearDown 方法，測試執行器會在每個測試運行之前執行 setUp 方法，每個測試運行之後執行 tearDown 方法。
    """

    def setUp(self):
        self.mysql_util = MysqlUtil()  # 默認連接的是metadata
        pass

    def test_execute_with_commit(self):
        # 選擇要用來測試的數據庫
        self.mysql_util.select_db('test')
        #
        self.mysql_util.execute_with_commit(
            'drop table if exists unittest_table '
        )
        # 創建表格
        if not self.mysql_util.check_table_exists('test', 'unittest_table'):
            self.mysql_util.create_table('test', 'unittest_table', 'id int primary key, name varchar(255)')
        else:
            logger.debug('表已經存在')

        # 插入數據
        self.mysql_util.execute_with_commit(
            'insert into unittest_table values (1,"danny"),(2,"mark")'
        )
        # 查詢數據
        result = self.mysql_util.query('select * from unittest_table')
        print(result)
        # 斷言
        self.assertEqual(result, ((1, 'danny'), (2, 'mark')))  # 查詢的結果是元組
        # 刪除 unittest_table
        self.mysql_util.execute_with_commit(
            'drop tables unittest_table'
        )
        # 關閉數據庫
        self.mysql_util.close()
        pass

    def test_execute_without_commit(self):
        # 在程式碼中設置mysql為自動提交
        # 每次執行完之後都會自動提交，不需要建立對象去提交
        self.mysql_util.conn.autocommit(True)
        # 選擇要用來測試的數據庫
        self.mysql_util.select_db('test')
        # 有可能上次測試執行失敗，導致最後面的drop table語句沒有執行到，當要再次測試時，想要再插入數據就會插不進去
        # 所以要在前面把表刪掉。當unittest_table存在的話
        self.mysql_util.execute_with_commit(
            'drop table if exists unittest_table ;'
        )
        # 創建表格
        if not self.mysql_util.check_table_exists('test', 'unittest_table'):
            self.mysql_util.create_table('test', 'unittest_table', 'id int primary key, name varchar(255)')
        else:
            logger.debug('表已經存在')

        # 插入數據
        # 這邊使用的函數是execute_without_commit()原則是是沒有提交功能，但是上面已經設置了自動提交
        # self.mysql_util.conn.autocommit(True)所以他還是會提交數據 (1,"danny")
        self.mysql_util.execute_without_commit(
            'insert into unittest_table values (1,"danny")'
        )
        # 查詢數據
        result = self.mysql_util.query('select * from unittest_table')
        print(result)
        expect = ((1, 'danny'),)
        # 斷言
        self.assertEqual(result, expect)  # 查詢的結果是元組
        self.mysql_util.close()
        # 後半部分
        # 接著我們在這邊把自動提交在關閉new_util.conn.autocommit(False)，然後使用execute_without_commit()
        # 因為execute_without_commit()是沒有提交功能，且自動提交又被關閉，所以(2,"mark")應該是要插不進去
        new_util = MysqlUtil()
        new_util.select_db('test')
        new_util.conn.autocommit(False)
        new_util.execute_without_commit(
            'insert into unittest_table values (2,"mark")'
        )
        new_util.close()
        # 正常來說上面的(2,"mark")應該是沒有insert進去因為沒有提交，而是待在緩存中
        # 所以這邊用new_util2去query的話如果沒有(2,"mark")的數據代表函數是沒有什麼問題
        # 這邊在建一個實例，目的是因為mysql有緩存
        new_util2 = MysqlUtil()
        new_util2.select_db('test')
        result = new_util2.query('select * from unittest_table')
        # 斷言
        expect = ((1, 'danny'),)
        self.assertEqual(result, expect)
        # 刪除 unittest_table
        new_util2.execute_without_commit(
            'drop tables unittest_table'
        )
        # 關閉數據庫
        new_util2.close()

    def test_get_processed_files(self):
        """
        測試獲取已經被處理過的文件的和樹的單元測試
        測試需保證獨立性，自備表及數據
        :return:
        """
        # 在測試之前先把表清掉
        self.mysql_util.select_db('test')
        self.mysql_util.execute_with_commit(
            "drop table if exists test_file_monitor "
        )
        # 第一個測試用例
        result = get_processed_file(self.mysql_util, 'test', 'test_file_monitor')
        expect = []
        self.assertEqual(result, expect)
        # 準備數據
        if not self.mysql_util.check_table_exists('test', 'test_file_monitor'):
            self.mysql_util.create_table('test', 'test_file_monitor',
                                         create_cols=config.metadata_file_monitor_create_cols)
        self.mysql_util.execute_with_commit(
            'truncate table test_file_monitor'
        )
        # 第二個測試用莉
        self.mysql_util.execute_with_commit(
            'insert into test_file_monitor values (1,"e:/data.log",1024,"2000-01-01 10:00:00")'
        )
        result1 = get_processed_file(self.mysql_util, 'test', 'test_file_monitor',
                                     create_cols=config.metadata_file_monitor_create_cols)
        expect1 = ['e:/data.log']
        self.assertEqual(result1, expect1)

        # 第三個測試用例
        self.mysql_util.execute_with_commit(
            'insert into test_file_monitor values (2,"e:/data1.log",1024,"2000-01-01 10:00:00")'
        )
        result2 = get_processed_file(self.mysql_util, 'test', 'test_file_monitor',
                                     create_cols=config.metadata_file_monitor_create_cols)
        result2 = result1.sort()
        expect2 = ['e:/data.log', 'e:/data1.log'].sort()
        self.assertEqual(result2, expect2)
        # 把表清掉
        self.mysql_util.execute_with_commit(
            "drop table if exists test_file_monitor "
        )
        pass

    def tearDown(self):
        pass
