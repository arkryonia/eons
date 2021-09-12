
import os

from typing import List, Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "eons"
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    DEV_DB: str = f"postgresql://postgres:postgres@localhost/db_{PROJECT_NAME}"
   
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL", DEV_DB)  
    

    class Config:
        case_sensitive = True


settings = Settings()
