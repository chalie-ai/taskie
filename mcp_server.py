#!/usr/bin/env python3
"""MCP Server for Task Tracker — Streamable HTTP transport.

Talks to the Flask API as an HTTP client. Zero database access.
Run: python mcp_server.py
"""

import os
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from tools_registry import register_tools

API_BASE = os.getenv("API_BASE_URL", "http://localhost:5000/api")
MCP_PORT = int(os.getenv("MCP_PORT", "5100"))


def api_url(path):
    return f"{API_BASE}{path}"


async def list_tickets(cycle_id: int = None, project_id: int = None,
                        status: str = None, assignee: str = None):
    """List all tickets. Optional filters: cycle_id, project_id, status, assignee."""
    params = {}
    if cycle_id:
        params['cycle_id'] = cycle_id
    if project_id:
        params['project_id'] = project_id
    if status:
        params['status'] = status
    if assignee:
        params['assignee'] = assignee

    async with httpx.AsyncClient() as client:
        r = await client.get(api_url('/tickets'), params=params)
        r.raise_for_status()
        tickets = r.json()
        return [{
            'id': t['id'],
            'display_id': t['display_id'],
            'name': t['name'],
            'type': t['type'],
            'priority': t['priority'],
            'status': t['status'],
            'project_name': t.get('project_name', ''),
            'assignee': t.get('assignee', ''),
            'comment_count': t.get('comment_count', 0),
            'created_at': t['created_at'],
            'updated_at': t['updated_at'],
        } for t in tickets]


async def get_ticket(ticket_id: int):
    """Get full details of a ticket including description, comments, and PR links."""
    async with httpx.AsyncClient() as client:
        r = await client.get(api_url(f'/tickets/{ticket_id}'))
        r.raise_for_status()
        return r.json()


async def add_comment(ticket_id: int, body: str):
    """Add a comment to a ticket as the AI agent."""
    async with httpx.AsyncClient() as client:
        r = await client.post(api_url(f'/tickets/{ticket_id}/comments'), json={
            'body': body,
            'author_type': 'agent',
            'author_name': 'Claude',
        })
        r.raise_for_status()
        return {'status': 'Comment added', 'ticket_id': ticket_id}


async def submit_pr_link(ticket_id: int, url: str, title: str = "", status: str = "open"):
    """Submit a PR link for a ticket."""
    async with httpx.AsyncClient() as client:
        r = await client.post(api_url(f'/tickets/{ticket_id}/pr-links'), json={
            'url': url,
            'title': title,
            'status': status,
        })
        r.raise_for_status()
        return {'status': 'PR link submitted', 'ticket_id': ticket_id}


def create_server():
    server = Server("task-tracker")
    register_tools(server, list_tickets, get_ticket, add_comment, submit_pr_link)
    return server


async def serve_stdio():
    server = create_server()
    async with stdio_server() as (read, write):
        await server.run(read, write)


if __name__ == '__main__':
    import asyncio
    asyncio.run(serve_stdio())
