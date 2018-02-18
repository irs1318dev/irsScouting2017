"""Tests every method in server.config.py
"""
import os.path
import re

import server.config


def _check_path(pattern, path):
    assert re.search(pattern, path)
    assert os.path.isabs(path)


def test_web_sites():
    _check_path(r"server\\web\\sites\\admin.html$",
                server.config.web_sites("admin.html"))


def test_web_scripts():
    _check_path(r"server\\web\\scripts\\selectteam.js",
                server.config.web_scripts("selectteam.js"))


def test_web_data():
    _check_path(r"server\\web\\data\\alliances.csv",
                server.config.web_data("alliances.csv"))


def test_web_images():
    _check_path(r"server\\web\\images\\Climbing.png",
                server.config.web_images("Climbing.png"))


def test_scouting():
    _check_path(r"server\\scouting\\alliance.py",
                server.config.scouting("alliance.py"))


def test_testjson():
    _check_path(r"server\\TestJson\\pnw_events.json",
                server.config.TestJson("pnw_events.json"))


def test_season():
    _check_path(r"server\\season\\s2018\\gametasks.csv",
                server.config.season("2018", "gametasks.csv"))

    _check_path(r"server\\season\\s2017\\gametasks.csv",
                server.config.season("2017", "gametasks.csv"))


def test_tests_model_test_data():
    _check_path(r"server\\tests\\model\\test_data\\sched.json",
                server.config.tests_model_test_data("sched.json"))

