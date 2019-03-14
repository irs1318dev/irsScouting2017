"""This file contains functions used to calculate the absolute path of
files within certain folders
"""
import os.path

current_season = "2019"

# Database Parameters
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "scouting"
DB_MINCONN = 1
DB_MAXCONN = 5


# File Locations
def web_sites(file):
    path = os.path.join(os.path.dirname(__file__), 'web', 'sites', file)
    return path


def web_base():
    path = os.path.join(os.path.dirname(__file__), 'web')
    return path


def web_data(file):
    path = os.path.join(os.path.dirname(__file__), 'web', 'data', file)
    return path


def web_firstapi(file):
    return os.path.join(os.path.dirname(__file__), 'web', 'firstapi', file)


def web_images(file):
    path = os.path.join(os.path.dirname(__file__), 'web', 'images', file)
    return path


def web_scripts(file):
    path = os.path.join(os.path.dirname(__file__), 'web', 'scripts', file)
    return path


def scouting(file):
    path = os.path.join(os.path.dirname(__file__), 'scouting', file)
    return path


def TestJson(file):
    path = os.path.join(os.path.dirname(__file__), 'TestJson', file)
    return path


def season(year, file):
    path = os.path.join(os.path.dirname(__file__), 'season', 's' + year, file)
    return path


def tests_model_test_data(file):
    path = os.path.join(os.path.dirname(__file__), 'tests', 'model', 'test_data', file)
    return path


def output_path(season):
    season_str = str(season)
    return os.path.abspath(os.path.join(
        os.path.dirname(__file__), r"..\..\scouting" + season_str))
