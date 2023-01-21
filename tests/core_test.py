import pytest
from yamer.core import get_name

def test_get_name():
    assert get_name() == 'George Campbell'

