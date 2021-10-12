import unittest

import enum
from chauffeur.formats import OutputFormats, opf, OutputFormatter


class TestOutputFormats(unittest.TestCase):
    def test_interface(self):
        self.assertTrue(hasattr(OutputFormats, "Verbosity"))
        self.assertTrue(hasattr(OutputFormats, "Geometry"))
        self.assertTrue(hasattr(OutputFormats, "SortOrder"))

    def test_outmodes(self):
        self.assertIsInstance(opf.Verbosity, enum.EnumMeta)
        self.assertIsInstance(opf.Geometry, enum.EnumMeta)
        self.assertIsInstance(opf.SortOrder, enum.EnumMeta)
        # Test verbosity
        self.assertEqual(opf.Verbosity.GENERIC.value, "body")
        self.assertEqual(opf.Verbosity.CONCISE.value, "skel")
        self.assertEqual(opf.Verbosity.BRIEF.value, "ids")
        self.assertEqual(opf.Verbosity.VERBOSE.value, "meta")
        # Test geometry
        self.assertEqual(opf.Geometry.FULL_GEOM.value, "geom")
        self.assertEqual(opf.Geometry.BOUNDING_BOX.value, "bb")
        self.assertEqual(opf.Geometry.CENTER_POINT.value, "center")
        # Test sortorder
        self.assertEqual(opf.SortOrder.OBJECT_ID.value, "asc")
        self.assertEqual(opf.SortOrder.QUADTILE.value, "qt")

    def test_OutputFormatter(self):
        self.assertIsInstance(OutputFormatter.VERBOSITY, property)
        self.assertIsInstance(OutputFormatter.GEOMETRY, property)
        self.assertIsInstance(OutputFormatter.SORTORDER, property)
        opftr = OutputFormatter()
        self.assertEqual(opftr.VERBOSITY, opf.Verbosity.GENERIC)
        self.assertIsNone(opftr.GEOMETRY)
        self.assertEqual(opftr.SORTORDER, opf.SortOrder.OBJECT_ID)
        self.assertEqual(repr(opftr), "out;")

    def test_MetaOptions(self):
        opftr = OutputFormatter()
        opftr.IncludeTags = True
        opftr.ResultLimit = 10
        self.assertEqual(repr(opftr), "out tags 10;")

