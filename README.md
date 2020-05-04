# Discord Health Check

A small library and command line app to automate Docker health checks for [discord.py](https://discordpy.readthedocs.io/en/latest/) bots.

## How it works

The library has 1 function, `start`. This takes a `discord.Client` object as well as optional parameters. This function
creates a TCP socket server and when a client connects, it tests the discord client for various things that indicate
its health. The result of this health check is then sent to the client.

The CLI app is a simple client that connects to the server and determines its exit code from what the server sends.

## Installation

`pip install discordhealthcheck`

This will install both the Python library and the command line app.

The default server port is `40404`.

## Usage

### Python Library

```python
import discord
import discordhealthcheck

class ExampleClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        discordhealthcheck.start(self)
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

### Command Line App (in Dockerfile)

```dockerfile
FROM python:3.8-slim-buster

# Copy files, install requirements, setup bot, etc.
# Make sure `pip install discordhealthcheck` happens

HEALTHCHECK CMD discordhealthcheck || exit 1

CMD ["python","./path/to/bot/main.py"]
```
