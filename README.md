# Discord Health Check

[![CI](https://github.com/psidex/discordhealthcheck/workflows/CI/badge.svg)](https://github.com/psidex/discordhealthcheck/actions)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/discordhealthcheck?colorA=35383d)](https://pypi.org/project/discordhealthcheck/)
[![PyPI](https://img.shields.io/pypi/v/discordhealthcheck?colorA=35383d)](https://pypi.org/project/discordhealthcheck/)
[![Black formatter](https://img.shields.io/badge/Code%20Style-Black-000000.svg?colorA=35383d)](https://github.com/psf/black)

A small Python 3 library and command line app to automate Docker health checks for [discord.py](https://discordpy.readthedocs.io/en/latest/) bots.

## Installation

`pip install discordhealthcheck`

This will install both the Python library and the command line app, the python library is importable using `import discordhealthcheck` and the CLI app by using the command `discordhealthcheck`.

## How It Works & Usage Examples

### Python Library (Server)

The library has 1 function, `start`.

`start` takes a `discord.Client` object as well as optional parameters, and returns an awaitable that produces a `asyncio.base_events.Server`:

```python
def start(
    client: discord.client,
    port: int = 40404,
    bot_max_latency: float = 0.5
) -> Awaitable[asyncio.base_events.Server]
```

`start` calls [`asyncio.start_server`](https://docs.python.org/3/library/asyncio-stream.html#asyncio.start_server), creating an asyncio TCP socket server which listens for connections. Once a client connects, it tests the discord client for various things that indicate its health (latency, login status, etc.), and the result of this health check is then sent to the healthcheck client.

The returned `Server` object can be used to stop the server (e.g. `healthcheck_server.close()`)

The default port for the socket server is `40404`, if you change it you will need to use the `--port` flag on the client as well.

Call `start` once your event loop is running, generally a good place to call from is inside your [`setup_hook`](https://discordpy.readthedocs.io/en/stable/api.html#discord.Client.setup_hook) method:

```python
import discord
import discordhealthcheck

class CustomClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        self.healthcheck_server = await discordhealthcheck.start(self)
        # Later you can close or check on self.healthcheck_server
```

### CLI App (Client)

The CLI app is a simple client that connects to the server and determines its exit code from what the server sends; `0`
for healthy, `1` for unhealthy.

Here's an example of using in a Dockerfile:

```dockerfile
FROM python:3.11-slim-buster

# Copy files, install requirements, setup bot, etc.

RUN pip install discordhealthcheck

# The `|| exit 1` isn't required but it's good practice anyway.
HEALTHCHECK CMD discordhealthcheck || exit 1

CMD ["python", "/path/to/bot.py"]
```
