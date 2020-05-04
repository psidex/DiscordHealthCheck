# Discord Health Check

A small library and command line app to automate Docker health checks for [discord.py](https://discordpy.readthedocs.io/en/latest/) bots.

## Installation

`pip install discordhealthcheck`

This will install both the Python library and the command line app.

## Usage

### Python Library

```python
import discord
import discordhealthcheck

class ExampleClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        discordhealthcheck.start(self, port=12345)
```

### Command Line App (in Dockerfile)

```dockerfile
FROM python:3.8-slim-buster

# Copy files, install requirements, setup bot, etc.
# Make sure `pip install discordhealthcheck` happens

HEALTHCHECK CMD discordhealthcheck --port 12345 || exit 1

CMD ["python","./path/to/bot/main.py"]
```
