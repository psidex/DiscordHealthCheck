import asyncio

import discord


class _ClientContext:
    """A simple class to keep context for the client handler function"""

    def __init__(self, client: discord.client, bot_max_latency: float):
        self.client = client
        self.bot_max_latency = bot_max_latency

    def handle_socket_client(self, writer: asyncio.StreamWriter, **kwargs) -> None:
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
) -> asyncio.base_events.Server:
    """Starts the health check server.

    Args:
        client: The discord.py client object to monitor
        port: The port to bind the TCP socket server to
        bot_max_latency: The maximum acceptable latency (in seconds) for the bots
            connection to Discord

    Returns:
        asyncio.base_events.Server: The Server object for the healthcheck server

    """
    host = "127.0.0.1"
    ctx = _ClientContext(client, bot_max_latency)
    # The type is ignored as it expects handle_socket_client to accept a writer,
    # instead **kwargs is used.
    return client.loop.run_until_complete(
        asyncio.start_server(ctx.handle_socket_client, host, port)  # type: ignore
    )
