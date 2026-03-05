from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.menu_items.router import router as menu_router
from app.users.routers import router as user_router
from app.restaurants.router import router as restaurant_router
from app.orders.router import router as orders_router
from app.payments.router import router as payments_router
# from app.notifications.router import router as notifications_router

app = FastAPI()


app.include_router(menu_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(restaurant_router)
app.include_router(orders_router)
app.include_router(payments_router)
# app.include_router(notifications_router)
