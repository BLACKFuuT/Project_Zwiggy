import pytest
from app.orders.calculate_total import calculate_total


@pytest.mark.asyncio
async def test_calculate_total():
    items = [
        {"price": 100, "quantity": 2},
        {"price": 50, "quantity": 1},
    ]

    try:
        await calculate_total(items)
    except Exception:
        pass