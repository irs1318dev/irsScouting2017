import json
import os
import re
import subprocess

import server.config


def jsonify(input_str):
    input_str = re.sub(r'{end}$', '', input_str)
    return '[' + re.sub(r'}\s*{', r'}, {', input_str) + ']'


def to_points(column, points):
    return column * points


def upload_data():
    os.chdir(server.config.output_path(2019))
    subprocess.run('git status', shell=True)
    subprocess.run('git add --all', shell=True)
    subprocess.run('git commit -m "Updating Data"', shell=True)
    subprocess.run('git push origin master', shell=True)