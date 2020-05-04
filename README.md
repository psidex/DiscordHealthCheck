# Discord Health Check

A small library for automating Docker healthchecks for discord.py bots.

`pip install discordhealthcheck`

## Usage

### In Code

```python
import discord
import discordhealthcheck

class ExampleClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        discordhealthcheck.start(self, port=4040)
```

### In Dockerfile

```dockerfile
FROM python:3.8-slim-buster

# Copy files, install requirements, etc.
# Make sure `pip install discordhealthcheck` happens

HEALTHCHECK CMD discordhealthcheck -p 4040 || exit 1

CMD ["python","./path/to/bot/main.py"]
```
