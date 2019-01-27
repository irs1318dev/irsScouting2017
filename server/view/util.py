import json
import re


def jsonify(input_str):
    input_str = re.sub(r'{end}$', '', input_str)
    return '[' + re.sub(r'}\s*{', r'}, {', input_str) + ']'
