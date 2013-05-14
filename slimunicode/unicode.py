#coding=utf8


class SlimUnicode(object):
    #def __init__(self, value):
    #    self.value = self._unicode(value)

    @classmethod
    def unicode(cls, value):
        """
        Convert a string to a unicode string
        :return: A unicode string
        """
        unicode_types = (unicode, type(None))
        if isinstance(value, unicode_types):
            return value

        assert(value, bytes)
        return value.decode("utf-8", "ignore")

    @classmethod
    def is_number(cls, uchar):
        """
        Check a unicode string is a number character
        :param uchar:
        :return:
        """
        if uchar >= u'\u0030' and uchar <= u'\u0039':
            return True
        return False

    @classmethod
    def is_alphabet(cls, uchar):
        is_lower_case = (uchar >= u'\u0041') and (uchar <= u'\u005a')
        is_upper_case = (uchar >= u'\u0061') and (uchar <= u'\u007a')
        if is_lower_case or is_upper_case:
            return True
        return False

    @classmethod
    def is_chinese(cls, uchar):
        """
        Check a unicode string is a chinese character
        :param uchar:
        :return:
        """
        if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
            return True

        return False

    @classmethod
    def is_other(cls, uchar):
        if not (cls.is_chinese(uchar) or cls.is_number(uchar) or
                                        cls.is_alphabet(uchar)):
            return True
        return False


_CHINESE_LENGTH_MAP = {
    "utf-8": 3,
    "gbk": 2,
}


class CNString(object):
    """ String property with chinese characters """

    def __init__(self, value, charset="utf-8"):
        self.value = SlimUnicode.unicode(value)
        self.charset = charset.lower()

    def to_string(self):
        """
        Convert a unicode string to a byte string.
        :return: a byte string.
        """
        if self.value is None:
            return None

        return self.value.encode(self.charset, "ignore")

    def length(self):
        """
        The length of the unicode value
        :return:
        """
        length = 0
        for uchar in self.value:
            length += 1

        return length

    def test_byte_length(self):
        """
        used by unittest
        :return:
        """
        length = 0
        for uchar in self.value:
            if SlimUnicode.is_chinese(uchar):
                length += _CHINESE_LENGTH_MAP.get(self.charset, 1)
            else:
                length += 1

        return length

    def slice(self, index, step=None):
        """
        Slice the unicode string
        :param index: start index
        :param step:
        :return: a slice string
        """
        _index = 0
        result = []
        for uchar in self.value:
            if (_index >= index) and ((step is None) or (step > _index)):
                result.append(uchar)
            _index += 1

        return "".join(result).encode(self.charset, "ignore")
