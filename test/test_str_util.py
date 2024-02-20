from unittest import TestCase
from util.str_util import check_null, check_str_null_and_transform_to_sql_null


class TestStrUtil(TestCase):
    def setUp(self):
        pass

    def test_check_null(self):
        s = None
        self.assertTrue(check_null(s))

        s = 'None'
        self.assertTrue(check_null(s))

        s = "None"
        self.assertTrue(check_null(s))

        s = "NONE  "
        self.assertTrue(check_null(s))
        s = ""
        self.assertTrue(check_null(s))

        s = "Undefined"
        self.assertTrue(check_null(s))

        s = "undefined"
        self.assertTrue(check_null(s))

        s = "有意義的字符串"
        self.assertFalse(check_null(s))
        pass

    def test_check_str_null_and_transform_to_sql_null(self):
        s = None
        result = check_str_null_and_transform_to_sql_null(s)
        self.assertEqual(result, "None")

        s = 1
        result = check_str_null_and_transform_to_sql_null(s)
        self.assertEqual(result, "'1'")

        s = '高雄'
        result = check_str_null_and_transform_to_sql_null(s)
        self.assertEqual(result, "'高雄'")

    def tearDown(self):
        pass
