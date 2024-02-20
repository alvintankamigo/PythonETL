"""讀取source 裡的sys_barcode裡的data"""
import sys

from util.logger_util import init_logger
from util.mysql_util import MysqlUtil
import config.project_config as config
from models.barcode_model import BarcodeModel


def get_db_util():
    # 1.創建mysql對象 (source,retail,metadata)
    metadata_util = MysqlUtil()
    target_util = MysqlUtil(
        host=config.target_host,
        port=config.target_port,
        user=config.target_user,
        password=config.target_password,
        database=config.target_database
    )
    source_util = MysqlUtil(
        host=config.source_host,
        port=config.source_port,
        user=config.source_user,
        password=config.source_password,
        database=config.source_db
    )
    return metadata_util, target_util, source_util


def chek_table_exist(source_util, target_util):
    # 2.1 判斷數據源存不存在
    if not source_util.check_table_exists(config.source_db, config.source_barcode_table_name):
        logger.error(f"資料庫{config.source_db}不存在{config.source_barcode_table_name}這張表，無法採集，請退出")
        sys.exit(1)  # 傳入0代表python程序正常停止
    # 3 檢查retail裡面有沒有存在barcode表，沒有就創建
    if not target_util.check_table_exists(config.target_database, config.target_barcode_table_name):
        target_util.create_table(config.target_database,
                                 config.target_barcode_table_name,
                                 config.target_barcode_table_create_cols)


def get_last_update_time(metadata_util):
    metadata_util.select_db(config.meta_database)
    last_update_time = None
    # 讀取元數據庫中的barcode_monitor表中的上次更新批次的時間戳的最大時間
    # 如果不存在就創建barcode_monitor表
    if not metadata_util.check_table_exists(config.meta_database, config.metadata_barcode_table_name):
        metadata_util.create_table(config.meta_database, config.metadata_barcode_table_name,
                                   config.metadata_barcode_table_create_cols)
    else:  # 進入else表示表存在，需要從mysql中查出上次查詢的時間
        query_sql = f"select time_record from {config.metadata_barcode_table_name} order by time_record desc limit 1"
        result = metadata_util.query(query_sql)  # 在mysql中是利用tuple在傳送數據
        # ((,))
        if len(result) > 0:
            last_update_time = str(result[0][0])  # 找出上次查詢的時間
    return last_update_time


def get_new_increment(last_update_time, source_util):
    if last_update_time is not None:
        # 就只拿比上次更新時間還大的資料
        sql = (f"select * from {config.source_barcode_table_name} where updateAt >= '{last_update_time}'"
               f" order by updateAt")
    else:
        # 就把source資料庫中 sys_barcode表裡面的資料全部撈出來
        sql = f"select * from {config.source_barcode_table_name} order by updateAt"
    source_util.select_db(config.source_db)
    results = source_util.query(sql)
    return results


def build_barcode_model(results):
    barcode_list = []
    for single_result in results:
        code = single_result[0]
        name = single_result[1]
        spec = single_result[2]
        trademark = single_result[3]
        addr = single_result[4]
        units = single_result[5]
        factory_name = single_result[6]
        trade_price = single_result[7]
        retail_price = single_result[8]
        updateAt = str(single_result[9])
        wholeunit = single_result[10]
        wholenum = single_result[11]
        img = single_result[12]
        src = single_result[13]

        model = BarcodeModel(
            code=code, name=name, spec=spec, trademark=trademark,
            addr=addr, units=units, factory_name=factory_name,
            trade_price=trade_price, retail_price=retail_price,
            updateAt=updateAt, wholeunit=wholeunit,
            wholenum=wholenum, img=img, src=src
        )
        barcode_list.append(model)
    return barcode_list


def write_csv(barcode_list):
    # 構建一個open實例
    barcode_csv_write_f = open(
        file=config.barcode_output_csv_root_path + config.barcode_orders_output_csv_file_name,
        mode='a',
        encoding='utf-8'
    )
    csv_count = 0
    for barcode in barcode_list:
        csv_line = barcode.to_csv()
        barcode_csv_write_f.write(csv_line)
        barcode_csv_write_f.write('\n')
        csv_count += 1
        if csv_count % 1000 == 0:
            barcode_csv_write_f.flush()
            logger.info(f"將{config.source_db}中的{config.source_barcode_table_name}數據，寫入csv中，總共{csv_count}")
    barcode_csv_write_f.close()
    return csv_count


def write_to_sql(target_util,barcode_list):
    target_util.select_db(config.target_database)
    count = 0
    max_last_update_time = "2000-01-01 00:00:00"
    for i, barcode in enumerate(barcode_list):
        # 紀錄當前時間
        current_time = barcode.updateAt
        if current_time > max_last_update_time:
            max_last_update_time = current_time
        sql = barcode.generate_insert_sql()
        target_util.execute_without_commit(sql)
        count += 1
        if count % 1000 == 0:
            target_util.conn.commit()
            logger.info(f"從數據源{config.source_db}，讀取表{config.source_barcode_table_name}"
                        f"導入並寫入目標表{config.target_barcode_table_name}數據有：{i}行")
    target_util.conn.commit()
    return count, max_last_update_time


def write_to_metadata(metadata_util):
    metadata_util.select_db(config.meta_database)
    meta_sql = (f"INSERT INTO {config.metadata_barcode_table_name}(time_record,gather_line_count) "
                f"values('{max_last_update_time}',{count})")
    metadata_util.execute_with_commit(meta_sql)


def close_db(metadata_util,target_util,source_util):
    metadata_util.close()
    target_util.close()
    source_util.close()


if __name__ == '__main__':

    logger = init_logger()
    metadata_util, target_util, source_util = get_db_util()
    # 2 從source 裡讀取barcode的數據
    chek_table_exist(source_util, target_util)

    # 4 寫入csv,及retail資料庫裡
    last_update_time = get_last_update_time(metadata_util)

    results = get_new_increment(last_update_time, source_util)
    # print(results[:1])

    # 到這邊以上已經做到把資料從source database 拿出來
    # 建構數據的model來乘載數據
    barcode_list = build_barcode_model(results)
    # print(barcode_list[:3])
    # 寫入到指定路徑下的csv
    csv_count = write_csv(barcode_list)

    logger.info(f"將{config.source_db}中的{config.source_barcode_table_name}數據，寫入csv中，總共{csv_count}")

    # 插入目旳地資料庫
    count, max_last_update_time = write_to_sql(target_util, barcode_list)
    logger.info(f"從數據源{config.source_db}，讀取表{config.source_barcode_table_name}"
                f"導入並寫入目標表{config.target_barcode_table_name}數據有：{count}行")
    # 紀錄到metadata database
    write_to_metadata(metadata_util)

    close_db(metadata_util,target_util,source_util)
    logger.info(f"讀取mysql數據，寫入目標數據庫及csv完成")
