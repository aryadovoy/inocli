from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator
from yarl import URL


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

    @classmethod
    def timestamp_validator(cls, v: int | str) -> datetime:
        if isinstance(v, (int, str)):
            timestamp = int(v) if isinstance(v, str) else v
            return datetime.fromtimestamp(timestamp)
        return v


class UserInfo(BaseSchema):
    user_id: str = Field(validation_alias="userId")
    user_name: str = Field(validation_alias="userName")
    user_profile_id: str = Field(validation_alias="userProfileId")
    user_email: str = Field(validation_alias="userEmail")
    is_blogger_user: bool = Field(validation_alias="isBloggerUser")
    signup_time_sec: datetime = Field(validation_alias="signupTimeSec")
    is_multi_login_enabled: bool = Field(
        validation_alias="isMultiLoginEnabled"
    )

    @field_validator("signup_time_sec", mode="before")
    @classmethod
    def convert_timestamp(cls, v: int | str) -> datetime:
        return cls.timestamp_validator(v)


class Category(BaseSchema):
    id: str
    label: str


class Subscription(BaseSchema):
    id_: str = Field(validation_alias="id")
    feed_type: str = Field(validation_alias="feedType")
    title: str
    categories: list[Category]
    sort_id: str = Field(validation_alias="sortid")
    first_item_msec: int = Field(validation_alias="firstitemmsec")
    url: str
    html_url: str = Field(validation_alias="htmlUrl")
    icon_url: str = Field(validation_alias="iconUrl")


class SubscriptionsList(BaseSchema):
    subscriptions: list[Subscription]


class Tag(BaseSchema):
    id_: str = Field(validation_alias="id")
    sort_id: str = Field(validation_alias="sortid")
    unread_count: int | None = Field(
        default=None, validation_alias="unreadCount"
    )
    unseen_count: int | None = Field(
        default=None, validation_alias="unseenCount"
    )
    type_: Literal["tag", "folder", "active_search"] | None = Field(
        default=None, validation_alias="type"
    )
    pinned: int | None = None
    article_count: int | None = Field(
        default=None, validation_alias="articleCount"
    )
    article_count_today: int | None = Field(
        default=None, validation_alias="articleCountToday"
    )


class TagsList(BaseSchema):
    tags: list[Tag]


class Link(BaseSchema):
    href: HttpUrl
    type_: str | None = Field(default=None, validation_alias="type")

    @property
    def url(self) -> URL:
        return URL(f"{self.href.scheme}://{self.href.host}{self.href.path}")


class Summary(BaseSchema):
    direction: str
    content: str


class Origin(BaseSchema):
    stream_id: str = Field(validation_alias="streamId")
    title: str
    html_url: HttpUrl = Field(validation_alias="htmlUrl")


class Item(BaseSchema):
    crawl_time_msec: str = Field(validation_alias="crawlTimeMsec")
    timestamp_usec: str = Field(validation_alias="timestampUsec")
    id_: str = Field(validation_alias="id")
    categories: list[str]
    title: str
    published: datetime
    updated: datetime
    canonical: list[Link]
    alternate: list[Link]
    summary: Summary
    author: str
    liking_users: list[str] = Field(validation_alias="likingUsers")
    comments: list[str]
    comments_num: int = Field(validation_alias="commentsNum")
    annotations: list[str]
    origin: Origin
    summaries: list[str]

    @field_validator(
        "published",
        "updated",
        mode="before",
    )
    @classmethod
    def convert_timestamps(cls, v: int | str) -> datetime:
        return cls.timestamp_validator(v)


class StreamContents(BaseSchema):
    direction: str
    id_: str = Field(validation_alias="id")
    title: str
    description: str
    self_: Link = Field(validation_alias="self")
    updated: datetime
    updated_usec: str = Field(validation_alias="updatedUsec")
    items: list[Item]

    @field_validator("updated", mode="before")
    @classmethod
    def convert_timestamp(cls, v: int | str) -> datetime:
        return cls.timestamp_validator(v)
