"""將log裡的資料寫進去retail(目的地資料庫裡)以及csv"""
from util.logger_util import init_logger
from util.file_util import get_dir_files_list, get_new_by_compare_list
from util.mysql_util import MysqlUtil, get_processed_file
from models.log_model import BackendLogModel
import config.project_config as config
from util.logger_util import init_logger

logger = init_logger()
# 1. 創建數據庫對象
# 寫入的資料庫
target_util = MysqlUtil(
    host=config.target_host,
    port=config.target_port,
    user=config.target_user,
    password=config.target_password,
    database=config.target_database
)
# 元資料庫
metadata_util = MysqlUtil()
# 1.讀取日誌資料（在目的地資料夾下面）: 要找的是沒有被處理過的資料
logger_file = get_dir_files_list(path=config.database_log_root_path)
# 1.1 第一次一定是什麼都沒除理過
# 如果元資料庫中沒有logfile_monitor表就創建
if not metadata_util.check_table_exists(config.meta_database, config.metadata_logfile_monitor_table_name):
    metadata_util.create_table(config.meta_database,
                               config.metadata_logfile_monitor_table_name,
                               config.metadata_logfile_monitor_create_cols)
if not target_util.check_table_exists(config.target_database,
                                      config.target_backend_table_name):
    target_util.create_table(config.target_database,
                             config.target_backend_table_name,
                             config.target_backend_table_create_cols)
# 讀取以處理過的資料
processed_files = get_processed_file(metadata_util,
                                     config.meta_database,
                                     config.metadata_logfile_monitor_table_name,
                                     config.metadata_logfile_monitor_create_cols)
# 需要被處理的資料
need_to_processed_files = get_new_by_compare_list(logger_file, processed_files)
# print(need_to_processed_files)


processed_file_dict = {}
for file_name in need_to_processed_files:
    processed_file_count = 0
    backend_log_list = []
    count = 0
    for line in open(file_name, mode='r', encoding='utf-8'):  # 每一個log檔
        processed_file_count += 1
        backend_log_model = BackendLogModel(line)
        backend_log_list.append(backend_log_model)

    backend_log_csv_f = open(
        file=config.backend_log_csv_output + config.backend_log_csv_output_csv_file_name,
        mode='a',
        encoding='utf-8'
    )
    for backend_log in backend_log_list:
        csv_line = backend_log.to_csv()
        backend_log_csv_f.write(csv_line)
    backend_log_csv_f.close()

    # 寫入目的地數據庫
    for i, backend_log in enumerate(backend_log_list):
        sql = backend_log.generate_insert_to_sql()
        target_util.execute_without_commit(sql)
        if i % 1000 == 0:
            target_util.conn.commit()
            logger.info(f"完成了向{config.target_database}資料庫中的{config.target_backend_table_name}表中，"
                        f"插入數據，總共插入了{i}條的數據")
    target_util.conn.commit()
    logger.info(f"插入資料庫程序已完成")
    processed_file_dict[file_name] = processed_file_count
# 3 在元數據庫裡面做紀錄
for file_name, processed_file_count in processed_file_dict.items():
    sql = f"INSERT INTO {config.metadata_logfile_monitor_table_name}(file_name,process_line) VALUES ('{file_name}','{processed_file_count}')"
    metadata_util.execute_with_commit(sql)
logger.info(f"以向{config.metadata_logfile_monitor_table_name}，寫入數據")
# print(len(logger_file))
# 2.將資料寫入csv文件夾，寫成csv檔
