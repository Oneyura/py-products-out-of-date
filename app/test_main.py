from unittest import mock
import datetime
import copy

import pytest

from app.main import outdated_products

@pytest.fixture()
def set_products():
    yield copy.deepcopy([
    {
        "name": "salmon",
        "expiration_date": datetime.date(2022, 2, 10),
        "price": 600
    },
    {
        "name": "chicken",
        "expiration_date": datetime.date(2022, 2, 5),
        "price": 120
    },
    {
        "name": "duck",
        "expiration_date": datetime.date(2022, 2, 1),
        "price": 160
    }
    ])

@pytest.mark.parametrize(
    "salmon_date, chicken_date, duck_date, today, result",
    [
        (
            datetime.date(2022, 2, 10),
            datetime.date(2022, 2, 10),
            datetime.date(2022, 2, 10),
            datetime.date(2022, 2, 11),
            ["salmon", "chicken", "duck"]
        ),
        (
            datetime.date(2023, 2, 10),
            datetime.date(2025, 2, 10),
            datetime.date(2035, 2, 10),
            datetime.date(2022, 2, 10),
            []
        ),
        (
            datetime.date(2022, 2, 10),
            datetime.date(2022, 2, 10),
            datetime.date(2022, 2, 10),
            datetime.date(2022, 2, 10),
            []
        ),
        (
            datetime.date(2022, 2, 10),
            datetime.date(1999, 2, 10),
            datetime.date(2000, 2, 9),
            datetime.date(2000, 2, 10),
            ["chicken", "duck"]
        ),
    ],
    ids=[
        "all products are out of date",
        "all products are on date",
        "all products are out of date tomorrow",
        "chicken and duck are out of date",
    ]
)
def test_general(
        set_products,
        salmon_date,
        chicken_date,
        duck_date,
        today,
        result
) -> None:
    set_products[0]["expiration_date"] = salmon_date
    set_products[1]["expiration_date"] = chicken_date
    set_products[2]["expiration_date"] = duck_date
    with mock.patch("datetime.date") as mock_date:
        mock_date.today.return_value = today
        assert outdated_products(set_products) == result
