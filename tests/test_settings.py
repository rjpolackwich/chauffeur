import unittest
import datetime as dt

from chauffeur.settings import BaseSetting, QuerySettings
from chauffeur.settings import PayloadFormat, Timeout, Maxsize, Date, Bbox


class TestSettings(unittest.TestCase):
    def test_BaseSettings(self):
        self.assertTrue(hasattr(BaseSetting, "_fmt_param"))
        self.assertIsInstance(BaseSetting._alias, property)

    def test_QuerySettings(self):
        self.assertEqual(QuerySettings.DEFAULT_FORMAT, "xml")
        self.assertEqual(QuerySettings.DEFAULT_TIMEOUT, 180)
        self.assertEqual(QuerySettings.MAXSIZE_LIMIT, 2 * 1073741824)
        self.assertIsInstance(QuerySettings.payload_format, property)
        self.assertIsInstance(QuerySettings.timeout, property)
        self.assertIsInstance(QuerySettings.maxsize, property)
        self.assertIsInstance(QuerySettings.bbox, property)
        # Test that defaults to empty string without param
        qs = QuerySettings()
        self.assertEqual(repr(qs), "")
        # Test full init
        test_format = 'json'
        test_timeout = 3600
        test_maxsize = 1073741824
        test_date = dt.datetime.today()
        test_bbox = [1.0, 2.0, 3.0, 4.0]
        qs = QuerySettings(payload_format=test_format,
                           timeout=test_timeout,
                           maxsize=test_maxsize,
                           date=test_date,
                           bbox=test_bbox)
        self.assertIsInstance(qs._out, PayloadFormat)
        self.assertEqual(qs._out._fmt_param(), test_format)
        self.assertIsInstance(qs._timeout, Timeout)
        self.assertEqual(qs._timeout._fmt_param(), test_timeout)
        self.assertIsInstance(qs._date, Date)
        self.assertEqual(qs._date._fmt_param(), test_date.isoformat(timespec="seconds") + "Z")
        self.assertIsInstance(qs._bbox, Bbox)
        self.assertEqual(qs._bbox._fmt_param(), f'''{test_bbox[0]:.8f},{test_bbox[1]:.8f},{test_bbox[2]:.8f},{test_bbox[3]:.8f}''')
        # Test output statement
        exp = (
            f'''[out:{qs._out._fmt_param()}]'''
            f'''[timeout:{qs._timeout._fmt_param()}]'''
            f'''[maxsize:{qs._maxsize._fmt_param()}]'''
            f'''[date:{qs._date._fmt_param()}]'''
            f'''[bbox:{qs._bbox._fmt_param()}];'''
        )
        self.assertEqual(repr(qs), exp)


if __name__ == "__main__":
    unittest.main()
