import sys

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles

from .app.routes import router
from .core.config.settings import settings
from .core.events import lifespan
from .core.middlewares import register_middlewares

sys.tracebacklimit = settings.APP_TRACEBACK_DEPTH

app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)

register_middlewares(app)

app.include_router(router)

app.mount(settings.STATIC_URL, StaticFiles(directory=settings.STATIC_DIR), name="static")
