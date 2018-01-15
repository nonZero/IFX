import re
def is_hebrew(s):
    return re.search("[א-ת]", s)