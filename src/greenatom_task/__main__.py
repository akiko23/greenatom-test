"""Application entry point."""

import asyncio
import os
import sys

from greenatom_task.web.app_setup import (
    create_app,
    create_http_server,
    initialise_dependencies,
    initialise_routers,
)
from greenatom_task.web.config import load_config
from greenatom_task.web.consts import DEFAULT_CONFIG_PATH


async def main() -> None:
    """Set up application and start http server."""
    config = load_config(os.getenv("CONFIG_PATH") or DEFAULT_CONFIG_PATH)
    app = create_app(config.app)

    initialise_routers(app)
    initialise_dependencies(app, config)

    server = create_http_server(app, config.http_server)
    await server.serve()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        loop = asyncio.ProactorEventLoop()

    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
