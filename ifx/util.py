import re


def is_hebrew(s):
    return bool(re.search("[א-ת]", s))


def is_english(s):
    return bool(re.search("[a-zA-Z]", s))
