from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Role, UserRole, RolePermission, Permission


class RBACRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_role_by_name(self, name: str):
        stmt = select(Role).where(Role.name == name)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def assign_role(self, user_id, role_id):
        user_role = UserRole(user_id=user_id, role_id=role_id)
        self.db.add(user_role)
        await self.db.flush()
        
    async def get_permissions_by_user_id(self, user_id):
        stmt = (
            select(Permission.name)
            .join(RolePermission, Permission.id == RolePermission.permission_id)
            .join(UserRole, UserRole.role_id == RolePermission.role_id)
            .where(UserRole.user_id == user_id)
        )

        result = await self.db.execute(stmt)
        return set(result.scalars().all())