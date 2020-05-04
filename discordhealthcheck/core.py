import asyncio

import discord


class _ClientContext:
    """A simple class to keep context for the client handler function"""

    def __init__(self, client: discord.client, bot_max_latency: float):
        self.client = client
        self.bot_max_latency = bot_max_latency

    async def handle_socket_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        message = b"unhealthy"

        if self.client.latency <= self.bot_max_latency:
            message = b"healthy"

        writer.write(message)
        writer.close()


def start(
    client: discord.client, port: int = 40404, bot_max_latency: float = 0.2
) -> None:
    """Starts the health check server.

    Args:
        client: The discord.py client object to monitor
        port: The port to bind the TCP socket server to
        bot_max_latency: The maximum acceptable latency (in seconds) for the bots
            connection to Discord

    """
    host = "127.0.0.1"
    ctx = _ClientContext(client, bot_max_latency)
    client.loop.create_task(asyncio.start_server(ctx.handle_socket_client, host, port))
