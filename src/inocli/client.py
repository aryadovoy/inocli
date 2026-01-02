import sys
from enum import Enum
from typing import Final

from aiohttp import ClientSession

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from yarl import URL

from inocli.configs import InoreaderConfig
from inocli.schemas import (
    StreamContents,
    SubscriptionsList,
    TagsList,
    UserInfo,
)


class SystemTag(str, Enum):
    READ = "user/-/state/com.google/read"
    STARRED = "user/-/state/com.google/starred"
    LIKED = "user/-/state/com.google/like"
    BROADCAST = "user/-/state/com.google/broadcast"
    ANNOTATED = "user/-/state/com.google/annotated"
    SAVED_WEB_PAGES = "user/-/state/com.google/saved-web-pages"


class CustomTag:
    def __init__(self, tag_name: str) -> None:
        self.tag_name = tag_name

    @property
    def value(self) -> str:
        return f"user/-/label/{self.tag_name}"

    def __str__(self) -> str:
        return self.value


class InoreaderClient:
    USER_INFO_PATH: Final = "user-info"
    SUBSCRIPTION_LIST_PATH: Final = "subscription/list"
    TAG_LIST_PATH: Final = "tag/list"
    CONTENT_PATH: Final = "stream/contents"
    EDIT_TAG_PATH: Final = "edit-tag"

    def __init__(self, config: InoreaderConfig, api_key: str) -> None:
        self._config = config
        headers = {
            "Authorization": f"GoogleLogin auth={api_key}",
            "AppId": self._config.app_id,
            "AppKey": self._config.app_key,
        }
        self._client = ClientSession(
            headers=headers,
            base_url=config.base_api_url,
        )

    @classmethod
    async def create(cls, config: InoreaderConfig) -> Self:
        tmp_client = ClientSession()
        try:
            api_key = await cls._fetch_api_key(
                client=tmp_client, config=config
            )
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
            },
        ) as response:
            data = await response.text()
            return data.split("\n")[2].strip("Auth=")

    async def get_user_info(self) -> UserInfo:
        async with self._client.get(self.USER_INFO_PATH) as response:
            return UserInfo.model_validate(await response.json())

    async def get_subscriptions(self) -> SubscriptionsList:
        async with self._client.get(self.SUBSCRIPTION_LIST_PATH) as response:
            return SubscriptionsList.model_validate(await response.json())

    async def get_tags(self) -> TagsList:
        params = {"types": 1, "count": 1}
        async with self._client.get(
            self.TAG_LIST_PATH, params=params
        ) as response:
            return TagsList.model_validate(await response.json())

    async def get_content(
        self,
        stream_id: str | None = None,
        include: list[SystemTag | CustomTag] | None = None,
        exclude: list[SystemTag | CustomTag] | None = None,
    ) -> StreamContents:
        if stream_id:
            url_path = f"{self.CONTENT_PATH}/{stream_id}"
        else:
            url_path = self.CONTENT_PATH

        params = {
            "n": 100,  # maximum number of items to return
            "r": "o",  # order by oldest first
        }
        if include:
            params["it"] = [tag.value for tag in include]
        if exclude:
            params["xt"] = [tag.value for tag in exclude]
        async with self._client.get(url_path, params=params) as response:
            return StreamContents.model_validate(await response.json())

    async def edit_tag(
        self,
        item_ids: list[str],
        to_add: list[SystemTag | CustomTag] | None = None,
        to_remove: list[SystemTag | CustomTag] | None = None,
    ) -> str:
        if not to_add and not to_remove:
            raise ValueError("Either 'to_add' or 'to_remove' must be provided")

        params = {}
        if to_add:
            params["a"] = [tag.value for tag in to_add]

        if to_remove:
            params["r"] = [tag.value for tag in to_remove]

        for item_id in item_ids:
            if "i" not in params:
                params["i"] = []
            params["i"].append(item_id)

        async with self._client.post(
            self.EDIT_TAG_PATH, params=params
        ) as response:
            return await response.text()

    async def close(self) -> None:
        await self._client.close()
