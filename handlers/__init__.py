from aiogram import Router

from .command_handlers import command_router
from .keyboards_handlers import keyboard_router
from .ai_handlers import ai_handler
from .callback_handlers import callback_router

all_handlers_router = Router()
all_handlers_router.include_routers(
    command_router,
    ai_handler,
    keyboard_router,
    callback_router,
)

__all__ = [
    'all_handlers_router',
]
