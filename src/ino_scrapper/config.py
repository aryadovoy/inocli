from pydantic_settings import BaseSettings, SettingsConfigDict

class InoreaderConfig(BaseSettings):
    app_id: str
    api_key: str
    password: str

    model_config = SettingsConfigDict(env_file=".env", env_prefix="inoreader_")


class Config(BaseSettings):
    inoreader: InoreaderConfig


def get_config():
    return Config(
        inoreader=InoreaderConfig(),
    )
