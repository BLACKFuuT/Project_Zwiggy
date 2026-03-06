from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from app.core.security import hash_password


from app.rbac.models import (
    Role,
    Permission,
    RolePermission,
    UserRole
    
)

from app.users.models import User
from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -------------------------
# DEFAULT ROLES
# -------------------------

DEFAULT_ROLES = [
    "Admin",
    "Customer",
    "Restaurant_owner",
    "Delivery_partner",
]


# -------------------------
# DEFAULT PERMISSIONS
# -------------------------

DEFAULT_PERMISSIONS = [

    # RESTAURANTS
    "create_restaurant",
    "update_restaurant",
    "delete_restaurant",
    "view_restaurant",

    # MENU ITEMS
    "create_menu_item",
    "update_menu_item",
    "delete_menu_item",
    "view_menu_item",

    # ORDERS
    "create_order",
    "view_order",
    "update_order",
    "cancel_order",

    # PAYMENTS
    "create_payment",   
    "confirm_payment",
    "view_payment",

    # DELIVERY
    "update_delivery_status",
    "view_delivery",

    # ADMIN
    "manage_users",
]


# -------------------------
# ROLE PERMISSION MAPPING
# -------------------------

ROLE_PERMISSION_MAPPING = {

    "Admin": DEFAULT_PERMISSIONS,

    "Restaurant_owner": [
        "create_restaurant",
        "update_restaurant",
        "delete_restaurant",
        "view_restaurant",

        "create_menu_item",
        "update_menu_item",
        "delete_menu_item",
        "view_menu_item",

        "view_order",
        "update_order",
    ],

    "Delivery_partner": [
        "view_order",
        "update_delivery_status",
        "view_delivery",
    ],

    "Customer": [
        "create_order",
        "view_order",
        "cancel_order",

        "view_restaurant",
        "view_menu_item",

        "create_payment",
        "view_payment",
    ],
}


async def seed_roles_permissions(db: AsyncSession):
    """
    Seed roles, permissions, role-permission mapping
    and create default admin user.
    Safe to run multiple times.
    """

    # -------------------------
    # Seed Roles
    # -------------------------

    for role_name in DEFAULT_ROLES:
        from sqlalchemy import select
        result = await db.execute(
            select(Role).where(Role.name == role_name)
        )

        role = result.scalar_one_or_none()

        if not role:
            db.add(Role(name=role_name))

    await db.commit()


    # -------------------------
    # Seed Permissions
    # -------------------------

    for perm_name in DEFAULT_PERMISSIONS:

        result = await db.execute(
            select(Permission).where(Permission.name == perm_name)
        )

        permission = result.scalar_one_or_none()

        if not permission:
            db.add(Permission(name=perm_name))

    await db.commit()


    # -------------------------
    # Seed Role-Permission Mapping
    # -------------------------

    for role_name, permissions in ROLE_PERMISSION_MAPPING.items():

        role_result = await db.execute(
            select(Role).where(Role.name == role_name)
        )

        role = role_result.scalar_one()

        for perm_name in permissions:

            perm_result = await db.execute(
                select(Permission).where(Permission.name == perm_name)
            )

            permission = perm_result.scalar_one()

            rp_result = await db.execute(
                select(RolePermission).where(
                    RolePermission.role_id == role.id,
                    RolePermission.permission_id == permission.id,
                )
            )

            mapping = rp_result.scalar_one_or_none()

            if not mapping:
                db.add(
                    RolePermission(
                        role_id=role.id,
                        permission_id=permission.id,
                    )
                )

    await db.commit()

    # -------------------------
    # CREATE DEFAULT ADMIN
    # -------------------------

    from sqlalchemy import select

    result = await db.execute(
        select(User).where(User.email == settings.ADMIN_EMAIL)
    )

    admin = result.scalar_one_or_none()

    if not admin:

        # create user
        admin = User(
            email=settings.ADMIN_EMAIL,
            hashed_password=hash_password(settings.ADMIN_PASSWORD),
            is_active=True,
            is_verified=True
        )

        db.add(admin)
        await db.flush()

        # get admin role
        role_result = await db.execute(
            select(Role).where(Role.name == "Admin")
        )

        admin_role = role_result.scalar_one()

        # assign role
        user_role = UserRole(
            user_id=admin.id,
            role_id=admin_role.id
        )

        db.add(user_role)

        await db.commit()

        print("Admin user created")