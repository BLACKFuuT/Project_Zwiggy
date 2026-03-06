# app/main.py

from fastapi import FastAPI

# Import routers
from app.auth.router import router as auth_router
from app.menu_items.router import router as menu_router
from app.users.routers import router as user_router
from app.restaurants.router import router as restaurant_router
from app.orders.router import router as orders_router
from app.payments.router import router as payments_router
from app.admin.router import router as admin_router
from app.orders.router import router as calculate_router

#Import Middleware
from app.middleware.logging_middleware import logging_middleware
from app.middleware.request_id_middleware import request_id_middleware

from app.core.logging import setup_logging

setup_logging()

# Initialize FastAPI app with metadata
app = FastAPI(
    title="Zwiggy API",
    version="1.0",
    description="FastAPI project for restaurants, menu items, and orders with async support"
)

app.middleware("http")(logging_middleware)
app.middleware("http")(request_id_middleware)


# Include routers
app.include_router(auth_router)         # /auth
app.include_router(user_router)         # /users
app.include_router(restaurant_router)   # /restaurants
app.include_router(menu_router)         # /menu-items
app.include_router(orders_router)       # /orders
app.include_router(payments_router)     # /payments
app.include_router(admin_router)        # /admin
app.include_router(calculate_router)
# app.include_router(notifications_router)  # /notifications (if added later)