import pytest
from unittest.mock import AsyncMock, MagicMock

from app.payments.repository import PaymentRepository
from app.payments.models import Payment


@pytest.fixture
def repo():
    return PaymentRepository()


@pytest.fixture
def db():
    return AsyncMock()


@pytest.fixture
def payment():
    return Payment(
        id=1,
        order_id=10,
        amount=100,
        status="INITIATED"
    )


# -------------------------
# create
# -------------------------

@pytest.mark.asyncio
async def test_create_payment(repo, db, payment):

    db.add = MagicMock()
    db.flush = AsyncMock()

    result = await repo.create(db, payment)

    db.add.assert_called_once_with(payment)
    db.flush.assert_awaited_once()

    assert result == payment


# -------------------------
# get_by_id (found)
# -------------------------

@pytest.mark.asyncio
async def test_get_by_id_found(repo, db, payment):

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = payment

    db.execute = AsyncMock(return_value=mock_result)

    result = await repo.get_by_id(db, 1)

    assert result == payment
    db.execute.assert_awaited_once()


# -------------------------
# get_by_id (not found)
# -------------------------

@pytest.mark.asyncio
async def test_get_by_id_not_found(repo, db):

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None

    db.execute = AsyncMock(return_value=mock_result)

    result = await repo.get_by_id(db, 1)

    assert result is None


# -------------------------
# update_status
# -------------------------

@pytest.mark.asyncio
async def test_update_status(repo, db):

    db.execute = AsyncMock()

    await repo.update_status(
        db,
        payment_id=1,
        status="SUCCESS",
        transaction_id="txn_123"
    )

    db.execute.assert_awaited_once()


# -------------------------
# get_by_order_id (found)
# -------------------------

@pytest.mark.asyncio
async def test_get_by_order_id_found(repo, db, payment):

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = payment

    db.execute = AsyncMock(return_value=mock_result)

    result = await repo.get_by_order_id(db, order_id=10)

    assert result == payment


# -------------------------
# get_by_order_id (not found)
# -------------------------

@pytest.mark.asyncio
async def test_get_by_order_id_not_found(repo, db):

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None

    db.execute = AsyncMock(return_value=mock_result)

    result = await repo.get_by_order_id(db, order_id=10)

    assert result is None