from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from .models import User, Profile
from .repository import UserRepository
from .schemas import UserCreate
from app.rbac.repository import RBACRepository


class UserService:

    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)
        self.db = db

    async def create_user(self, data: UserCreate) -> User:

        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
        )

        profile = Profile(
            address=data.address,
            phone=data.phone,
        )

        user.profile = profile

        user = await self.repo.create_user(user)

        # load profile explicitly
        await self.db.refresh(user, attribute_names=["profile"])
        
        # Default role assignment 
        rbac_repo = RBACRepository(self.db)
        role = await rbac_repo.get_role_by_name("Customer")

        if not role:
            raise HTTPException(500, "Default role not configured")

        await rbac_repo.assign_role(user.id, role.id)

        await self.db.commit()
        return user

    async def get_user(self, user_id):
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )
        return user