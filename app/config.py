from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # @classmethod
    # def make_dirs(cls):
    #     print("mmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
    #     if not os.path.exists("audio/en"):
    #         print("--------------------------")
    #         os.makedirs("audio")
    #     if not os.path.exists("audio/ru"):
    #         os.makedirs("audio/ru")

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()