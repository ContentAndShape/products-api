from pydantic import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    db_username: str
    db_password: str
    db_name: str

    @property
    def db_conn_str(self) -> str:
        return f"mongodb://{self.db_username}:{self.db_password}@127.0.0.1/{self.db_name}?authSource=admin"


def get_settings() -> Settings:
    return Settings()
