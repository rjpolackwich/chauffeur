import unittest
import collections.abc

from chauffeur.grammar import OSMElement, Node, Way, Relation
from chauffeur.grammar import AbstractQueryStatement, GenericElementQuery, BaseQuerySet
from chauffeur.grammar import UnionQuerySet, DifferenceQuerySet, CompoundQuery
from chauffeur.filters import CompoundFilter


class TestOSMElements(unittest.TestCase):
    def test_Node(self):
        self.assertIsInstance(Node(), OSMElement)
        self.assertEqual(Node._level, 1)
        self.assertEqual("node", Node._fmt())

    def test_Way(self):
        self.assertIsInstance(Way(), OSMElement)
        self.assertEqual(Way._level, 2)
        self.assertEqual("way", Way._fmt())

    def test_Relation(self):
        self.assertIsInstance(Relation(), OSMElement)
        self.assertEqual(Relation._level, 3)
        self.assertEqual("relation", Relation._fmt())


class TestBaseQueryObjects(unittest.TestCase):
    def test_AbstractInterface(self):
        self.assertIsNone(AbstractQueryStatement._input)
        self.assertIsNone(AbstractQueryStatement._output)
        self.assertEqual(AbstractQueryStatement._default_name, "_")
        inst = AbstractQueryStatement()
        self.assertFalse(hasattr(inst, "_name"))
        self.assertIsInstance(inst.filters, CompoundFilter)
        self.assertTrue(hasattr(inst, "_fmt_statement"))
        self.assertTrue(hasattr(inst, "__add__"))
        self.assertTrue(hasattr(inst, "__radd__"))
        self.assertTrue(hasattr(inst, "__iadd__"))
        self.assertTrue(hasattr(inst, "__sub__"))
        self.assertTrue(hasattr(inst, "__rsub__"))
        self.assertTrue(hasattr(inst, "__isub__"))
        self.assertTrue(hasattr(inst, "union"))
        self.assertTrue(hasattr(inst, "difference"))

    def test_GenericElementQuery(self):
        self.assertTrue(issubclass(GenericElementQuery, AbstractQueryStatement))
        self.assertEqual(GenericElementQuery._element, NotImplemented)
        self.assertIsNone(GenericElementQuery._input)
        self.assertIsInstance(GenericElementQuery._output, property)
        self.assertTrue(hasattr(GenericElementQuery, "add_filter"))
        self.assertTrue(hasattr(GenericElementQuery, "_fmt_element"))

    def test_CompoundQuery(self):
        self.assertTrue(issubclass(CompoundQuery, GenericElementQuery))
        self.assertTrue(hasattr(CompoundQuery, "_elements"))

    def test_BaseQuerySet(self):
        self.assertTrue(issubclass(BaseQuerySet, AbstractQueryStatement))
        bqs = BaseQuerySet()
        self.assertIsInstance(bqs, collections.abc.Iterable)
        self.assertIsInstance(bqs.query_statements, list)

    def test_UnionQuerySet(self):
        self.assertTrue(issubclass(UnionQuerySet, BaseQuerySet))

    def test_DifferenceQuerySet(self):
        self.assertTrue(issubclass(DifferenceQuerySet, BaseQuerySet))



if __name__ == "__main__":
    unittest.main()
