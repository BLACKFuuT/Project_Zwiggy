import pytest
from unittest.mock import AsyncMock

from fastapi import HTTPException

from app.payments.service import PaymentService
from app.payments.models import Payment
from app.users.models import User


@pytest.fixture
def service():
    service = PaymentService()
    service.repository = AsyncMock()
    service.order_repo = AsyncMock()
    return service


@pytest.fixture
def db():
    return AsyncMock()


@pytest.fixture
def user():
    return User(id=1, email="test@test.com")


# -----------------------------
# initiate_payment tests
# -----------------------------

@pytest.mark.asyncio
async def test_initiate_payment_order_not_found(service, db, user):

    service.order_repo.get_order_by_id.return_value = None

    with pytest.raises(HTTPException) as exc:

        await service.initiate_payment(
            db=db,
            order_id=1,
            current_user=user
        )

    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_initiate_payment_user_not_owner(service, db, user):

    order = AsyncMock()
    order.id = 1
    order.customer_id = 2
    order.total_amount = 100

    service.order_repo.get_order_by_id.return_value = order

    with pytest.raises(HTTPException) as exc:

        await service.initiate_payment(
            db=db,
            order_id=1,
            current_user=user
        )

    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_initiate_payment_duplicate(service, db, user):

    order = AsyncMock()
    order.id = 1
    order.customer_id = 1
    order.total_amount = 100

    service.order_repo.get_order_by_id.return_value = order
    service.repository.get_by_order_id.return_value = Payment()

    with pytest.raises(HTTPException) as exc:

        await service.initiate_payment(
            db=db,
            order_id=1,
            current_user=user
        )

    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_initiate_payment_success(service, db, user):

    order = AsyncMock()
    order.id = 1
    order.customer_id = 1
    order.total_amount = 100

    service.order_repo.get_order_by_id.return_value = order
    service.repository.get_by_order_id.return_value = None
    service.repository.create.return_value = None

    db.commit = AsyncMock()
    db.refresh = AsyncMock()

    result = await service.initiate_payment(
        db=db,
        order_id=1,
        current_user=user
    )

    assert result.order_id == 1
    assert result.amount == 100
    assert result.status == "INITIATED"


# -----------------------------
# confirm_payment tests
# -----------------------------

@pytest.mark.asyncio
async def test_confirm_payment_not_found(service, db, user):

    service.repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc:

        await service.confirm_payment(
            db=db,
            payment_id=1,
            current_user=user
        )

    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_confirm_payment_success(service, db, user):

    payment = AsyncMock()
    payment.id = 1
    payment.order_id = 10

    service.repository.get_by_id.return_value = payment
    service.repository.update_status.return_value = None
    service.order_repo.update_status.return_value = None

    db.commit = AsyncMock()

    service.repository.get_by_id.return_value = payment

    result = await service.confirm_payment(
        db=db,
        payment_id=1,
        current_user=user
    )

    assert result == payment