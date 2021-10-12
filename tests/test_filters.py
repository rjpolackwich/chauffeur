import unittest

from chauffeur.filters import Filter, CompoundFilter, GenericFilter
from chauffeur.filters import IdFilter, UserFilter, BboxFilter, TagFilter


class TestBaseFilters(unittest.TestCase):
    def test_Filter(self):
        self.assertTrue(hasattr(Filter, "_fmt"))
        self.assertTrue(hasattr(Filter, "__add__"))
        self.assertTrue(hasattr(Filter, "__radd__"))
        self.assertTrue(hasattr(Filter, "__iadd__"))
        with self.assertRaises(NotImplementedError):
            repr(Filter())

    def test_CompoundFilter(self):
        self.assertTrue(hasattr(CompoundFilter, "__add__"))
        self.assertTrue(hasattr(CompoundFilter, "__radd__"))
        self.assertTrue(hasattr(CompoundFilter, "__iadd__"))
        self.assertTrue(hasattr(CompoundFilter, "add_filter"))
        self.assertTrue(isinstance(CompoundFilter.filters, property))
        cf = CompoundFilter()
        self.assertIsInstance(cf.filters, list)

    def test_GenericFilter(self):
        self.assertTrue(issubclass(GenericFilter, Filter))


class TestGenericFilters(unittest.TestCase):
    def test_UserFilter(self):
        self.assertTrue(issubclass(UserFilter, GenericFilter))
        test_fstring = "[highway]"
        self.assertEqual(repr(UserFilter(test_fstring)), test_fstring)

    def test_IdFilter(self):
        self.assertTrue(issubclass(IdFilter, GenericFilter))
        self.assertTrue(isinstance(IdFilter.osm_id, property))
        test_id = 102302
        self.assertEqual(repr(IdFilter(test_id)), f'''(id:{test_id})''')

    def test_BboxFilter(self):
        self.assertTrue(issubclass(BboxFilter, GenericFilter))
        test_bbox = [50.6, 7.0, 50.8, 7.3]
        self.assertEqual(repr(BboxFilter(test_bbox)), "(50.60000000,7.00000000,50.80000000,7.30000000)")

    def test_TagFilter(self):
        self.assertTrue(issubclass(TagFilter, GenericFilter))
        test_tagkey = "building"
        # Test key value exists:
        self.assertEqual(repr(TagFilter(test_tagkey)), f'''[{test_tagkey}]''')
        # Test key value does not exist:
        self.assertEqual(repr(TagFilter(test_tagkey, exists=False)), f'''[!{test_tagkey}]''')
        # Test key exists with value:
        test_tagvals = "school"
        self.assertEqual(repr(TagFilter(test_tagkey, test_tagvals)), f'''[{test_tagkey}={test_tagvals}]''')
        # Test key exists with at least one of many values:
        test_tagvals = ["school", "college"]
        exp = f'''[{test_tagkey}~"^({test_tagvals[0]}|{test_tagvals[1]})$"]'''
        self.assertEqual(repr(TagFilter(test_tagkey, vals=test_tagvals)), exp)
        # Test key exists without any of many values:
        exp = f'''[{test_tagkey}][{test_tagkey}!~"^({test_tagvals[0]}|{test_tagvals[1]})$"]'''
        self.assertEqual(repr(TagFilter(test_tagkey, test_tagvals, exists=False)), exp)



if __name__ == "__main__":
    unittest.main()
