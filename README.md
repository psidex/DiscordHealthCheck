# Discord Health Check

A small library and command line app to automate Docker health checks for [discord.py](https://discordpy.readthedocs.io/en/latest/) bots.

## How it works

### Server

The library has 1 function, `start`. This takes a `discord.Client` object as well as optional parameters. This function
creates a TCP socket server and when a client connects, it tests the discord client for various things that indicate
its health. The result of this health check is then sent to the client.

The socket server is started by creating an async Task in the Discord clients loop using `asyncio.start_server` .

The default server port is `40404`.

### Client

The CLI app is a simple client that connects to the server and determines its exit code from what the server sends.

## Installation

`pip install discordhealthcheck`

This will install both the Python library and the command line app, the python library is importable using `import discordhealthcheck` and the CLI app by using the command `discordhealthcheck`.

## Usage Examples

### Python Library (Server)

The only function you will need is `start`. Here's the function signature:

```python
def start(
    client: discord.client,
    port: int = 40404,
    bot_max_latency: float = 0.5
) -> asyncio.Task
```

Here's how you might use it:

```python
import discord
import discordhealthcheck

class CustomClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.healthcheck_task = discordhealthcheck.start(self)
        # Later you can cancel or check on self.healthcheck_task
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

### Dockerfile (Client)

```dockerfile
FROM python:3.8-slim-buster

# Copy files, install requirements, setup bot, etc.

RUN pip install discordhealthcheck

HEALTHCHECK CMD discordhealthcheck || exit 1

CMD ["python", "/path/to/bot.py"]
```
