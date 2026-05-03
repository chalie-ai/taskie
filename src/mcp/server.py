import os
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from src.mcp.tools import register_tools

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8080/api")


def api_url(path):
    return f"{API_BASE}{path}"


def get_client(token=None):
    headers = {}
    if token:
        headers['X-Agent-Token'] = token
    return httpx.AsyncClient(headers=headers)


async def list_tickets(agent_token: str = "", cycle_id: int = None,
                       project_id: int = None, status: str = None,
                       assignee: str = None, search: str = ""):
    params = {}
    if cycle_id: params['cycle_id'] = cycle_id
    if project_id: params['project_id'] = project_id
    if status: params['status'] = status
    if assignee: params['assignee'] = assignee
    if search: params['search'] = search

    async with get_client(agent_token) as client:
        r = await client.get(api_url('/tickets'), params=params)
        r.raise_for_status()
        tickets = r.json()
        return [{
            'id': t['id'], 'display_id': t['display_id'], 'name': t['name'],
            'type': t['type'], 'priority': t['priority'], 'status': t['status'],
            'project_name': t.get('project_name', ''),
            'assignee': t.get('assignee', ''),
            'comment_count': t.get('comment_count', 0),
            'created_at': t['created_at'], 'updated_at': t['updated_at'],
        } for t in tickets]


async def get_ticket(ticket_id: int, agent_token: str = ""):
    async with get_client(agent_token) as client:
        r = await client.get(api_url(f'/tickets/{ticket_id}'))
        r.raise_for_status()
        return r.json()


async def create_ticket(agent_token: str, name: str,
                        description: str = "", type: str = "feature",
                        priority: str = "medium", status: str = "backlog",
                        project_id: int = None, cycle_id: int = None,
                        assignee: str = "", due_date: str = ""):
    async with get_client(agent_token) as client:
        r = await client.post(api_url('/tickets'), json={
            'name': name, 'description': description, 'type': type,
            'priority': priority, 'status': status,
            'project_id': project_id, 'cycle_id': cycle_id,
            'assignee': assignee,
            'due_date': due_date if due_date else None,
        })
        r.raise_for_status()
        return r.json()


async def update_ticket(ticket_id: int, agent_token: str,
                        name: str = None, description: str = None,
                        type: str = None, priority: str = None,
                        status: str = None, assignee: str = None,
                        due_date: str = None):
    data = {'author_name': 'Claude'}
    if name is not None: data['name'] = name
    if description is not None: data['description'] = description
    if type is not None: data['type'] = type
    if priority is not None: data['priority'] = priority
    if status is not None: data['status'] = status
    if assignee is not None: data['assignee'] = assignee
    if due_date is not None: data['due_date'] = due_date

    async with get_client(agent_token) as client:
        r = await client.patch(api_url(f'/tickets/{ticket_id}'), json=data)
        r.raise_for_status()
        return r.json()


async def delete_ticket(ticket_id: int, agent_token: str):
    async with get_client(agent_token) as client:
        r = await client.delete(api_url(f'/tickets/{ticket_id}'))
        r.raise_for_status()
        return {'deleted': True}


async def reorder_tickets(agent_token: str, items: list):
    async with get_client(agent_token) as client:
        r = await client.put(api_url('/tickets/reorder'), json={'items': items})
        r.raise_for_status()
        return r.json()


async def add_comment(ticket_id: int, body: str, agent_token: str,
                      pr_url: str = "", pr_title: str = ""):
    data = {
        'body': body,
        'author_type': 'agent',
        'author_name': 'Claude',
    }
    if pr_url:
        data['pr_url'] = pr_url
        data['pr_title'] = pr_title

    async with get_client(agent_token) as client:
        r = await client.post(api_url(f'/tickets/{ticket_id}/comments'), json=data)
        r.raise_for_status()
        return {'status': 'Comment added', 'ticket_id': ticket_id}


async def list_comments(ticket_id: int, agent_token: str = ""):
    async with get_client(agent_token) as client:
        r = await client.get(api_url(f'/tickets/{ticket_id}/comments'))
        r.raise_for_status()
        return r.json()


async def submit_pr_link(ticket_id: int, url: str, agent_token: str,
                         title: str = "", status: str = "open"):
    async with get_client(agent_token) as client:
        r = await client.post(api_url(f'/tickets/{ticket_id}/pr-links'), json={
            'url': url, 'title': title, 'status': status,
        })
        r.raise_for_status()
        return {'status': 'PR link submitted', 'ticket_id': ticket_id}


async def list_pr_links(ticket_id: int, agent_token: str = ""):
    async with get_client(agent_token) as client:
        r = await client.get(api_url(f'/tickets/{ticket_id}/pr-links'))
        r.raise_for_status()
        return r.json()


async def delete_pr_link(ticket_id: int, pr_id: int, agent_token: str):
    async with get_client(agent_token) as client:
        r = await client.delete(api_url(f'/tickets/{ticket_id}/pr-links/{pr_id}'))
        r.raise_for_status()
        return {'deleted': True}


async def list_relationships(ticket_id: int, agent_token: str = ""):
    async with get_client(agent_token) as client:
        r = await client.get(api_url(f'/tickets/{ticket_id}/relationships'))
        r.raise_for_status()
        return r.json()


async def add_relationship(ticket_id: int, agent_token: str,
                           related_ticket_id: int, relationship_type: str = "related"):
    async with get_client(agent_token) as client:
        r = await client.post(api_url(f'/tickets/{ticket_id}/relationships'), json={
            'related_ticket_id': related_ticket_id,
            'relationship_type': relationship_type,
        })
        r.raise_for_status()
        return r.json()


async def remove_relationship(ticket_id: int, relationship_id: int,
                              agent_token: str):
    async with get_client(agent_token) as client:
        r = await client.delete(
            api_url(f'/tickets/{ticket_id}/relationships/{relationship_id}'))
        r.raise_for_status()
        return {'deleted': True}


async def get_ticket_history(ticket_id: int, agent_token: str = ""):
    async with get_client(agent_token) as client:
        r = await client.get(api_url(f'/tickets/{ticket_id}/history'))
        r.raise_for_status()
        return r.json()


async def get_stats(agent_token: str = "", cycle_id: int = None):
    params = {}
    if cycle_id: params['cycle_id'] = cycle_id
    async with get_client(agent_token) as client:
        r = await client.get(api_url('/stats'), params=params)
        r.raise_for_status()
        return r.json()


def create_server():
    server = Server("task-tracker")
    tools = [
        list_tickets, get_ticket, create_ticket, update_ticket, delete_ticket,
        reorder_tickets, add_comment, list_comments, submit_pr_link,
        list_pr_links, delete_pr_link, list_relationships, add_relationship,
        remove_relationship, get_ticket_history, get_stats,
    ]
    register_tools(server, tools)
    return server


async def serve_stdio():
    server = create_server()
    async with stdio_server() as (read, write):
        await server.run(read, write)


if __name__ == '__main__':
    import asyncio
    asyncio.run(serve_stdio())
