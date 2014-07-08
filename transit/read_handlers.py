import transit_types
from constants import *
import uuid
import ctypes
import dateutil.parser
import datetime
import dateutil.tz
from helpers import pairs

## Read handlers are used by the decoder when parsing/reading in Transit
## data and returning Python objects

class DefaultHandler(object):
    @staticmethod
    def from_rep(t, v):
        return transit_types.TaggedValue(t, v)

class NoneHandler(object):
    @staticmethod
    def from_rep(_):
        return None

class KeywordHandler(object):
    @staticmethod
    def from_rep(v):
        return transit_types.Keyword(v)

class SymbolHandler(object):
    @staticmethod
    def from_rep(v):
        return transit_types.Symbol(v)

class BooleanHandler(object):
    @staticmethod
    def from_rep(x):
        return x == "t"

class IntHandler(object):
    @staticmethod
    def from_rep(v):
        return int(v)

class FloatHandler(object):
    @staticmethod
    def from_rep(v):
        return float(v)

class UuidHandler(object):
    @staticmethod
    def from_rep(u):
        """ Given a string, return a UUID object"""
        if isinstance(u, basestring):
            return uuid.UUID(u)

        # hack to remove signs
        a = ctypes.c_ulong(u[0])
        b = ctypes.c_ulong(u[1])
        combined = a.value << 64 | b.value
        return uuid.UUID(int=combined)

class UriHandler(object):
    @staticmethod
    def from_rep(u):
        return transit_types.URI(u)

class DateHandler(object):
    @staticmethod
    def from_rep(d):
        if isinstance(d, (long, int)):
            return DateHandler._convert_timestamp(d)
        if "T" in d:
            return dateutil.parser.parse(d)
        return DateHandler._convert_timestamp(long(d))
    @staticmethod
    def _convert_timestamp(ms):
        """ Given a timestamp in ms, return a DateTime object"""
        return datetime.datetime.fromtimestamp(ms/1000.0, dateutil.tz.tzutc())

class BigIntegerHandler(object):
    @staticmethod
    def from_rep(d):
        return long(d)

class LinkHandler(object):
    @staticmethod
    def from_rep(l):
        return transit_types.Link(**l)

class ListHandler(object):
    @staticmethod
    def from_rep(l):
        return l

class SetHandler(object):
    @staticmethod
    def from_rep(s):
        return frozenset(s)

class CmapHandler(object):
    @staticmethod
    def from_rep(cmap):
        return transit_types.frozendict(pairs(cmap))

class IdentityHandler(object):
    @staticmethod
    def from_rep(i):
        return i

