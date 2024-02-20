from logging import RootLogger
from unittest import TestCase
from util.logger_util import init_logger


class TestLoggingUtil(TestCase):
    def setUp(self) -> None:
        pass

    def test_init_logger(self):
        logger = init_logger()
        result = isinstance(logger, RootLogger)  # 回傳的result是boolen
        self.assertEqual(result, True)
        pass

    def tearDown(self) -> None:
        pass


