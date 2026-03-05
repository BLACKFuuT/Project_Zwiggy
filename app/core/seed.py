from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.rbac.models import Role


DEFAULT_ROLES = [
    "Admin",
    "Customer",
    "Restaurant_owner",
    "Delivery_partner",
]


# DEFAULT_PERMISSIONS = [
#     "create_restaurant",
#     "update_restaurant",
#     "delete_restaurant",
#     "view_restaurant",

#     "create_order",
#     "update_order",
#     "cancel_order",
#     "view_order",

#     "manage_users",
# ]


# ROLE_PERMISSION_MAPPING = {
#     "admin": [
#         "create_restaurant",
#         "update_restaurant",
#         "delete_restaurant",
#         "view_restaurant",
#         "create_order",
#         "update_order",
#         "cancel_order",
#         "view_order",
#         "manage_users",
#     ],

#     "restaurant_owner": [
#         "create_restaurant",
#         "update_restaurant",
#         "delete_restaurant",
#         "view_restaurant",
#         "view_order",
#         "update_order",
#     ],

#     "delivery_partner": [
#         "view_order",
#         "update_order",
#     ],

#     "customer": [
#         "create_order",
#         "cancel_order",
#         "view_order",
#     ],
# }


async def seed_roles_permissions(db: AsyncSession):
    """
    Seed default roles and permissions.
    Safe to run multiple times.
    """

    # --------
    # Seed Roles
    # --------
    for role_name in DEFAULT_ROLES:
        result = await db.execute(
            select(Role).where(Role.name == role_name)
        )
        role = result.scalar_one_or_none()

        if not role:
            db.add(Role(name=role_name))

    await db.commit()

    # --------
    # Seed Permissions
    # --------
    # for perm_name in DEFAULT_PERMISSIONS:
    #     result = await db.execute(
    #         select(Permission).where(Permission.name == perm_name)
    #     )
    #     permission = result.scalar_one_or_none()

    #     if not permission:
    #         db.add(Permission(name=perm_name))

    # await db.commit()

    # # --------
    # # Seed Role-Permission Mapping
    # # --------
    # for role_name, permissions in ROLE_PERMISSION_MAPPING.items():

    #     role_result = await db.execute(
    #         select(Role).where(Role.name == role_name)
    #     )
    #     role = role_result.scalar_one()

    #     for perm_name in permissions:

    #         perm_result = await db.execute(
    #             select(Permission).where(Permission.name == perm_name)
    #         )
    #         permission = perm_result.scalar_one()

    #         rp_result = await db.execute(
    #             select(RolePermission).where(
    #                 RolePermission.role_id == role.id,
    #                 RolePermission.permission_id == permission.id,
    #             )
    #         )

    #         mapping = rp_result.scalar_one_or_none()

    #         if not mapping:
    #             db.add(
    #                 RolePermission(
    #                     role_id=role.id,
    #                     permission_id=permission.id,
    #                 )
    #             )

    # await db.commit()

    print(" RBAC seed completed")
    
    
    
