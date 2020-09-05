# Discord Health Check

[![PyPI - Downloads](https://img.shields.io/pypi/dm/discordhealthcheck)](https://pypi.org/project/discordhealthcheck/)
[![PyPI](https://img.shields.io/pypi/v/discordhealthcheck)](https://pypi.org/project/discordhealthcheck/)
[![license](https://img.shields.io/github/license/psidex/EACS.svg)](./LICENSE)
[![Ko-fi donate link](https://img.shields.io/badge/Support%20Me-Ko--fi-orange.svg?style=flat&colorA=35383d)](https://ko-fi.com/M4M18XB1)

A small Python 3 library and command line app to automate Docker health checks for [discord.py](https://discordpy.readthedocs.io/en/latest/) bots.

## Installation

`pip install discordhealthcheck`

This will install both the Python library and the command line app, the python library is importable using `import discordhealthcheck` and the CLI app by using the command `discordhealthcheck`.

## How It Works & Usage Examples

### Python Library (Server)

The library has 1 function, `start`. This takes a `discord.Client` object as well as optional parameters:

```python
def start(
    client: discord.client,
    port: int = 40404,
    bot_max_latency: float = 0.5
) -> asyncio.base_events.Server
```

`start` creates a TCP socket server which listens for any connections, and then when a client connects, it tests the
discord client for various things that indicate its health (latency, login status, etc.). The result of this health
check is then sent to the healthcheck client.

The returned `Server` object can be used to stop the server (e.g. `healthcheck_server.close()`)

The default port for the socket server is `40404`, if you change it you will need to use the `--port` flag on the
client as well.

Here's some example usage:

```python
import discord
import discordhealthcheck

class CustomClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.healthcheck_server = discordhealthcheck.start(self)
        # Later you can close or check on self.healthcheck_server
```

or

```python
import discord
import discordhealthcheck

client = discord.Client()
discordhealthcheck.start(client)

@client.event
async def on_ready():
    print("Logged in")
```

### CLI App (Client)

The CLI app is a simple client that connects to the server and determines its exit code from what the server sends; `0`
for healthy, `1` for unhealthy.

Here's an example of using in a Dockerfile:

```dockerfile
FROM python:3.8-slim-buster

# Copy files, install requirements, setup bot, etc.

RUN pip install discordhealthcheck

# The `|| exit 1` isn't required but it's good practice anyway.
HEALTHCHECK CMD discordhealthcheck || exit 1

CMD ["python", "/path/to/bot.py"]
```
