import unittest

from chauffeur.query import *
from chauffeur.query import QueryRegister
from chauffeur.grammar import Node, Way, Relation, GenericElementQuery, CompoundQuery
from chauffeur.grammar import UnionQuerySet, DifferenceQuerySet
from chauffeur.settings import QuerySettings
from chauffeur.formats import opf, OutputFormatter
from chauffeur.filters import TagFilter


class TestElementQueryClasses(unittest.TestCase):
    def test_NodeQuery(self):
        self.assertTrue(issubclass(NodeQuery, GenericElementQuery))
        self.assertEqual(NodeQuery._element, Node)
        self.assertEqual(NodeQuery()._fmt_element(), "node")

    def test_WayQuery(self):
        self.assertTrue(issubclass(WayQuery, GenericElementQuery))
        self.assertEqual(WayQuery._element, Way)
        self.assertEqual(WayQuery()._fmt_element(), "way")

    def test_RelationQuery(self):
        self.assertTrue(issubclass(RelationQuery, GenericElementQuery))
        self.assertEqual(RelationQuery._element, Relation)
        self.assertEqual(RelationQuery()._fmt_element(), "relation")

    def test_NodeWayQuery(self):
        self.assertTrue(issubclass(NodeWayQuery, CompoundQuery))
        self.assertEqual(NodeWayQuery._elements, (Node, Way))
        self.assertEqual(NodeWayQuery()._fmt_element(), "nw")

    def test_NodeRelationQuery(self):
        self.assertTrue(issubclass(NodeWayQuery, CompoundQuery))
        self.assertEqual(NodeRelationQuery._elements, (Node, Relation))
        self.assertEqual(NodeRelationQuery()._fmt_element(), "nr")

    def test_WayRelationQuery(self):
        self.assertTrue(issubclass(WayRelationQuery, CompoundQuery))
        self.assertEqual(WayRelationQuery._elements, (Way, Relation))
        self.assertEqual(WayRelationQuery()._fmt_element(), "wr")

    def test_NodeWayRelationQuery(self):
        self.assertTrue(issubclass(NodeWayRelationQuery, CompoundQuery))
        self.assertEqual(NodeWayRelationQuery._elements, (Node, Way, Relation))
        self.assertEqual(NodeWayRelationQuery()._fmt_element(), "nwr")


class TestQueryOperations(unittest.TestCase):
    def setUp(self):
        self.tf_rail = TagFilter("railway", "station")
        self.tf_trans = TagFilter("public_transport", "station")
        self.tf_bus = TagFilter("amenity", "bus_station")
        self.nq = NodeQuery()
        self.nwrq =NodeWayRelationQuery()

    def test_filter_description(self):
        # Test initialize and append
        q = NodeWayRelationQuery(filters=self.tf_rail)
        self.nq.add_filter(self.tf_rail)
        self.assertEqual(q.filters.filters, self.nq.filters.filters)
        q = NodeWayRelationQuery(filters=(self.tf_rail, self.tf_trans))
        self.nq.add_filter(self.tf_trans)
        self.assertEqual(q.filters.filters, self.nq.filters.filters)

    @unittest.expectedFailure
    def test_filter_reassign(self):
        self.nq.add_filter(tf_rail)
        with self.assertRaises(AttributeError):
            self.nq.filters = self.tf_trans

    def test_additive_emulations(self):
        self.nwrq.add_filter((self.tf_rail, self.tf_trans))
        self.nq.add_filter(self.tf_bus)
        # __add__
        rq = self.nwrq + self.nq
        self.assertIsInstance(rq, UnionQuerySet)
        self.assertEqual(repr(rq), f'''(nwr{self.tf_rail}{self.tf_trans};node{self.tf_bus};);''')
        # __iadd__
        self.nwrq += self.nq
        self.assertIsInstance(self.nwrq, UnionQuerySet)
        self.assertEqual(repr(rq), repr(self.nwrq))

    def test_subtractive_emulations(self):
        self.nwrq.add_filter((self.tf_rail, self.tf_trans))
        self.nq.add_filter(self.tf_bus)
        # __sub__
        rq = self.nwrq - self.nq
        self.assertIsInstance(rq, DifferenceQuerySet)
        self.assertIs(rq.minued, self.nwrq)
        self.assertIs(rq.subtrahend, self.nq)
        self.assertEqual(repr(rq), f'''(nwr{self.tf_rail}{self.tf_trans}; - node{self.tf_bus};);''')
        # __isub__
        self.nwrq -= self.nq
        self.assertEqual(repr(rq), repr(self.nwrq))


class TestQueryBuilder(unittest.TestCase):
    def setUp(self):
        self.qb = QueryBuilder()
        self.tf_rail = TagFilter("railway", "station")
        self.tf_trans = TagFilter("public_transport", "station")
        self.nwrq =NodeWayRelationQuery(filters=(self.tf_rail, self.tf_trans))

    def test_interface(self):
        self.assertTrue(hasattr(QueryBuilder, "overpass_endpoint"))
        self.assertIsInstance(QueryBuilder.GlobalBoundingBox, property)
        self.assertIsInstance(QueryBuilder.raw_query_string, property)
        self.assertTrue(hasattr(QueryBuilder, "request"))
        self.assertEqual(self.qb.name, "default")
        self.assertIsInstance(self.qb.settings, QuerySettings)
        self.assertIsInstance(self.qb.output_mode, OutputFormatter)
        self.assertIsInstance(self.qb.qsx, QueryRegister)
        self.assertEqual(self.qb.output_mode.SORTORDER, opf.SortOrder.QUADTILE)

    def test_query_assignment_basic(self):
        self.qb.qsx.append(self.nwrq)
        self.assertIs(self.qb.qsx._dset, self.nwrq)
        self.assertEqual(self.qb.qsx.output, self.nwrq._output)
        self.assertEqual(repr(self.qb.qsx), repr(self.nwrq))

    @unittest.skip("Experimental Interface")
    def test_named_query_assignment(self):
        pass

    @unittest.skip("Experimental Interface")
    def test_dynamic_statement_chaining(self):
        pass

    def test_overpass_endpoint(self):
        self.assertEqual(QueryBuilder.overpass_endpoint, 'http://overpass-api.de/api/interpreter')


if __name__ == "__main__":
    unittest.main()


