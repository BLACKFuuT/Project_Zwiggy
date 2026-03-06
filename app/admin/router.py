from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.database import get_db
from app.auth.dependencies import require_permission
from app.admin.service import AdminService
from app.admin.schemas import ChangeUserRole
router = APIRouter(prefix="/admin", tags=["Admin"])

service = AdminService()


@router.patch("/users/{user_id}/role")
async def change_user_role(
    user_id: UUID,
    data: ChangeUserRole,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("manage_users")),
):
    return await service.change_user_role(
        db,
        user_id,
        data.role_name
    )