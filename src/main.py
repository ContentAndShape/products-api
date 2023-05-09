from fastapi import FastAPI

from loguru import logger
from settings import get_settings
from events import get_startup_handler, get_shutdown_handler
from controllers import router


def main() -> None:
    settings = get_settings()
    logger.debug(settings)

    app = FastAPI()
    app.add_event_handler(
        "startup",
        get_startup_handler(app, settings),
    )
    app.add_event_handler(
        "shutdown",
        get_shutdown_handler(app, settings),
    )
    app.include_router(router)

    return app


app = main()
