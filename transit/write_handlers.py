## Copyright (c) Cognitect, Inc.
## All rights reserved.

from constants import *
from class_hash import ClassDict
from transit_types import Keyword, Symbol, URI, frozendict, TaggedValue, Link
import uuid
import datetime, time
from dateutil import tz

## This file contains Write Handlers - all the top-level objects used when
## writing Transit data.  These object must all be immutable and pickleable.

class TaggedMap(object):
    def __init__(self, tag, rep, str):
        self._tag = tag
        self._rep = rep
        self._str = str
    def tag(self):
        return self._tag
    def rep(self):
        return self._rep
    def string_rep(self):
        return self._str

class NoneHandler(object):
    @staticmethod
    def tag(_):
        return '_'
    @staticmethod
    def rep(_):
        return None
    @staticmethod
    def string_rep(n):
        return None

class IntHandler(object):
    @staticmethod
    def tag(i):
        return 'i'
    @staticmethod
    def rep(i):
        return i
    @staticmethod
    def string_rep(i):
        return str(i)

class BigIntHandler(object):
    @staticmethod
    def tag(_):
        return "n"
    @staticmethod
    def rep(n):
        return str(n)
    @staticmethod
    def string_rep(n):
        return str(n)

class FloatHandler(object):
    @staticmethod
    def tag(_):
        return "f"
    @staticmethod
    def rep(f):
        return str(f)
    @staticmethod
    def string_rep(f):
        return str(f)

class StringHandler(object):
    @staticmethod
    def tag(s):
        return 's'
    @staticmethod
    def rep(s):
        return s
    @staticmethod
    def string_rep(s):
        return s

class BooleanHandler(object):
    @staticmethod
    def tag(_):
        return '?'
    @staticmethod
    def rep(b):
        return b
    @staticmethod
    def string_rep(b):
        return b and 't' or 'f'

class ArrayHandler(object):
    @staticmethod
    def tag(a):
        return 'array'
    @staticmethod
    def rep(a):
        return a
    @staticmethod
    def string_rep(a):
        return None

class MapHandler(object):
    @staticmethod
    def tag(m):
        return 'map'
    @staticmethod
    def rep(m):
        return m
    @staticmethod
    def string_rep(m):
        return None

class KeywordHandler(object):
    @staticmethod
    def tag(k):
        return ':'
    @staticmethod
    def rep(k):
        return str(k)
    @staticmethod
    def string_rep(k):
        return str(k)

class SymbolHandler(object):
    @staticmethod
    def tag(s):
        return '$'
    @staticmethod
    def rep(s):
        return str(s)
    @staticmethod
    def string_rep(s):
        return str(s)

class UuidHandler(object):
    mask = pow(2, 64) - 1
    @staticmethod
    def tag(_):
        return "u"
    @staticmethod
    def rep(u):
        i = u.int
        return (i >> 64, i & UuidHandler.mask)
    @staticmethod
    def string_rep(u):
        return str(u)

class UriHandler(object):
    @staticmethod
    def tag(_):
        return "r"
    @staticmethod
    def rep(u):
        return u.rep
    @staticmethod
    def string_rep(u):
        return u.rep

class DateTimeHandler(object):
    epoch = datetime.datetime(1970, 1, 1).replace(tzinfo=tz.tzutc())
    @staticmethod
    def tag(_):
        return "m"
    @staticmethod
    def rep(d):
        td = d - DateTimeHandler.epoch
        return long((td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 1e3)
    @staticmethod
    def verbose_handler():
        return VerboseDateTimeHandler
    @staticmethod
    def string_rep(d):
        return str(DateTimeHandler.rep(d))

class VerboseDateTimeHandler(object):
    @staticmethod
    def tag(_):
        return "t"
    @staticmethod
    def rep(d):
        return d.isoformat()
    @staticmethod
    def string_rep(d):
        return d.isoformat()

class SetHandler(object):
    @staticmethod
    def tag(_):
        return "set"
    @staticmethod
    def rep(s):
        return TaggedMap("array", tuple(s), None)
    @staticmethod
    def string_rep(_):
        return None

class MapHandler(object):
    @staticmethod
    def tag(_):
        return "map"
    @staticmethod
    def rep(m):
        return m
    @staticmethod
    def string_rep(_):
        return None

class TaggedValueHandler(object):
    @staticmethod
    def tag(tv):
        return tv.tag
    @staticmethod
    def rep(tv):
        return tv.rep
    @staticmethod
    def string_rep(_):
        return None

class LinkHandler(object):
    @staticmethod
    def tag(_):
        return "link"
    @staticmethod
    def rep(l):
        return l.as_map
    @staticmethod
    def string_rep(_):
        return None

class WriteHandler(ClassDict):
    """This is the master handler for encoding/writing Python data into
    Transit data, based on its type.
    The Handler itself is a dispatch map, that resolves on full type/object
    inheritance.

    These handlers can be overriden during the creation of a Transit Writer."""

    def __init__(self):
        super(WriteHandler, self).__init__()
        self[type(None)] = NoneHandler
        self[bool] = BooleanHandler
        self[str] = StringHandler
        self[unicode] = StringHandler
        self[list] = ArrayHandler
        self[tuple] = ArrayHandler
        self[dict] = MapHandler
        self[int] = IntHandler
        self[float] = FloatHandler
        self[long] = BigIntHandler
        self[Keyword] = KeywordHandler
        self[Symbol] = SymbolHandler
        self[uuid.UUID] = UuidHandler
        self[URI] = UriHandler
        self[datetime.datetime] = DateTimeHandler
        self[set] = SetHandler
        self[frozenset] = SetHandler
        self[TaggedMap] = TaggedMap
        self[dict] = MapHandler
        self[frozendict] = MapHandler
        self[TaggedValue] = TaggedValueHandler
        self[Link] = LinkHandler

