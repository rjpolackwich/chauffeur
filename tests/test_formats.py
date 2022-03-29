import unittest

import enum
from chauffeur.formats import OutputFormats, fmt, OutputFormatter


class TestOutputFormats(unittest.TestCase):
    def test_interface(self):
        self.assertTrue(hasattr(OutputFormats, "Verbosity"))
        self.assertTrue(hasattr(OutputFormats, "Geometry"))
        self.assertTrue(hasattr(OutputFormats, "SortOrder"))

    def test_outmodes(self):
        self.assertIsInstance(fmt.Verbosity, enum.EnumMeta)
        self.assertIsInstance(fmt.Geometry, enum.EnumMeta)
        self.assertIsInstance(fmt.SortOrder, enum.EnumMeta)
        # Test verbosity
        self.assertEqual(fmt.Verbosity.GENERIC.value, "body")
        self.assertEqual(fmt.Verbosity.CONCISE.value, "skel")
        self.assertEqual(fmt.Verbosity.BRIEF.value, "ids")
        self.assertEqual(fmt.Verbosity.VERBOSE.value, "meta")
        # Test geometry
        self.assertEqual(fmt.Geometry.FULL_GEOM.value, "geom")
        self.assertEqual(fmt.Geometry.BOUNDING_BOX.value, "bb")
        self.assertEqual(fmt.Geometry.CENTER_POINT.value, "center")
        # Test sortorder
        self.assertEqual(fmt.SortOrder.OBJECT_ID.value, "asc")
        self.assertEqual(fmt.SortOrder.QUADTILE.value, "qt")

    def test_OutputFormatter(self):
        self.assertIsInstance(OutputFormatter.VERBOSITY, property)
        self.assertIsInstance(OutputFormatter.GEOMETRY, property)
        self.assertIsInstance(OutputFormatter.SORTORDER, property)
        opftr = OutputFormatter()
        self.assertEqual(opftr.VERBOSITY, fmt.Verbosity.GENERIC)
        self.assertIsNone(opftr.GEOMETRY)
        self.assertEqual(opftr.SORTORDER, fmt.SortOrder.OBJECT_ID)
        self.assertEqual(repr(opftr), "out;")

    def test_MetaOptions(self):
        opftr = OutputFormatter()
        opftr.IncludeTags = True
        opftr.ResultLimit = 10
        self.assertEqual(repr(opftr), "out tags 10;")

