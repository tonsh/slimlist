#coding=utf8

from slimlist.fields import OPT_STRING
from slimlist.fields import OPT_INT
from slimlist.fields import OPT_FLOAT
from slimlist.fields import OPT_BOOLEAN
from slimlist.fields import OPT_NONE
from slimlist.fields import OPT_DATE

tpl = (
    ('field_1', {'field_type': OPT_STRING, 'default': 'demo', 'title': 'first field'}),
    ('field_2', {'field_type': OPT_DATE, 'default': '2013-05-03 15:22:46', 'title': 'second field'}),
    ('field_3', {'field_type': OPT_BOOLEAN, 'title': 'third field'}),
    ('field_5', {'field_type': OPT_FLOAT, 'default': 0.00, 'title': 'fourth field'}),
    ('field_4', {'field_type': OPT_INT, 'default': 0, 'title': 'fifth field'}),
    ('field_6', {'field_type': OPT_NONE, 'title': 'sixth field'}),
)