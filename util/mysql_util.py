import pymysql
from util.logger_util import init_logger
import config.project_config as config

# coding: utf-8
"""
這是一個mysql的工具類
提供mysql的一些功能
1.創建連接
2.關閉連接
3.執行sql語句，並返回查詢結果
4.執行一條單獨無返回直的sql語句
5.創建表
6.查詢表是否存在
"""
logger = init_logger()


class MysqlUtil:
    def __init__(self,
                 host=config.meta_host,
                 port=config.meta_port,
                 user=config.meta_user,
                 password=config.meta_password,
                 charset=config.mysql_charset,
                 database=config.meta_database,
                 ):
        # 創建連接
        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset=charset,
            database=database,  #
            autocommit=False  # 不自動提交
        )
        if self.conn:
            logger.info(f"構建完成到{host}:{port}的{database}數據庫連接...")
        pass

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
        pass

    def query(self, sql):
        """

        :param sql: 需要執行的查詢語句
        :return: 查詢的結果
        """
        # 獲取游標
        cursor = self.conn.cursor()
        # 執行查詢語句
        cursor.execute(sql)
        # 獲得查詢結果
        result = cursor.fetchall()
        # 關閉游標
        cursor.close()
        logger.info(f"執行的sql語句完成，查詢的結果有{len(result)}條數據，執行的sql語句是{sql}")
        return result

    def select_db(self, db):
        """
        切換資料庫
        :param db: 資料庫名稱
        :return: None
        """
        self.conn.select_db(db)
        logger.info(f"切換到{db}數據庫")
        pass

    def execute_with_commit(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        logger.debug(f"執行了一條：{sql}")
        # logger.info(results)
        if not self.conn.get_autocommit():
            self.conn.commit()
        cursor.close()
        pass

    def execute_without_commit(self, sql):
        """
        直接執行一條sql語句，不處理返回值，不會判斷自動提交，只執行步commit
        :param sql:
        :return:
        """
        cursor = self.conn.cursor()
        cursor.execute(sql)
        logger.debug(f"執行了一條：{sql}")
        cursor.close()
        pass

    def check_table_exists(self, db_name, table_name):
        """
        檢查數據庫中的特定的表是否存在
        :param db_name: 資料庫
        :param self:
        :param table_name: 要確認的表
        :return: true,false
        """
        self.conn.select_db(db_name)
        # 查詢
        # 查詢出來的結果資料型態是元組，
        # 假設該數據庫裡有兩張表，table1,table2, result的結果就是((table1,),(table2))
        result = self.query('show tables;')

        return (table_name,) in result

    def create_table(self, db_name, table_name, create_cols):
        """
        檢查表是否存在，如果不存在就創建
        :param db_name: 數據庫
        :param table_name:
        :param create_cols:
        :return:
        """

        sql = f'create table {table_name}({create_cols});'
        self.select_db(db_name)
        self.execute_with_commit(sql)
        logger.info(f"在{db_name}:中創建好了{table_name}，建表語句是：{sql}")


def get_processed_file(db_util, db_name=config.meta_database, table_name=config.metadata_file_monitor_table_name,
                       create_cols=config.metadata_file_monitor_create_cols):
    """
    獲取被處理過的文件名稱
    :param db_util:mysql實例
    :param db_name:數據庫名稱，metadata
    :param table_name:元數據表名，file_monitor
    :param create_cols:間表語句中的蘭桂名稱和類型
    :return:被處理過的文件名稱列表
    """
    # 切換數據庫
    db_util.select_db(db_name)

    # 判斷是否表格存在，如果不存在就要建立表格
    if not db_util.check_table_exists(db_name, table_name):
        db_util.create_table(db_name, table_name, create_cols)
        logger.info(f"建立:{table_name}")
    else:
        logger.info(f"{table_name}已經存在")
    # 查詢被處理過的文件名稱
    results = db_util.query(f"select file_name from {table_name}")
    # result是一個元組((file1,),(file2,))
    file_names = []
    for result in results:
        file_names.append(result[0])

    return file_names


if __name__ == '__main__':
    mysql_util = MysqlUtil()
    mysql_util.query('select * from test;')
    mysql_util.select_db('retail')
    mysql_util.query('select database();')
    if not mysql_util.check_table_exists('metadata', 'test2'):
        mysql_util.create_table('metadata', 'test2', 'name varchar(255), age int')

    mysql_util.close()
    # target_mysql_util = MysqlUtil(
    #     host=config.target_host,
    #     port=config.target_port,
    #     user=config.target_user,
    #     password=config.target_password,
    #     database=config.target_database
    # )
    # target_mysql_util.close()
