import os

import server.config
import server.view.util as svu


def test_path():
    print(server.config.output_path(2019))


def test_output():
    svu.upload_data()