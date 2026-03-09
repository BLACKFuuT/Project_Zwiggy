import pytest
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from app.restaurants.models import Restaurant


@pytest.mark.asyncio
async def test_create_restaurant(db: AsyncSession):

    restaurant = Restaurant(
        name="Pizza Hut",
        description="Best pizza in town",
        address="Delhi",
        owner_id=uuid4()
    )

    db.add(restaurant)
    await db.commit()
    await db.refresh(restaurant)

    assert restaurant.id is not None
    assert restaurant.name == "Pizza Hut"
    assert restaurant.address == "Delhi"
    assert restaurant.is_active is True
    assert restaurant.created_at is not None
    
    
    
@pytest.mark.asyncio
async def test_soft_delete_restaurant(db: AsyncSession):

    restaurant = Restaurant(
        name="Dominos",
        address="Mumbai",
        owner_id=uuid4()
    )

    db.add(restaurant)
    await db.commit()
    await db.refresh(restaurant)

    restaurant.deleted_at = restaurant.created_at
    await db.commit()

    assert restaurant.deleted_at is not None
    


# @pytest.mark.asyncio
# async def test_restaurant_relationships(db: AsyncSession):

#     restaurant = Restaurant(
#         name="Burger King",
#         address="Delhi",
#         owner_id=uuid4()
#     )

#     db.add(restaurant)
#     await db.commit()
#     await db.refresh(restaurant)

#     assert restaurant.menu_items == []