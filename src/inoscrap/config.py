from typing import Final, Self

from pydantic import EmailStr, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", frozen=True)

    @classmethod
    def get(cls) -> Self:
        return cls()


class InoreaderConfig(BaseConfig):
    app_id: str
    app_key: str
    email: EmailStr
    password: SecretStr
    base_api_url: Final = "https://www.inoreader.com/reader/api/0/"

    model_config = SettingsConfigDict(env_prefix="inoreader_")


class Config(BaseSettings):
    inoreader: InoreaderConfig

    @classmethod
    def get(cls) -> Self:
        return cls(
            inoreader=InoreaderConfig.get(),
        )
