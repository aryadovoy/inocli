import sys
from typing import ClassVar

from pydantic import EmailStr, SecretStr

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", frozen=True
    )

    @classmethod
    def get(cls) -> Self:
        return cls()


class InoreaderConfig(BaseConfig):
    app_id: str
    app_key: str
    email: EmailStr
    password: SecretStr
    base_api_url: ClassVar[str] = "https://www.inoreader.com/reader/api/0/"

    model_config = SettingsConfigDict(env_prefix="inoreader_")
