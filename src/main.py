from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .core.config.settings import settings
from .core.events import lifespan
from .core.middlewares import register_middlewares
from .app.routes import router

app = FastAPI(lifespan=lifespan)

register_middlewares(app)

app.include_router(router)

app.mount(settings.STATIC_URL, StaticFiles(directory=settings.STATIC_DIR), name="static")
