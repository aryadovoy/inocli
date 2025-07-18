import asyncio
import logging

from inoscrap.client import InoreaderClient
from inoscrap.config import InoreaderConfig

logger = logging.getLogger(__name__)


async def main() -> None:
    config = InoreaderConfig.get()
    client = await InoreaderClient.create(config)

    try:
        user_info = await client.get_user_info()
        logger.info("User info: %s", user_info)
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
