from fastapi import APIRouter

from app.api.routes.chat import router as chat_router
from app.api.routes.system import router as system_router
from app.core.config import settings

router = APIRouter(prefix=settings.api_prefix)

router.include_router(system_router)
router.include_router(chat_router)