"""設計一個log的class(設計圖)來承載log的data"""
import config.project_config as config


class BackendLogModel:
    def __init__(self, data: str):
        # log_data的格式：2024-02-19 03:54:35.586436	[INFO]	event.py	响应时间:164ms	北京市	大兴区	这里是日志信息......
        # 是str
        data = data.split('\t')
        self.log_time = data[0]
        self.log_level = data[1].strip('[]')
        self.log_module = data[2]
        self.response_time = data[3][5:-2]
        self.province = data[4]
        self.city = data[5]
        self.log_text = data[6]

    def to_csv(self, sep=','):
        csv_line = \
            f"{self.log_time}{sep}" \
            f"{self.log_level}{sep}" \
            f"{self.log_module}{sep}" \
            f"{self.response_time}{sep}" \
            f"{self.province}{sep}" \
            f"{self.city}{sep}" \
            f"{self.log_text}"
        return csv_line

    def generate_insert_to_sql(self):
        sql = (f"INSERT INTO {config.target_backend_table_name}"
               f"(log_time,log_level,log_module,response_time,province,city,log_text) VALUES("
               f"'{self.log_time}',"
               f"'{self.log_level}',"
               f"'{self.log_module}',"
               f"'{self.response_time}',"
               f"'{self.province}',"
               f"'{self.city}',"
               f"'{self.log_text}'"
               f")")
        return sql


if __name__ == '__main__':
    log_data = '2024-02-19 03:54:35.585248	[INFO]	goods_manager.py	响应时间:404ms	北京市	怀柔区	这里是日志信息......'
    backend_log = BackendLogModel(log_data)
    print(backend_log.generate_insert_to_sql())
    print(backend_log.to_csv())
