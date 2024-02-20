import time

log_root_path = '/Users/tandunqian/PythonEtl/logging/'
log_dir = f"pyetl-{time.strftime('%Y%m%d-%H', time.localtime(time.time()))}.log"
level = 20
# 這裡指的是一班放log日誌的地方，我用database來舉例
database_log_root_path = '/Users/tandunqian/PythonEtl/source_database_logging'

# Mysql 配置 (所有的sql)
mysql_charset = 'utf8'
# 元數據庫 配置begin 
meta_host = 'localhost'
meta_port = 3306
meta_user = 'root'
meta_password = 'A870206a'
meta_database = 'metadata'  #

metadata_file_monitor_table_name = 'file_monitor'
metadata_file_monitor_create_cols = """
    id int primary key auto_increment,
    file_name varchar(255) unique not null comment '被處理的文件名稱',
    process_line int comment '本文件中有多少條數據被處理',
    process_time timestamp default current_timestamp comment '處理時間'
"""

metadata_logfile_monitor_table_name = 'logfile_monitor'
metadata_logfile_monitor_create_cols = """
    id int primary key auto_increment,
    file_name varchar(255) unique not null comment '被處理的文件名稱',
    process_line int comment '本文件中有多少條數據被處理',
    process_time timestamp default current_timestamp comment '處理時間'
"""
# 元數據庫 配置end 

# 目標數據庫 配置begin
target_host = 'localhost'
target_port = 3306
target_user = 'root'
target_password = 'A870206a'
target_database = 'retail'  #
# 目標數據庫 配置end

# json 相關配置start 
json_data_root_path = '/Users/tandunqian/PythonEtl/data/json'

# 訂單數據輸出的csv根路徑
retail_output_csv_root_path = "/Users/tandunqian/PythonEtl/retail_csv_output/"
# 每次運行，訂單文件寫出的檔名
retail_orders_output_csv_file_name = f"order-{time.strftime('%Y-%m-%d-%H_%M', time.localtime())}.csv"
# 每次運行，訂單詳情文件檔名
retail_orders_detail_output_csv_file_name = f"orders-detail-{time.strftime('%Y-%m-%d-%H_%M', time.localtime())}.csv"

# 訂單表名稱
target_orders_table_name = "orders"
# 訂單表mysql資料庫建表語句訊息
target_orders_table_create_cols = \
    f"order_id VARCHAR(255) PRIMARY KEY, " \
    f"store_id INT COMMENT '店鋪ID', " \
    f"store_name VARCHAR(30) COMMENT '店鋪名稱', " \
    f"store_status VARCHAR(10) COMMENT '店鋪狀態(open,close)', " \
    f"store_own_user_id INT COMMENT '店主id', " \
    f"store_own_user_name VARCHAR(50) COMMENT '店主名稱', " \
    f"store_own_user_tel VARCHAR(15) COMMENT '店主手機號', " \
    f"store_category VARCHAR(10) COMMENT '店鋪類型(normal,test)', " \
    f"store_address VARCHAR(255) COMMENT '店鋪地址', " \
    f"store_shop_no VARCHAR(255) COMMENT '店鋪第三方支付id號', " \
    f"store_province VARCHAR(10) COMMENT '店鋪所在省', " \
    f"store_city VARCHAR(10) COMMENT '店鋪所在市', " \
    f"store_district VARCHAR(10) COMMENT '店鋪所在行政區', " \
    f"store_gps_name VARCHAR(255) COMMENT '店鋪gps名稱', " \
    f"store_gps_address VARCHAR(255) COMMENT '店鋪gps地址', " \
    f"store_gps_longitude VARCHAR(255) COMMENT '店鋪gps經度', " \
    f"store_gps_latitude VARCHAR(255) COMMENT '店鋪gps緯度', " \
    f"is_signed TINYINT COMMENT '是否第三方支付簽约(0,1)', " \
    f"operator VARCHAR(10) COMMENT '操作員', " \
    f"operator_name VARCHAR(50) COMMENT '操作員名稱', " \
    f"face_id VARCHAR(255) COMMENT '顧客面部識别ID', " \
    f"member_id VARCHAR(255) COMMENT '顧客會員ID', " \
    f"store_create_date_ts TIMESTAMP COMMENT '店鋪創建時間', " \
    f"origin VARCHAR(255) COMMENT '原始信息(無用)', " \
    f"day_order_seq INT COMMENT '本訂單是當日第幾單', " \
    f"discount_rate DECIMAL(10, 5) COMMENT '折扣率', " \
    f"discount_type TINYINT COMMENT '折扣類型', " \
    f"discount DECIMAL(10, 5) COMMENT '折扣金額', " \
    f"money_before_whole_discount DECIMAL(10, 5) COMMENT '折扣前總金額', " \
    f"receivable DECIMAL(10, 5) COMMENT '應收金額', " \
    f"erase DECIMAL(10, 5) COMMENT '抹零金額', " \
    f"small_change DECIMAL(10, 5) COMMENT '找零金額', " \
    f"total_no_discount DECIMAL(10, 5) COMMENT '總價格(無折扣)', " \
    f"pay_total DECIMAL(10, 5) COMMENT '付款金額', " \
    f"pay_type VARCHAR(10) COMMENT '付款類型', " \
    f"payment_channel TINYINT COMMENT '付款通道', " \
    f"payment_scenarios VARCHAR(15) COMMENT '付款描述(無用)', " \
    f"product_count INT COMMENT '本單賣出多少商品', " \
    f"date_ts TIMESTAMP COMMENT '訂單時間', " \
    f"INDEX (receivable), INDEX (date_ts)"

# 訂單詳情表名稱
target_orders_detail_table_name = "orders_detail"
# 訂單詳情表建表訊息
target_orders_detail_table_create_cols = \
    f"order_id VARCHAR(255) COMMENT '訂單ID', " \
    f"barcode VARCHAR(255) COMMENT '商品條碼', " \
    f"name VARCHAR(255) COMMENT '商品名稱', " \
    f"count INT COMMENT '本單此商品賣出數量', " \
    f"price_per DECIMAL(10, 5) COMMENT '實際售賣單價', " \
    f"retail_price DECIMAL(10, 5) COMMENT '零售建議價', " \
    f"trade_price DECIMAL(10, 5) COMMENT '貿易價格(進貨價)', " \
    f"category_id INT COMMENT '商品類别ID', " \
    f"unit_id INT COMMENT '商品單位ID(包、袋、箱、等)', " \
    f"PRIMARY KEY (order_id, barcode)"

# 目標數據表以及數據表結構
target_barcode_table_name = 'barcode'
target_barcode_table_create_cols = """
    `code` varchar(50) PRIMARY KEY COMMENT '商品條碼',
    `name` varchar(200) DEFAULT '' COMMENT '商品名稱',
    `spec` varchar(200) DEFAULT '' COMMENT '商品規格',
    `trademark` varchar(100) DEFAULT '' COMMENT '商品商標',
    `addr` varchar(200) DEFAULT '' COMMENT '商品產地',
    `units` varchar(50) DEFAULT '' COMMENT '商品單位(個、杯、箱、等)',
    `factory_name` varchar(200) DEFAULT '' COMMENT '生產廠家',
    `trade_price` DECIMAL(50, 5) DEFAULT 0.0 COMMENT '貿易價格(指導進價)',
    `retail_price` DECIMAL(50, 5) DEFAULT 0.0 COMMENT '零售價格(建議賣價)',
    `updateAt` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新時間',
    `wholeunit` varchar(50) DEFAULT NULL COMMENT '大包装單位',
    `wholenum` int(11) DEFAULT NULL COMMENT '大包装内装數量',
    `img` varchar(500) DEFAULT NULL COMMENT '商品圖片',
    `src` varchar(20) DEFAULT NULL COMMENT '源信息', 
    INDEX (updateAt)
"""

target_backend_table_name = 'backend_log'
target_backend_table_create_cols = \
    f"id int PRIMARY KEY AUTO_INCREMENT COMMENT '自增ID', " \
    f"log_time TIMESTAMP(6) COMMENT '日誌时间,精確到6位毫秒值', " \
    f"log_level VARCHAR(10) COMMENT '日誌级别', " \
    f"log_module VARCHAR(50) COMMENT '輸出日誌的功能模塊名', " \
    f"response_time INT COMMENT '接口響應時間毫秒', " \
    f"province VARCHAR(30) COMMENT '訪問者省份', " \
    f"city VARCHAR(30) COMMENT '訪問者城市', " \
    f"log_text VARCHAR(255) COMMENT '日誌正文', " \
    f"INDEX(log_time)"
# 數據庫配置
source_host = 'localhost'
source_user = 'root'
source_password = 'A870206a'
source_port = 3306
source_db = 'source'
# 數據庫名稱
source_barcode_table_name = 'sys_barcode'

# barcode業務：update_at欄位監控表的名稱
metadata_barcode_table_name = 'barcode_monitor'
metadata_barcode_table_create_cols = "id INT PRIMARY KEY AUTO_INCREMENT COMMENT '自增ID', " \
                                     "time_record TIMESTAMP NOT NULL COMMENT '本次採集紀錄的最大時間', " \
                                     "gather_line_count INT NULL COMMENT '本次採集條數'"
# 數據csv導入目標資料夾路徑
barcode_output_csv_root_path = '/Users/tandunqian/PythonEtl/barcode_csv_output/'
barcode_orders_output_csv_file_name = f"barcode-{time.strftime('%Y-%m-%d-%H_%M', time.localtime())}.csv"
# 後台日誌資料寫入的目標csv路徑
backend_log_csv_output = '/Users/tandunqian/PythonEtl/backend_log_csv_output/'
backend_log_csv_output_csv_file_name = f"backend_log-{time.strftime('%Y-%m-%d-%H_%M', time.localtime())}.csv"
