#coding=utf8


import unittest

from slimunicode.unicode import SlimUnicode
from slimunicode.unicode import CNString


class TestSlimUnicode(unittest.TestCase):

    def test_unicode(self):
        # unicode with None
        self.assertIsNone(SlimUnicode.unicode(None))

        # unicode with string
        self.assertEqual(SlimUnicode.unicode("您好2013"), u"您好2013")

        # unicode with unicode
        self.assertEqual(SlimUnicode.unicode(u"您好2013"), u"您好2013")

        # unicode with non-byte string
        self.assertRaises(AttributeError, SlimUnicode.unicode, [u"您好2013"])

    def test_is_number(self):
        # unicode string number is number
        for num in range(0, 9):
            self.assertTrue(SlimUnicode.is_number(unicode(num)))

        self.assertFalse(SlimUnicode.is_number(unicode('a')))

    def test_is_alphabet(self):
        # unicode alphabet
        letters = "abcdefghigklmnopqrstuvwxyzABCDEFGHIGKLMNOPQRSTUVWXYZ"
        for letter in letters:
            self.assertTrue(SlimUnicode.is_alphabet(unicode(letter)))

        self.assertFalse(SlimUnicode.is_alphabet(unicode(0)))

    def test_is_chinese(self):
        self.assertTrue(SlimUnicode.is_chinese(u'您'))
        self.assertFalse(SlimUnicode.is_chinese(u"a"))

    def test_is_other(self):
        self.assertTrue(SlimUnicode.is_other(u'@'))
        self.assertTrue(SlimUnicode.is_other(u'％'))
        self.assertFalse(SlimUnicode.is_other(u'您'))


class TestCNString(unittest.TestCase):

    def test_init(self):
        # value attribute should be unicode
        obj = CNString("您好2013")
        self.assertIsInstance(obj.value, unicode)

        obj = CNString(u'您好2013')
        self.assertIsInstance(obj.value, unicode)
        self.assertEqual(obj.charset, 'utf-8')

        # charset
        obj = CNString(u'aaa', charset='UTF-8')
        self.assertEqual(obj.charset, 'utf-8')

        obj = CNString(u'aaa', charset='GBK')
        self.assertEqual(obj.charset, 'gbk')

    def test_to_string(self):
        obj = CNString(u'您好2013')
        self.assertEqual(obj.to_string(), "您好2013")

        obj = CNString("您好2013")
        self.assertEqual(obj.to_string(), "您好2013")

        obj = CNString(None)
        self.assertIsNone(obj.to_string())

    def test_length(self):
        string = "您好2013"
        obj = CNString(string)
        self.assertEqual(obj.length(), 6)

        self.assertEqual(obj.test_byte_length(), len(string))

