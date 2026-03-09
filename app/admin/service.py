from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from uuid import UUID

from app.users.models import User
from app.rbac.models import Role, UserRole


class AdminService:

    async def change_user_role(
        self,
        db: AsyncSession,
        user_id: UUID,
        role_name: str
    ):
        #  check if user exists
        user_result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = user_result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # get role by name
        role_result = await db.execute(
            select(Role).where(Role.name == role_name)
        )
        role = role_result.scalar_one_or_none()

        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )

        # remove existing roles
        existing_roles = await db.execute(
            select(UserRole).where(UserRole.user_id == user_id)
        )

        for ur in existing_roles.scalars().all():
            await db.delete(ur)

        #  assign new role
        user_role = UserRole(
            user_id=user_id,
            role_id=role.id
        )

        db.add(user_role)

        await db.commit()

        return {
            "message": f"User role updated to {role_name}"
        }