import os
import json
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent, ServerCapabilities, ToolsCapability
from src.mcp.tools import TOOL_DEFS, call_tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("task-tracker-mcp")

server = Server("task-tracker")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    return TOOL_DEFS


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    logger.info(f"Tool call: {name}")
    try:
        result = call_tool(name, arguments)
        return [TextContent(type="text", text=result)]
    except Exception as e:
        logger.error(f"Tool error: {e}")
        return [TextContent(type="text",
                text=json.dumps({"error": str(e)}))]


async def serve_stdio():
    init_opts = InitializationOptions(
        server_name="task-tracker",
        server_version="1.0.0",
        capabilities=ServerCapabilities(tools=ToolsCapability()),
    )
    async with stdio_server() as (read, write):
        await server.run(read, write, init_opts)


if __name__ == '__main__':
    import asyncio
    asyncio.run(serve_stdio())
