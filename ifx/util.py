import re
def is_hebrew(s):
    return bool(re.search("[א-ת]", s))