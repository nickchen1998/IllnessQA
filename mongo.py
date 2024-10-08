import contextlib
from pymongo.mongo_client import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from env_settings import EnvSettings


@contextlib.contextmanager
def get_mongo_database() -> Database:
    env_settings = EnvSettings()
    client = MongoClient(host=env_settings.MONGODB_ATLAS_URI)
    try:
        yield Database(client, name=env_settings.MONGODB_DATABASE)
    finally:
        client.close()


def insert_datas(datas: list):
    with get_mongo_database() as database:
        collection = Collection(database=database, name="Illness")
        collection.insert_many(datas)
