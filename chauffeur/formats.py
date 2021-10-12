from enum import Enum


class OutputFormats:
    class Verbosity(Enum):
        GENERIC = "body"
        CONCISE = "skel"
        BRIEF = "ids"
        VERBOSE = "meta"

    class Geometry(Enum):
        FULL_GEOM = "geom"
        BOUNDING_BOX = "bb"
        CENTER_POINT = "center"

    class SortOrder(Enum):
        OBJECT_ID = "asc"
        QUADTILE = "qt"

    # Can set defaults and stuff here

opf = OutputFormats()

class OutputFormatter:
    def __init__(self,
                 verbosity=opf.Verbosity.GENERIC,
                 geometry=None,
                 sortorder=opf.SortOrder.OBJECT_ID,
                 result_limit=-1):

        self._v = verbosity
        self._g = geometry
        self._s = sortorder
        self._include_tags = False
        self._result_limit = result_limit

    def _write_tagspec(self):
        if self.IncludeTags and self.VERBOSITY is not opf.Verbosity.VERBOSE:
            return True
        return False

    @property
    def ResultLimit(self):
        return self._result_limit

    @ResultLimit.setter
    def ResultLimit(self, val):
        if type(val) is not int or val==0:
            raise ValueError("Limit must be an integer greater than zero or -1")
        self._result_limit = val

    @property
    def IncludeTags(self):
        return self._include_tags

    @IncludeTags.setter
    def IncludeTags(self, val):
        if val in (True, 1):
            self._include_tags = True
            return
        if val in (False, 0):
            if self.VERBOSITY is opf.Verbosity.VERBOSE:
                raise ValueError("Verbosity level return values cannot be modified")
            self._include_tags = False
            return
        raise ValueError("Assignment must be boolean")

    @property
    def VERBOSITY(self):
        return self._v

    @VERBOSITY.setter
    def VERBOSITY(self, mode):
        self._v = mode
        if mode is opf.Verbosity.VERBOSE:
            self._include_tags = True

    @property
    def GEOMETRY(self):
        return self._g

    @GEOMETRY.setter
    def GEOMETRY(self, mode):
        self._g = mode

    @property
    def SORTORDER(self):
        return self._s

    @SORTORDER.setter
    def SORTORDER(self, mode):
        self._s = mode

    def __repr__(self):
        s = "out"
        modes = []
        if self._v != opf.Verbosity.GENERIC:
            modes.append(self._v.value)
        if self._g is not None:
            modes.append(self._g.value)
        if self._s == opf.SortOrder.QUADTILE:
            modes.append(self._s.value)
        if self._write_tagspec():
            modes.append('tags')
        if self.ResultLimit != -1:
            modes.append(str(self.ResultLimit))
        if modes:
            s = f'''{s} {" ".join(m for m in modes)}'''
        return s + ";"

