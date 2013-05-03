#coding=utf8

""" Translate tuple type data to a values list
    将 tuple 数据按定义的类型默认值等转换为列表数据
"""


import datetime


OPT_STRING = basestring
OPT_INT = int
OPT_FLOAT = float
OPT_BOOLEAN = bool
OPT_NONE = None
OPT_DATE = datetime.datetime


class Fields(object):

    def __init__(self, definer_tuple):
        self._order = []
        self._fields = {}

        self.define(definer_tuple)

    def define(self, definer_tuple):
        for name, items in definer_tuple:
            self._order.append(name)
            self._fields[name] = Field(name, **dict(items))

    def insert(self, name, items=None, index=-1):
        if index == -1:
            self._order.append(name)
        else:
            self._order.insert(index, name)

        if not items:
            items = {}
        self._fields[name] = Field(name, **dict(items))

    def remove(self, name):
        if name in self._order:
            self._order.remove(name)
            del self._fields[name]

    def titles(self):
        titles = []
        for name in self._order:
            titles.append(self._fields[name].title)

        return titles

    def to_list(self, data=None, callback=None):
        values = []
        if not isinstance(data, dict):
            return values

        for name in self._order:
            option_obj = self._fields[name]
            value = data.get(option_obj.name)
            values.append(option_obj.value(value))

        if callback is not None:
            callback(values)

        return values


class Field(object):

    def __init__(self, name, field_type=None, default=None,
                 title=None, field_help=None):

        self.name = name
        self.default = default
        self.type = field_type
        self.title = title
        self.help = field_help

    def value(self, value):
        _parse = {
            OPT_STRING: self._parse_string,
            OPT_INT: self._parse_int,
            OPT_FLOAT: self._parse_float,
            OPT_BOOLEAN: self._parse_boolean,
            OPT_DATE: self._parse_date,
            OPT_NONE: self._parse_none,
        }.get(self.type, self.type)

        value = _parse(value)
        return self.default if value is None else value

    def _parse_none(self, value):
        return value

    def _parse_string(self, value):
        if isinstance(value, (unicode, type(None))):
            return value
        elif isinstance(value, bytes):
            return value.encode('utf-8')

        try:
            return str(value)
        except ValueError:
            return None

    def _parse_int(self, value):
        if value is None:
            return None

        try:
            return int(value)
        except ValueError:
            return None

    def _parse_float(self, value):
        if value is None:
            return None

        try:
            return float(value)
        except ValueError:
            return None

    def _parse_boolean(self, value):
        if not value or (value in ('false', 'f', '0')):
            return False
        return True

    _DATETIME_FORMATS = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%Y%m%d",
        "%Y%m%d%H%M%S",
        "%Y%m%d %H%M%S",
        "%Y%m%d %H%M",
        "%H%M%S",
    ]
    def _parse_date(self, value):
        if value is None:
            return None

        if isinstance(value, datetime.datetime):
            return value

        for fmt in self._DATETIME_FORMATS:
            try:
                return datetime.datetime.strptime(value, fmt)
            except ValueError:
                continue
        return None