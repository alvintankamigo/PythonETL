"""
json 文件處理的主要邏輯
# 第一步：讀取指定路徑下的json文件名稱
# 第二步：讀取元數據中已經被處理過的json文件
# 第三部：比較兩串列的差異。找出還未被處理過的文件名
"""
from util.logger_util import init_logger
from util.file_util import get_dir_files_list, get_new_by_compare_list
import config.project_config as config
from models.orders_model import OrdersModel, OrderDetailModel
from util.mysql_util import MysqlUtil, get_processed_file


def build_db_util():
    db_util = MysqlUtil()
    # 建立mysql對象，連接到retail資料庫中
    target_util = MysqlUtil(
        host=config.target_host,
        port=config.target_port,
        user=config.target_user,
        password=config.target_password,
        database=config.target_database
    )
    return db_util, target_util


def get_processed_files(db_util):
    # 第一步：讀取指定路徑下的json文件名稱
    files = get_dir_files_list(path=config.json_data_root_path, recursive=False)
    logger.info(f"判斷json文件夾：有如下文件：{files}")
    # 第二步：讀取元數據中已經被處理過的json文件
    # 2-2
    processed_file = get_processed_file(db_util)
    logger.info(f"查詢mysql找到有以下文件已被處理過{processed_file}")
    # 第三步：比較兩串列的差異。找出還未被處理過的文件名
    need_to_process_files = get_new_by_compare_list(files, processed_file)
    logger.info(f"經過對比元數據庫，以下文件供我們處理：{need_to_process_files}")
    return need_to_process_files


def build_model(filename):
    # 記錄此文件有多少條數據被處理的計數器
    file_processed_line_count = 0
    # 用來儲存訂單對象的列表
    order_model_list = []
    # 用來儲存訂單詳情對象的列表
    order_detail_model_list = []
    ## 4-2 將文件字串利用OrderModel,OrderDetailModel 將內容提取出來
    for line in open(filename, "r", encoding="utf-8"):  # line就是每一個文件裡面的每一條訂單的json格式字串
        # 每循環一行就加一次
        file_processed_line_count += 1
        order_model = OrdersModel(data=line)  # 一筆訂單數據
        order_detail_model = OrderDetailModel(data=line)  # 一筆訂單產品詳情數據
        # 分別把order,order_detail對象加進去
        order_model_list.append(order_model)
        order_detail_model_list.append(order_detail_model)
        # 當這個循環結束，一個json文件已經處理完
    return file_processed_line_count, order_model_list, order_detail_model_list


def filter_except_data(order_model_list):
    ## 4-3 對數據進行過濾
    reserved_models = []
    # 當金額超過10000元的刪掉，因為幾乎不可能，一個小店面會有超過人民幣10000的商品
    for model in order_model_list:
        if model.receivable < 10000:
            reserved_models.append(model)
    return reserved_models


def get_order_csv_file():
    # 用來寫出訂單模型的文件對象
    order_csv_write_f = open(
        file=config.retail_output_csv_root_path + config.retail_orders_output_csv_file_name,
        mode='a',  # 用w，當在執行到第二個json文件時，會覆蓋第一個json文件的數據、
        encoding="utf-8"
    )
    # 把訂單產品詳情寫入到csv
    # 用來寫出訂單產品詳情模型的文件對象
    order_detail_csv_write_f = open(
        file=config.retail_output_csv_root_path + config.retail_orders_detail_output_csv_file_name,
        mode='a',
        encoding="utf-8"
    )
    return order_csv_write_f, order_detail_csv_write_f


def write_model_to_csv(reserved_models, order_detail_model_list, order_csv_write_f, order_detail_csv_write_f):
    for model in reserved_models:
        csv_line = model.to_csv()
        order_csv_write_f.write(csv_line)

    for model in order_detail_model_list:
        for single_product in model.products_detail:  # 每一筆訂單的所有產品對象都在這個產品詳情列表裡
            csv_line = single_product.to_csv()
            order_detail_csv_write_f.write(csv_line)
            order_detail_csv_write_f.write('\n')


def close_order_csv_file(order_csv_write_f, order_detail_csv_write_f):
    order_csv_write_f.close()
    order_detail_csv_write_f.close()


def create_order_tables(target_util):
    if not target_util.check_table_exists(config.target_database, config.target_orders_table_name):
        target_util.create_table(config.target_database,
                                 config.target_orders_table_name,
                                 config.target_orders_table_create_cols)

    if not target_util.check_table_exists(config.target_database,
                                          config.target_orders_detail_table_name):
        target_util.create_table(config.target_database,
                                 config.target_orders_detail_table_name,
                                 config.target_orders_detail_table_create_cols)


def write_model_data_to_mysql(models):
    for i, model in enumerate(models):
        sql = model.generate_insert_sql()
        target_util.select_db(config.target_database)
        target_util.execute_without_commit(sql)
        # 每1000次提交一次
        if i % 1000 == 0:
            target_util.conn.commit()
    # 提交零頭
    target_util.conn.commit()


def write_to_csv(reserved_models, order_detail_model_list):
    # 打開csv文件：創建csv對象
    order_csv_write_f, order_detail_csv_write_f = get_order_csv_file()
    # 將order,order_detail 裡的資料寫入csv檔案
    write_model_to_csv(reserved_models, order_detail_model_list, order_csv_write_f, order_detail_csv_write_f)
    # 關閉csv_file
    close_order_csv_file(order_csv_write_f, order_detail_csv_write_f)
    # logger.info(f"完成了csv備份文件的輸出，寫到了：{config.retail_output_csv_root_path}")


def write_to_sql(target_util,reserved_models,order_detail_model_list):
    create_order_tables(target_util)
    # 將order表寫入retail
    write_model_data_to_mysql(reserved_models)
    # 將order_detail表寫入retail
    write_model_data_to_mysql(order_detail_model_list)


def write_matadata_to_metadatabase(db_util, processed_file_record_dict):
    for filename, processed_line in processed_file_record_dict.items():
        insert_sql = f"INSERT INTO {config.metadata_file_monitor_table_name}(file_name,process_line) VALUES ('{filename}',{processed_line})"
        db_util.execute_with_commit(insert_sql)


def close_mysql(db_util,target_util):
    db_util.close()
    target_util.close()


if __name__ == '__main__':
    logger = init_logger()
    logger.info(f"讀取json文件數據處理，程式開始進行")
    # 創建mysql連接對象
    db_util, target_util = build_db_util()
    # 獲取需要處理的文件名稱
    need_to_process_files = get_processed_files(db_util)
    # 被處理的文件信息紀錄
    processed_file_record_dict = {}
    # 第四步： 開始處理json文件
    ## 4-1 讀取json文件
    for filename in need_to_process_files:
        # 建立order,order_detail 模型，得到訂單列表、訂單詳情列表
        file_processed_line_count, order_model_list, order_detail_model_list = build_model(filename=filename)
        # print(file_processed_line_count, order_model_list)
        ## 4-3 對數據進行過濾
        reserved_models = filter_except_data(order_model_list)
        # print(reserved_models)
        ## 4-4 把得到的模型中的數據寫入csv
        write_to_csv(reserved_models, order_detail_model_list)

        # 記錄有多少條數據在這次循環的filename裏面，以這邊來說會有三個文件，每個文件都有一個數
        processed_file_record_dict[filename] = file_processed_line_count

        ## 4-5 把得到的模型中的數據寫入sql(retail)
        # write_to_sql(target_util)

        if not target_util.check_table_exists(config.target_database, config.target_orders_table_name):
            target_util.create_table(config.target_database,
                                     config.target_orders_table_name,
                                     config.target_orders_table_create_cols)

        if not target_util.check_table_exists(config.target_database,
                                              config.target_orders_detail_table_name):
            target_util.create_table(config.target_database,
                                     config.target_orders_detail_table_name,
                                     config.target_orders_detail_table_create_cols)

            write_model_data_to_mysql(reserved_models)
            write_model_data_to_mysql(order_detail_model_list)

    target_util.close()
    global_count = sum(processed_file_record_dict.values())
    logger.info(f"完成了csv備份文件的輸出，寫到了：{config.retail_output_csv_root_path}")
    logger.info(f"完成了向mysql資料庫中插入數據，總共插入了{global_count}條的數據")

    # 把已經被處理過的文件，寫進去元數據庫裡面（區分處理過和未處理過）
    write_matadata_to_metadatabase(db_util, processed_file_record_dict)
    db_util.close()
    logger.info(f"讀取json數據以及向mysql插入數據，並寫入csv，程式已執行完成")
