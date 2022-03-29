from enum import Enum
from collections import OrderedDict, defaultdict
import functools
import csv

from .grammar import Node, Way, Relation, GenericElementQuery, CompoundQuery
from .settings import QuerySettings
from .filters import BboxFilter, TagFilter, IdFilter, UserFilter
from .formats import OutputFormatter, fmt

import requests


__all__ = ["NodeQuery",
           "WayQuery",
           "RelationQuery",
           "NodeWayQuery",
           "NodeRelationQuery",
           "WayRelationQuery",
           "NodeWayRelationQuery",
           "QueryBuilder",
           ]

def reduce_union_or(querylist):
    return functools.reduce(lambda x, y: x + y, querylist)


class NodeQuery(GenericElementQuery):
    _element = Node


class WayQuery(GenericElementQuery):
    _element = Way


class RelationQuery(GenericElementQuery):
    _element = Relation


class NodeWayQuery(CompoundQuery):
    _elements = (Node, Way)


class NodeRelationQuery(CompoundQuery):
    _elements = (Node, Relation)


class WayRelationQuery(CompoundQuery):
    _elements = (Way, Relation)


class NodeWayRelationQuery(CompoundQuery):
    _elements = (Node, Way, Relation)


query_index_lut = dict()
query_index_lut[( (Node._level,) )] = NodeQuery
query_index_lut[( (Way._level,) )] = WayQuery
query_index_lut[( (Relation._level) )] = RelationQuery
query_index_lut[( (Node._level, Way._level) )] = NodeWayQuery
query_index_lut[( (Node._level, Relation._level) )] = NodeRelationQuery
query_index_lut[( (Way._level, Relation._level) )] = WayRelationQuery
query_index_lut[( (Node._level, Way._level, Relation._level) )] = NodeWayRelationQuery


def element_query_factory(levels):
    assert isinstance(levels, (list, tuple))
    assert 1 <= len(levels) <= 3
    for lev in levels:
        assert isinstance(lev, int)
        assert 1 <= lev <= 3
    levels = list(levels)
    levels = sorted(levels)
    levels = tuple(levels)
    qc = query_index_lut[levels]
    if isinstance(qc, tuple):
        qc = qc[0]
    return qc



class QueryRegister:
    def __init__(self, qb):
        self.qb = qb
        self.qc = list()
        self.r = OrderedDict()

#    def __getattr__(self, qname):
#        try:
#            return self.r[qname]
#        except KeyError:
#            raise NameError("Named query: {} does not exist".format(qname))

    def append(self, qs, name=None):
        if not self.qc:
            assert qs._input is None
        if not name:
            self.qc.append(qs)
        else:
            self.r[name] = qs
            self.qc.append(name)

    @property
    def _dset(self):
        _ = reversed(self.qc)
        while True:
            item = next(_)
            if item not in self.r.keys():
                return item

    @property
    def output(self):
        return self._dset._output

    def __repr__(self):
        s =  f'''{"".join(repr(qs) for qs in self.qc)}'''
        if self.qb.auto_recourse_down and self.output != Node:
            if self.qb.output_mode.VERBOSITY is (fmt.Verbosity.CONCISE or fmt.Verbosity.GENERIC):
                if self.qb.output_mode.GEOMETRY is None:
                    s += "(._;>;);"
        return s



class QueryBuilder:
    overpass_endpoint = 'http://overpass-api.de/api/interpreter'

    def __init__(self,
                 name="default",
                 basic_optimize=True,
                 auto_recourse=True,
                 **kwargs):
        self.name = name
        self.settings = QuerySettings(**kwargs)
        self.output_mode = OutputFormatter()
        self.qsx = QueryRegister(self)
        if basic_optimize:
            self.output_mode.SORTORDER = fmt.SortOrder.QUADTILE
        self.auto_recourse_down = auto_recourse

    @property
    def GlobalBoundingBox(self):
        return self.settings.bbox

    @GlobalBoundingBox.setter
    def GlobalBoundingBox(self, bbox):
        self.settings.bbox = bbox

    def include_geometries(self):
        self.output_mode.GEOMETRY = fmt.Geometry.FULL_GEOM

    def include_boundingboxes(self):
        self.output_mode.GEOMETRY = fmt.Geometry.BOUNDING_BOX

    def include_centerpoints(self):
        self.output_mode.GEOMETRY = fmt.Geometry.CENTER_POINT

    @property
    def raw_query_string(self):
        return f'''{self.settings}{self.qsx}{self.output_mode}'''

    @classmethod
    def from_query(cls, query, *args, **kwargs):
        inst = cls(*args, **kwargs)
        cls._query = query

    def request(self):
        return requests.get(self.overpass_endpoint, data=self.raw_query_string)




