import os
import pytest


@pytest.fixture
def data_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
