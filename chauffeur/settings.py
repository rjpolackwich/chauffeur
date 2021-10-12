import datetime
from dateutil.parser import parse as dateparse


class BaseSetting:
    def __init_subclass__(cls, param_name, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._param_name = param_name

    @property
    def _alias(self):
        param = getattr(self, self.__class__._param_name)
        return param

    def __repr__(self):
        if self._alias is not None:
            return f'''[{self._param_name}:{self._fmt_param()}]'''
        return ""

    def _fmt_param(self):
        return self._alias



class PayloadFormat(BaseSetting, param_name="out"):
    def __init__(self, out):
        self.out = out


class Timeout(BaseSetting, param_name="timeout"):
    def __init__(self, timeout):
        self.timeout = timeout


class Maxsize(BaseSetting, param_name="maxsize"):
    def __init__(self, maxsize):
        self.maxsize = maxsize


class Bbox(BaseSetting, param_name="bbox"):
    def __init__(self, bbox):
        self.bbox = bbox

    def _fmt_param(self):
        s, w, n, e = self.bbox
        return f'''{s:.8f},{w:.8f},{n:.8f},{e:.8f}'''


class Date(BaseSetting, param_name="date"):
    def __init__(self, date):
        self.date = date

    def _fmt_param(self):
        return self.date.isoformat(timespec="seconds") + "Z"



class QuerySettings:
    DEFAULT_FORMAT = "xml"
    DEFAULT_TIMEOUT = 180
    MAXSIZE_LIMIT = 2 * 1073741824 # 2 GB is max size request

    def __init__(self,
                 payload_format=None,
                 timeout=None,
                 maxsize=None,
                 date=None,
                 bbox=None):

        self.payload_format = payload_format
        self.timeout = timeout
        self.maxsize = maxsize
        self.date = date
        self.bbox = bbox

    def __repr__(self):
        s = (
            f'''{self._out}'''
            f'''{self._timeout}'''
            f'''{self._maxsize}'''
            f'''{self._date}'''
            f'''{self._bbox}'''
        )
        if s != "":
            s += ";"
        return s

    @property
    def payload_format(self):
        return self._out.out

    @payload_format.setter
    def payload_format(self, val):
        self._out = PayloadFormat(val)

    @property
    def timeout(self):
        return self._timeout.timeout

    @timeout.setter
    def timeout(self, val):
        self._timeout = Timeout(val)

    @property
    def maxsize(self):
        return self._maxsize.maxsize

    @maxsize.setter
    def maxsize(self, val):
        self._maxsize = Maxsize(val)

    @property
    def date(self):
        return self._date.date

    @date.setter
    def date(self, val):
        self._date = Date(val)

    @property
    def bbox(self):
        return self._bbox.bbox

    @bbox.setter
    def bbox(self, val):
        self._bbox = Bbox(val)


