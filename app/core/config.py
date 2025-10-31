from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_USER: str = "space"
    DB_PASS: str = "space"
    DB_NAME: str = "spacetracker"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5440

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"


settings = Settings()
