from typing import Any, Final, Self, TypedDict

from aiohttp import ClientSession
from yarl import URL

from inoscrap.config import InoreaderConfig


class InoreaderHeaders(TypedDict):
    Authorization: str
    AppId: str
    AppKey: str


class InoreaderClient:
    USER_INFO_PATH: Final = "user-info"

    def __init__(self, config: InoreaderConfig, api_key: str) -> None:
        self._config = config
        self._api_key = api_key
        self._client = ClientSession(
            headers=self._headers,
            base_url=config.base_api_url,
        )

    @classmethod
    async def create(cls, config: InoreaderConfig) -> Self:
        tmp_client = ClientSession()
        try:
            api_key = await cls._fetch_api_key(client=tmp_client, config=config)
            return cls(config=config, api_key=api_key)
        finally:
            await tmp_client.close()

    @staticmethod
    async def _fetch_api_key(
        client: ClientSession, config: InoreaderConfig
    ) -> str:
        async with client.get(
            url=URL("https://www.inoreader.com/accounts/ClientLogin"),
            params={
                "Email": config.email,
                "Passwd": config.password.get_secret_value(),
            }
        ) as response:
            data = await response.text()
            return data.split("\n")[2].strip("Auth=")

    @property
    def _headers(self) -> InoreaderHeaders:
        return InoreaderHeaders(
            Authorization=f"GoogleLogin auth={self._api_key}",
            AppId=self._config.app_id,
            AppKey=self._config.app_key,
        )

    async def get_user_info(self) -> dict[str, Any]:
        async with self._client.get(
            self.USER_INFO_PATH, headers=self._headers
        ) as response:
            return await response.json()

    async def close(self) -> None:
        await self._client.close()
