"""This file contains functions used to calculate the absolute path of files within certain folders
"""
import os.path

current_season = "2018"


def web_sites(file):
    path = os.path.join(os.path.dirname(__file__), 'web', 'sites', file)
    return path


def web_base():
    path = os.path.join(os.path.dirname(__file__), 'web')
    return path


def web_data(file):
    path = os.path.join(os.path.dirname(__file__), 'web', 'data', file)
    return path


def web_images(file):
    path = os.path.join(os.path.dirname(__file__), 'web', 'images', file)
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

