from typing import Callable

from loguru import logger
from fastapi import FastAPI

from settings import Settings
from db import get_database


def get_startup_handler(app: FastAPI, settings: Settings) -> Callable:
    async def startup_event() -> None:
        logger.info("Starting app...")

        app.state.db = await get_database(settings)
        logger.debug(f"DB: {app.state.db}")

    return startup_event


def get_shutdown_handler(app: FastAPI, settings: Settings) -> Callable:
    async def shutdown_event() -> None:
        logger.info("Shutting down...")

    return shutdown_event
