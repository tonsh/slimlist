#coding=utf8

import datetime
import unittest

from slimlist.fields import OPT_STRING
from slimlist.fields import OPT_INT
from slimlist.fields import OPT_FLOAT
from slimlist.fields import OPT_BOOLEAN
from slimlist.fields import OPT_NONE
from slimlist.fields import OPT_DATE
from slimlist.fields import Field
from slimlist.fields import Fields


class FieldTest(unittest.TestCase):
    def test_none_field(self):
        field_obj = Field('demo')
        self.assertIsNone(field_obj.type)
        self.assertIsNone(field_obj.value(None))
        self.assertEqual(field_obj.value(993), 993)

    def test_string_field(self):
        field_obj = Field('demo', field_type=OPT_STRING)
        self.assertIs(field_obj.type, basestring)
        self.assertIsNone(field_obj.value(None))
        self.assertEqual(field_obj.value(993), '993')
        self.assertEqual(field_obj.value(u'demo string'), u'demo string')
        self.assertEqual(field_obj.value('demo string'), 'demo string')

    def test_string_field_with_default(self):
        field_obj = Field('demo', field_type=OPT_STRING, default='demo string')
        self.assertEqual(field_obj.value(None), 'demo string')

    def test_date_field(self):
        field_obj = Field('demo', field_type=OPT_DATE)
        self.assertIs(field_obj.type, datetime.datetime)
        self.assertIsNone(field_obj.value(None))
        date_time = datetime.datetime(2013, 5, 3)
        self.assertEqual(field_obj.value('2013-05-03'), date_time)

    def test_date_field_with_default(self):
        date_time = datetime.datetime(2013, 5, 3)
        field_obj = Field('demo', field_type=OPT_DATE, default=date_time)
        self.assertEqual(field_obj.value(None), date_time)

    def test_int_field(self):
        field_obj = Field('demo', field_type=OPT_INT)
        self.assertIs(field_obj.type, int)
        self.assertIsNone(field_obj.value(None))
        self.assertEqual(field_obj.value(993), 993)
        self.assertEqual(field_obj.value('993'), 993)
        self.assertEqual(field_obj.value(993.88), 993)
        self.assertEqual(field_obj.value('-993'), -993)

    def test_int_field_with_default(self):
        field_obj = Field('demo', field_type=OPT_INT, default=993)
        self.assertEqual(field_obj.value(None), 993)

    def test_float_field(self):
        field_obj = Field('demo', field_type=OPT_FLOAT)
        self.assertIs(field_obj.type, float)
        self.assertIsNone(field_obj.value(None))
        self.assertEqual(field_obj.value(993), 993)
        self.assertEqual(field_obj.value('993.88'), 993.88)
        self.assertEqual(field_obj.value(993.88), 993.88)

    def test_float_field_with_default(self):
        field_obj = Field('demo', field_type=OPT_FLOAT, default=993.88)
        self.assertEqual(field_obj.value(None), 993.88)

    def test_bool_field(self):
        field_obj = Field('demo', field_type=OPT_BOOLEAN)
        self.assertIs(field_obj.type, bool)
        self.assertFalse(field_obj.value(None))
        self.assertFalse(field_obj.value('false'))
        self.assertFalse(field_obj.value(''))
        self.assertFalse(field_obj.value(False))
        self.assertFalse(field_obj.value(0))
        self.assertFalse(field_obj.value('0'))

        self.assertTrue(field_obj.value(True))
        self.assertTrue(field_obj.value(1))
        self.assertTrue(field_obj.value('aaa'))


class FieldsTest(unittest.TestCase):
    def setUp(self):
        from slimlist.test.fields_tpl import tpl
        self.field_obj = Fields(tpl)

    def test_definer_tuple(self):
        self.assertEqual(len(self.field_obj._fields), 6)
        self.assertEqual(self.field_obj._order, [
            'field_1', 'field_2', 'field_3', 'field_5', 'field_4', 'field_6',
        ])
        self.assertEqual(self.field_obj.titles(), [
            'first field', 'second field', 'third field', 'fourth field',
            'fifth field', 'sixth field',
        ])

    def test_insert(self):
        self.field_obj.insert('field_7')
        self.assertEqual(len(self.field_obj._fields), 7)
        self.assertEqual(self.field_obj._order[-1], 'field_7')

        self.field_obj.insert('field_8', index=3)
        self.assertEqual(len(self.field_obj._fields), 8)
        self.assertEqual(self.field_obj._order[3], 'field_8')

    def test_remove(self):
        self.assertEqual(self.field_obj._order[1], 'field_2')
        self.field_obj.remove('field_2')
        self.assertEqual(len(self.field_obj._fields), 5)
        self.assertEqual(self.field_obj._order[1], 'field_3')

    def test_tolist(self):
        data = {}
        values = self.field_obj.to_list(data)
        self.assertEqual(values, ['demo',
                                  datetime.datetime(2013, 5, 3, 15, 22, 46),
                                  False, 0.00, 0, None])

        data = {
            'field_1': 'tonsh', 'field_2': '2010-09-01', 'field_3': 'y',
            'field_4': '73', 'field_5': '130.6', 'field_6': 'anything',
            'field_7': 'others',
        }
        values = self.field_obj.to_list(data)
        self.assertEqual(values, [
                                    'tonsh', datetime.datetime(2010, 9, 1),
                                    True, 130.6, 73, 'anything',
                                ])
        results = []
        self.field_obj.to_list(data, callback=results.append)
        self.assertEqual(results, [
                                    [ 'tonsh', datetime.datetime(2010, 9, 1),
                                    True, 130.6, 73, 'anything',]
                                ])