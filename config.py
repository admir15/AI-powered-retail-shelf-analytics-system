from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    camera_index: int = 0
    database_url: str = "sqlite:///./database/shelf_analytics.db"
    app_name: str = "Retail Shelf Analytics API"
    debug: bool = True

    class Config:
        env_file = ".env"


settings = Settings()