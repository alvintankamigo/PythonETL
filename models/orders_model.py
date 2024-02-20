import json
from util import time_util, str_util
import config.project_config as config

"""
定義訂單模型
"""


class OrdersModel:
    # 定義相關屬性，目標表中有多少欄位，類中就應該有多少個屬性，數據來源json字串
    # 純訂單，不包含訂單詳情
    def __init__(self, data):
        # 將json數據的字符串轉換成dict結構
        data = json.loads(data)
        self.discount_rate = data['discountRate']  # 折扣率
        self.store_shop_no = data['storeShopNo']  # 店鋪店號（無用列）
        self.day_order_seq = data['dayOrderSeq']  # 本單為當日第几單
        self.store_district = data['storeDistrict']  # 店鋪所在行政區
        self.is_signed = data['isSigned']  # 是否簽约店鋪（簽约第三方支付體系）
        self.store_province = data['storeProvince']  # 店鋪所在省份
        self.origin = data['origin']  # 原始信息（無用）
        self.store_gps_longitude = data['storeGPSLongitude']  # 店鋪GPS經度
        self.discount = data['discount']  # 折扣金額
        self.store_id = data['storeID']  # 店鋪ID
        self.product_count = data['productCount']  # 本單售賣商品數量
        self.operator_name = data['operatorName']  # 操作員姓名
        self.operator = data['operator']  # 操作員ID
        self.store_status = data['storeStatus']  # 店鋪狀態
        self.store_own_user_tel = data['storeOwnUserTel']  # 店鋪店主电话
        self.pay_total = data['payedTotal']  # 支付總金額
        self.pay_type = data['payType']  # 支付類型
        self.discount_type = data['discountType']  # 折扣類型
        self.store_name = data['storeName']  # 店鋪名稱
        self.store_own_user_name = data['storeOwnUserName']  # 店鋪店主名稱
        self.date_ts = data['dateTS']  # 訂單时间
        self.small_change = data['smallChange']  # 找零金額
        self.store_gps_name = data['storeGPSName']  # 店鋪GPS名稱
        self.erase = data['erase']  # 是否抹零
        self.store_gps_address = data['storeGPSAddress']  # 店鋪GPS地址
        self.order_id = data['orderID']  # 訂單ID
        self.money_before_whole_discount = data['moneyBeforeWholeDiscount']  # 折扣前金額
        self.store_category = data['storeCategory']  # 店鋪類别
        self.receivable = data['receivable']  # 应收金額
        self.face_id = data['faceID']  # 面部識别ID
        self.store_own_user_id = data['storeOwnUserId']  # 店鋪店主ID
        self.payment_channel = data['paymentChannel']  # 付款通道
        self.payment_scenarios = data['paymentScenarios']  # 付款情况（無用）
        self.store_address = data['storeAddress']  # 店鋪地址
        self.total_no_discount = data['totalNoDiscount']  # 整體價格（無折扣）
        self.payed_total = data['payedTotal']  # 已付款金額
        self.store_gps_latitude = data['storeGPSLatitude']  # 店鋪GPS緯度
        self.store_create_date_ts = data['storeCreateDateTS']  # 店鋪創建時間
        self.store_city = data['storeCity']  # 店鋪所在城市
        self.member_id = data['memberID']  # 會員ID

    # 讓每一筆訂單轉成csv格式，寫入到csv文件中
    def to_csv(self, sep=','):
        # 先確保省份、地區、城市的值有做轉換
        self.check_and_transform_area()
        # 再把有空直的欄位轉換成空字串
        self.check_and_transform_all_column()

        csv_line = \
            f"{self.order_id}{sep}" \
            f"{self.store_id}{sep}" \
            f"{self.store_name}{sep}" \
            f"{self.store_status}{sep}" \
            f"{self.store_own_user_id}{sep}" \
            f"{self.store_own_user_name}{sep}" \
            f"{self.store_own_user_tel}{sep}" \
            f"{self.store_category}{sep}" \
            f"{self.store_address}{sep}" \
            f"{self.store_shop_no}{sep}" \
            f"{self.store_province}{sep}" \
            f"{self.store_city}{sep}" \
            f"{self.store_district}{sep}" \
            f"{self.store_gps_name}{sep}" \
            f"{self.store_gps_address}{sep}" \
            f"{self.store_gps_longitude}{sep}" \
            f"{self.store_gps_latitude}{sep}" \
            f"{self.is_signed}{sep}" \
            f"{self.operator}{sep}" \
            f"{self.operator_name}{sep}" \
            f"{self.face_id}{sep}" \
            f"{self.member_id}{sep}" \
            f"{time_util.ts13_to_date_str(self.store_create_date_ts)}{sep}" \
            f"{self.origin}{sep}" \
            f"{self.day_order_seq}{sep}" \
            f"{self.discount_rate}{sep}" \
            f"{self.discount_type}{sep}" \
            f"{self.discount}{sep}" \
            f"{self.money_before_whole_discount}{sep}" \
            f"{self.receivable}{sep}" \
            f"{self.erase}{sep}" \
            f"{self.small_change}{sep}" \
            f"{self.total_no_discount}{sep}" \
            f"{self.pay_total}{sep}" \
            f"{self.pay_type}{sep}" \
            f"{self.payment_channel}{sep}" \
            f"{self.payment_scenarios}{sep}" \
            f"{self.product_count}{sep}" \
            f"{time_util.ts13_to_date_str(self.date_ts)}\n"

        return csv_line

    def generate_insert_sql(self):
        """生成插入訂單表的sql語句"""
        sql = (
            f"insert ignore into {config.target_orders_table_name} "
            f"(order_id,store_id,store_name,store_status,store_own_user_id,store_own_user_name,store_own_user_tel,store_category,store_address,store_shop_no,store_province,store_city,store_district,store_gps_name,store_gps_address,store_gps_longitude,store_gps_latitude,is_signed,operator,operator_name,face_id,member_id,store_create_date_ts,origin,day_order_seq,discount_rate,discount_type,discount,money_before_whole_discount,receivable,erase,small_change,total_no_discount,pay_total,pay_type,payment_channel,payment_scenarios,product_count,date_ts) "
            f"values ("
            f"'{self.order_id}',"
            f"{self.store_id},"
            f"{str_util.check_str_null_and_transform_to_sql_null(self.store_name)},"
            f"{str_util.check_str_null_and_transform_to_sql_null(self.store_status)},"
            f"{self.store_own_user_id},"
            f"{str_util.check_str_null_and_transform_to_sql_null(self.store_own_user_name)},"
            f"{str_util.check_str_null_and_transform_to_sql_null(self.store_own_user_tel)},"
            f"{str_util.check_str_null_and_transform_to_sql_null(self.store_category)},"
            f"{str_util.check_str_null_and_transform_to_sql_null(self.store_address)},"
            f"{str_util.check_str_null_and_transform_to_sql_null(self.store_shop_no)},"
            f"{str_util.check_str_null_and_transform_to_sql_null(self.store_province)},"
            f"{str_util.check_str_null_and_transform_to_sql_null(self.store_city)},"
            f"{str_util.check_str_null_and_transform_to_sql_null(self.store_district)},"
            f"{str_util.check_str_null_and_transform_to_sql_null(self.store_gps_name)},"
            f"{str_util.check_str_null_and_transform_to_sql_null(self.store_gps_address)},"
            f"{str_util.check_str_null_and_transform_to_sql_null(self.store_gps_longitude)},"
            f"{str_util.check_str_null_and_transform_to_sql_null(self.store_gps_latitude)},"
            f"{self.is_signed},"
            f"{str_util.check_str_null_and_transform_to_sql_null(self.operator)},"
            f"{str_util.check_str_null_and_transform_to_sql_null(self.operator_name)},"
            f"{str_util.check_str_null_and_transform_to_sql_null(self.face_id)},"
            f"{str_util.check_str_null_and_transform_to_sql_null(self.member_id)},"
            f"'{time_util.ts13_to_date_str(self.store_create_date_ts)}',"
            f"{str_util.check_str_null_and_transform_to_sql_null(self.origin)},"
            f"{self.day_order_seq},"
            f"{self.discount_rate},"
            f"{self.discount_type},"
            f"{self.discount},"
            f"{self.money_before_whole_discount},"
            f"{self.receivable},"
            f"{self.erase},"
            f"{self.small_change},"
            f"{self.total_no_discount},"
            f"{self.payed_total},"
            f"{str_util.check_str_null_and_transform_to_sql_null(self.pay_type)},"
            f"{self.payment_channel},"
            f"{str_util.check_str_null_and_transform_to_sql_null(self.payment_scenarios)},"
            f"{self.product_count},"
            f"'{time_util.ts13_to_date_str(self.date_ts)}'"
            f");")
        return sql

    # 如果城市、省份、地區是無意義內容，轉換成謂之地區、未知省份、未知城市
    def check_and_transform_area(self):
        if str_util.check_null(self.store_province):
            self.store_province = '未知省份'
        if str_util.check_null(self.store_district):
            self.store_district = '未知行政區域'
        if str_util.check_null(self.store_city):
            self.store_city = '未知城市'

    # 編寫一個函數，用於將所有的欄位如果有空直就直接轉換成空字串，因為數據寫入到csv文件中，必須是有數據的。否則會導致寫入csv文件失敗
    def check_and_transform_all_column(self):
        pass


class OrderDetailModel:
    def __init__(self, data: str):  # json格式的訂單字串
        data_dict = json.loads(data)
        self.order_id = data_dict['orderID']
        self.products_detail = []
        # 訂單產品清單列表：在這個訂單中有多少個商品
        order_product_list = data_dict['product']
        # print(order_product_list)
        for single_product in order_product_list:
            # print(single_product)
            product = SingleProductSoldModel(self.order_id, single_product)
            # print('這是測試')
            # print(product.generate_value_segment_for_sql_insert())
            # print(type(product.generate_value_segment_for_sql_insert()))
            self.products_detail.append(product)
        # print(self.products_detail)

    def to_csv(self):
        lines = ''
        for product in self.products_detail:
            # product 是對象，而這個對象的類型是什麼類型？ A:SingleProductSoldModel類型（每個對象都是這個對象對應的類，這個類就是可以作為他這個對象的類型）
            lines += product.to_csv()  # to_csv()是SingleProductSoldModel裡面的方法
            lines += '\n'
        return lines

    def generate_insert_sql(self):
        sql = f"INSERT IGNORE INTO {config.target_orders_detail_table_name}(order_id, barcode, name, count, price_per, retail_price, trade_price, category_id, unit_id) values "
        for single_product in self.products_detail:
            sql += single_product.generate_value_segment_for_sql_insert() + ", "  # 用逗號+空格隔開
        sql = sql[:-2]  # 把最後的逗號+空格去掉
        return sql


class SingleProductSoldModel(object):  # 每一件商品的設計圖
    def __init__(self, order_id, product_detail):
        self.order_id = order_id
        self.barcode = product_detail['barcode']
        self.name = product_detail['name']
        self.count = product_detail['count']
        self.price_per = product_detail['pricePer']
        self.retail_price = product_detail['retailPrice']
        self.trade_price = product_detail['tradePrice']
        self.category_id = product_detail['categoryID']
        self.unit_id = product_detail['unitID']

    # 拼接出字串
    def to_csv(self, sep=','):
        csv_line = f"{self.order_id}{sep}" \
                   f"{self.barcode}{sep}" \
                   f"{self.name}{sep}" \
                   f"{self.count}{sep}" \
                   f"{self.price_per}{sep}" \
                   f"{self.retail_price}{sep}" \
                   f"{self.trade_price}{sep}" \
                   f"{self.category_id}{sep}" \
                   f"{self.unit_id}"
        return csv_line

    def generate_value_segment_for_sql_insert(self):
        values_line = f"(" \
                      f"'{self.order_id}'," \
                      f"{str_util.check_str_null_and_transform_to_sql_null(self.barcode)}," \
                      f"{str_util.check_str_null_and_transform_to_sql_null(self.name)}," \
                      f"{self.count}," \
                      f"{self.price_per}," \
                      f"{self.retail_price}," \
                      f"{self.trade_price}," \
                      f"{self.category_id}," \
                      f"{self.unit_id}" \
                      f")"
        return values_line


if __name__ == '__main__':
    jstr = '{"discountRate": 1, "storeShopNo": "None", "dayOrderSeq": 20, "storeDistrict": "鼎城区", "isSigned": 0, "storeProvince": "湖南省", "origin": 0, "storeGPSLongitude": "111.6968", "discount": 0, "storeID": 1102, "productCount": 5, "operatorName": "OperatorName", "operator": "NameStr", "storeStatus": "open", "storeOwnUserTel": 12345678910, "payType": "wechat", "discountType": 2, "storeName": "蔚然锦和德宏商行", "storeOwnUserName": "OwnUserNameStr", "dateTS": 1542436495000, "smallChange": 0, "storeGPSName": "None", "erase": 0, "product": [{"count": 2, "name": "鱼仙贝辣味0g", "unitID": 0, "barcode": "6927018499357", "pricePer": 1, "retailPrice": 1, "tradePrice": 0, "categoryID": 1}, {"count": 1, "name": "达利园熊字饼15g", "unitID": 7, "barcode": "6911988005205", "pricePer": 3, "retailPrice": 3, "tradePrice": 2, "categoryID": 1}, {"count": 1, "name": "周氏香油条198g辣熟食南特产典辣条0包", "unitID": 7, "barcode": "6948930800014", "pricePer": 3, "retailPrice": 3, "tradePrice": 2.2, "categoryID": 1}, {"count": 2, "name": "笋尖", "unitID": 4, "barcode": "6942483999652", "pricePer": 4, "retailPrice": 4, "tradePrice": 0, "categoryID": 1}, {"count": 1, "name": "脆皮香干90g", "unitID": 8, "barcode": "6936158286437", "pricePer": 3.5, "retailPrice": 3.5, "tradePrice": 2.8, "categoryID": 1}], "storeGPSAddress": "None", "orderID": "154243648350611021331", "moneyBeforeWholeDiscount": 19.5, "storeCategory": "normal", "receivable": 19.5, "faceID": "", "storeOwnUserId": 981, "paymentChannel": 0, "paymentScenarios": "PASV", "storeAddress": "StoreAddress", "totalNoDiscount": 19.5, "payedTotal": 19.5, "storeGPSLatitude": "29.008802", "storeCreateDateTS": 1537496115000, "storeCity": "常德市", "memberID": "0"}'
    retail_order = OrdersModel(jstr)
    # print(retail_order.to_csv())
    # print(retail_order.generate_insert_sql())
    test_order = OrderDetailModel(jstr)
    # print(test_order.to_csv())
    # 這是執行插入sql的語句
    print(test_order.generate_insert_sql())
