from functools import lru_cache
from pathlib import Path
from dotenv import dotenv_values

class Settings:
    def __init__(self) -> None:
        env_path = Path(".env")
        env = dotenv_values(env_path)
        self.mongodb_uri = env.get("MONGODB_URI")
        self.mongodb_db = env.get("MONGODB_DB")
        self.port = int(env["PORT"]) if env.get("PORT") else None
        if not self.mongodb_uri or not self.mongodb_db or self.port is None:
            raise RuntimeError("Missing required configuration in .env")

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
