"""Application entry point."""

import asyncio
import sys

from greenatom_task.app_setup import (
    create_app,
    create_http_server,
    initialise_dependencies,
    initialise_routers,
)
from greenatom_task.config import load_config
from greenatom_task.consts import DEFAULT_CONFIG_PATH


async def main() -> None:
    """Set up application and start http server."""
    config = load_config(DEFAULT_CONFIG_PATH)
    app = create_app(config.app)

    initialise_routers(app)
    initialise_dependencies(app, config)

    server = create_http_server(app, config.http_server)
    await server.serve()


if __name__ == '__main__':
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
