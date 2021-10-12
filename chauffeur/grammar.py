import itertools
import collections
from .filters import CompoundFilter


class OSMElement:
    geom_type = NotImplemented

    @classmethod
    def _fmt(cls):
        return cls.__name__.lower()


class Node(OSMElement):
    _level = 1


class Way(OSMElement):
    _level = 2


class Relation(OSMElement):
    _level = 3


class AbstractQueryStatement:
    _input = None
    _output = None
    _default_name = "_"

    def __init__(self, inputs=None, name=None, filters=None):
        if inputs:
            self._inputs = inputs
        if name:
            self._name = name
        self.filters = CompoundFilter(filters)

    def _fmt_statement(self):
        raise NotImplementedError

    def __repr__(self):
        return f'''{self._fmt_statement()};'''

    def __add__(self, other):
        if isinstance(other, AbstractQueryStatement):
            return UnionQuerySet([self, other])
        raise NotImplementedError

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, AbstractQueryStatement):
            # Check output type match
            return DifferenceQuerySet([self, other])
        raise NotImplementedError

    def __rsub__(self, other):
        return NotImplemented

    def __isub__(self, other):
        return self.__sub__(other)

    def union(self, other):
        return self + other

    def difference(self, other):
        return self - other

    def iunion(self, other):
        self += other

    def idifference(self, other):
        self -= other



class GenericElementQuery(AbstractQueryStatement):
    _element = NotImplemented
    _input = None

    def __init__(self, name=None, filters=None):
        super().__init__(name=name, filters=filters)

    def add_filter(self, _filter):
        self.filters.add_filter(_filter)

    @property
    def _output(self):
        return self._element

    def _fmt_element(self):
        return f'''{self._element._fmt()}'''

    def _fmt_statement(self):
        msg = f'''{self._fmt_element()}'''
        if self.filters.filters:
            msg = f'''{msg}{self.filters}'''
        return msg


class CompoundQuery(GenericElementQuery):
    _elements = ()

    @property
    def _output(self):
        return self._elements

    def _fmt_element(self):
        return f'''{"".join(e._fmt()[0] for e in self._elements)}'''



class BaseQuerySet(AbstractQueryStatement):
    def __init__(self, query_statements=None):
        if query_statements is None:
            self.query_statements = list()
        else:
            self.query_statements = query_statements # gross

    @property
    def _output(self):
        _outputs = []
        for qs in self.query_statements:
            if isinstance(qs._output, collections.abc.Sequence):
                o = list(qs._output)
                _outputs.extend(o)
            else:
                _outputs.append(qs._output)
        return tuple(sorted(list(set(_outputs)), key=lambda elm: elm._level))

    def __iter__(self):
        return iter(self.query_statements)

    def __repr__(self):
        return f'''({self._fmt_statement()});'''


class UnionQuerySet(BaseQuerySet):
    def _fmt_statement(self):
        return f'''{"".join(repr(qs) for qs in self.query_statements)}'''


class DifferenceQuerySet(BaseQuerySet):
    def __init__(self, query_statements=None):
        assert len(query_statements) == 2
        super().__init__(query_statements)
        self.minued, self.subtrahend = query_statements

    def _fmt_statement(self):
        return f'''{self.minued} - {self.subtrahend}'''


