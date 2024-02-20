import logging
# 自定義一個logging類
from config.project_config import log_root_path, log_dir, level


class Logging:
    def __init__(self, level=20):
        self.logger = logging.getLogger()
        self.logger.setLevel(level)


# 自定義一個logger
def init_logger():
    logger = Logging(level=level).logger
    # 避免重複添加stream_handler,file_handler
    if logger.handlers:
        return logger
    # 建造handler對象
    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(log_root_path+log_dir, mode='a',encoding='utf-8')
    fmt = logging.Formatter('%(asctime)s - [%(levelname)s] - %(filename)s[%(lineno)d]:  %(message)s')
    stream_handler.setFormatter(fmt)
    file_handler.setFormatter(fmt)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger

