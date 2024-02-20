from unittest import TestCase
from util.time_util import ts10_to_date_str, ts13_to_date_str


class TestTimeUtil(TestCase):
    def setUp(self) -> None:
        pass

    def test_ts10_to_date_str(self):
        ts = 1706838265
        result = ts10_to_date_str(ts, "%Y-%m-%d %H:%M:%S")
        expected = '2024-02-02 09:44:25'
        self.assertEqual(result, expected)
        pass

    def test_ts13_to_date_str(self):
        ts = 1706838265000
        result = ts13_to_date_str(ts, "%Y-%m-%d %H:%M:%S")
        expected = '2024-02-02 09:44:25'
        self.assertEqual(result, expected)
        pass

    def tearDown(self) -> None:
        pass
