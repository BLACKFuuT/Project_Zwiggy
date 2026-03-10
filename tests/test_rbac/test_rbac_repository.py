import pytest
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.rbac.repository import RBACRepository
from app.rbac.models import Role, UserRole, Permission, RolePermission


@pytest.mark.asyncio
async def test_get_role_by_name_found(db: AsyncSession):
    role = Role(name="admin")
    db.add(role)
    await db.commit()

    repo = RBACRepository(db)

    result = await repo.get_role_by_name("admin")

    assert result is not None
    assert result.name == "admin"


@pytest.mark.asyncio
async def test_get_role_by_name_not_found(db: AsyncSession):
    repo = RBACRepository(db)

    result = await repo.get_role_by_name("manager")

    assert result is None


@pytest.mark.asyncio
async def test_assign_role(db: AsyncSession):
    role = Role(name="user")
    db.add(role)
    await db.commit()

    repo = RBACRepository(db)

    user_id = uuid.uuid4()

    await repo.assign_role(user_id=user_id, role_id=role.id)
    await db.commit()

    result = await db.execute(
        select(UserRole).where(UserRole.user_id == user_id)
    )
    user_role = result.scalar_one_or_none()

    assert user_role is not None
    assert user_role.role_id == role.id


@pytest.mark.asyncio
async def test_get_permissions_by_user_id(db: AsyncSession):

    role = Role(name="admin")
    permission1 = Permission(name="create_order")
    permission2 = Permission(name="delete_order")

    db.add_all([role, permission1, permission2])
    await db.flush()

    role_perm1 = RolePermission(role_id=role.id, permission_id=permission1.id)
    role_perm2 = RolePermission(role_id=role.id, permission_id=permission2.id)

    user_id = uuid.uuid4()
    user_role = UserRole(user_id=user_id, role_id=role.id)
    
    db.add_all([role_perm1, role_perm2, user_role])
    await db.commit()

    repo = RBACRepository(db)

    permissions = await repo.get_permissions_by_user_id(user_id)
    
    assert permissions == {"create_order", "delete_order"}