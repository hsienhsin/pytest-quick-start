from typing import List

import pytest

import lib
import pytest_mock
# noinspection PyUnresolvedReferences
from test_fixtures import guitar_data


# 需要使用到外部的 resource, get_guitars_from_db()
def test_electric_guitars_wrong():
    style = 'electric'
    guitars = lib.all_guitars(style)
    # sweet little generator expression
    assert all(g.style == style for g in guitars)


def test_electric_guitars(guitar_data: List[lib.Guitar], mocker: pytest_mock.MockFixture):
    # uncomment the following 2 line to mock the external dependency
    mocker.patch('lib.get_guitars_from_db', autospec=True, return_value=guitar_data)
    mock_log = mocker.patch('lib.log', autospec=True)

    style = 'electric'
    guitars = lib.all_guitars(style)
    # sweet little generator expression
    assert all(g.style == style for g in guitars)
    # uncomment the following line to test the external dependency behave as design
    mock_log.assert_called_once_with(f"Guitars for {style}")


def test_all_guitars(guitar_data: List[lib.Guitar], mocker: pytest_mock.MockFixture):
    # mocker.patch('lib.get_guitars_from_db', autospec=True, return_value=guitar_data)
    # mocker.patch('lib.log', autospec=True)

    style = 'all'
    guitars = lib.all_guitars(style)
    # sweet little generator expression
    types = {g.style for g in guitars}

    assert types == {'acoustic', 'electric'}


def test_invalid_style():
    with pytest.raises(ValueError):
        lib.all_guitars(None)
