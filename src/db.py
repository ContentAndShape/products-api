from typing import List, Dict
from pprint import pformat

from loguru import logger
from pymongo.database import Database
from pymongo.collection import Collection
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCursor

from settings import Settings
from dependencies import FilterParams


async def get_database(settings: Settings) -> Database:
    client = AsyncIOMotorClient(settings.db_conn_str)
    return client[settings.db_name]


async def get_documents(
    db: Database,
    collection: str,
    filter_params: FilterParams,
    skip: int,
    limit: int,
) -> List[Dict]:
    collection: Collection = db[collection]

    logger.debug(f"Filter params: {filter_params}")
    query = filter_params.get_query()
    logger.debug(f"Query: {pformat(query)}")

    cursor: AsyncIOMotorCursor = collection.find(
        query
    ).skip(skip).limit(limit)
    res = []
    for doc in await cursor.to_list(length=limit):
        logger.debug(pformat(doc))
        res.append(doc)

    return res
    