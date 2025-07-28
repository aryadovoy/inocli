# Unofficial Inoreader Client

An async Python client for the Inoreader API that provides easy access to your RSS feeds, subscriptions, and content management.

## Features

- **Async/await support** - Built with aiohttp for efficient async operations
- **Type safety** - Full type hints and Pydantic models for data validation
- **Easy authentication** - Automatic API key management
- **Tag management** - Read, star, like, and organize your articles
- **Custom tags** - Create and manage your own tags

## Installation

Install directly from GitHub:

```shell
pip install git+https://github.com/aryadovoy/inocli.git
```

Or by `uv`:

```bash
uv add "git+https://github.com/aryadovoy/inocli.git"
```

## Quick Start

### 1. Setup Configuration

Create a `.env` file with your Inoreader credentials:

```env
INOREADER_APP_ID=your_app_id
INOREADER_APP_KEY=your_app_key
INOREADER_EMAIL=your_email@example.com
INOREADER_PASSWORD=your_password
```

### 2. Basic Usage

```python
import asyncio
from inocli.client import InoreaderClient
from inocli.configs import InoreaderConfig

async def main():
    # Load configuration from environment variables
    config = InoreaderConfig.get()

    # Create client (automatically handles authentication)
    client = await InoreaderClient.create(config)

    try:
        # Get user information
        user_info = await client.get_user_info()
        print(f"Welcome, {user_info.user_name}!")

        # Get all subscriptions
        subscriptions = await client.get_subscriptions()
        print(f"You have {len(subscriptions.subscriptions)} subscriptions")

        # Get latest content
        content = await client.get_content()
        print(f"Found {len(content.items)} items")

    finally:
        await client.close()

# Run the example
asyncio.run(main())
```

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
