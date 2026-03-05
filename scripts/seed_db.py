import asyncio

from app.core.database import AsyncSessionLocal
from app.core.seed import seed_roles_permissions

# IMPORTANT: import models so SQLAlchemy registers them
from app.users import models as user_models
from app.rbac import models as rbac_models


async def main():
    async with AsyncSessionLocal() as db:
        await seed_roles_permissions(db)


if __name__ == "__main__":
    asyncio.run(main())