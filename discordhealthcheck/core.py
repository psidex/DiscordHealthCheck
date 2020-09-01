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
        message = b"healthy"

        if (
            self.client.latency > self.bot_max_latency  # Latency too high
            or self.client.user is None  # Not logged in
            or not self.client.is_ready()  # Client’s internal cache not ready
            or self.client.is_closed()  # The websocket connection is closed
        ):
            message = b"unhealthy"

        writer.write(message)
        writer.close()


def start(
    client: discord.client, port: int = 40404, bot_max_latency: float = 0.5
) -> asyncio.Task:
    """Starts the health check server.

    Args:
        client: The discord.py client object to monitor
        port: The port to bind the TCP socket server to
        bot_max_latency: The maximum acceptable latency (in seconds) for the bots
            connection to Discord

    Returns:
        asyncio.Task: The Task object for the healthcheck socket server

    """
    host = "127.0.0.1"
    ctx = _ClientContext(client, bot_max_latency)
    return client.loop.create_task(
        asyncio.start_server(ctx.handle_socket_client, host, port)
    )
