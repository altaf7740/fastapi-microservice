import json
import sys

from loguru import logger
from loguru._handler import Message

from .settings import settings

logger.remove()


def _json_sink(message: Message) -> None:
    record = message.record
    extra = record["extra"]
    log_obj: dict[str, object] = {
        "timestamp": record["time"].isoformat(),
        "level": record["level"].name,
        "module": record["name"],
        "function": record["function"],
        "file": record["file"].name,
        "line": record["line"],
        "message": record["message"],
    }
    if "request_id" in extra:
        log_obj["request_id"] = extra["request_id"]
    print(json.dumps(log_obj), file=sys.stderr)



if settings.ENV.upper().startswith("DEV"):
    print("going with dev logging")
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level:<8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level> | request_id=<yellow>{extra[request_id]}</yellow>",
        level=settings.APP_LOG_LEVEL.upper(),
    )
else:
    print("going with production logging")
    logger.add(_json_sink, level=settings.APP_LOG_LEVEL.upper())  # type: ignore
