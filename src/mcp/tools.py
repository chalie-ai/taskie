import json
import os
import httpx
from mcp import types

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8080/api")


def api_url(path):
    return f"{API_BASE}{path}"


def get_client(token=None):
    headers = {}
    if token:
        headers['X-Agent-Token'] = token
    return httpx.Client(headers=headers)


TOOL_DEFS = [
    types.Tool(
        name="list_tickets",
        description="Search and list tickets with optional filters: cycle_id, project_id, status, assignee, search, no_cycle",
        inputSchema={
            "type": "object",
            "properties": {
                "agent_token": {"type": "string", "description": "Agent token (optional for read)"},
                "cycle_id": {"type": "integer", "description": "Filter by cycle ID"},
                "project_id": {"type": "integer", "description": "Filter by project ID"},
                "status": {"type": "string", "description": "Status: backlog, todo, progress, review, done, cancel"},
                "assignee": {"type": "string", "description": "Filter by assignee name"},
                "assignee_id": {"type": "integer", "description": "Filter by assignee user ID"},
                "search": {"type": "string", "description": "Server-side search on name and description"},
                "no_cycle": {"type": "boolean", "description": "Only tickets without a cycle (the Backlog page)"},
            },
        },
    ),
    types.Tool(
        name="get_ticket",
        description="Get full ticket details including comments, PR links, relationships, and history",
        inputSchema={
            "type": "object",
            "properties": {
                "ticket_id": {"type": "integer", "description": "Ticket ID"},
            },
            "required": ["ticket_id"],
        },
    ),
    types.Tool(
        name="create_ticket",
        description="Create a new ticket. Requires agent_token.",
        inputSchema={
            "type": "object",
            "properties": {
                "agent_token": {"type": "string", "description": "Your agent token (required)"},
                "name": {"type": "string", "description": "Ticket title"},
                "description": {"type": "string", "description": "Markdown description"},
                "type": {"type": "string", "description": "bug, feature, or chore"},
                "priority": {"type": "string", "description": "urgent, high, medium, low, or none"},
                "status": {"type": "string", "description": "Initial status"},
                "project_id": {"type": "integer", "description": "Project ID"},
                "cycle_id": {"type": "integer", "description": "Cycle ID"},
                "assignee": {"type": "string", "description": "Assignee name"},
                "assignee_id": {"type": "integer", "description": "Assignee user ID"},
                "due_date": {"type": "string", "description": "YYYY-MM-DD"},
            },
            "required": ["agent_token", "name"],
        },
    ),
    types.Tool(
        name="update_ticket",
        description="Update ticket fields. Requires agent_token.",
        inputSchema={
            "type": "object",
            "properties": {
                "ticket_id": {"type": "integer", "description": "Ticket ID"},
                "agent_token": {"type": "string", "description": "Your agent token (required)"},
                "name": {"type": "string"}, "description": {"type": "string"},
                "type": {"type": "string"}, "priority": {"type": "string"},
                "status": {"type": "string"}, "assignee": {"type": "string"},
                "assignee_id": {"type": "integer", "description": "Assignee user ID"},
                "due_date": {"type": "string"},
            },
            "required": ["ticket_id", "agent_token"],
        },
    ),
    types.Tool(
        name="delete_ticket",
        description="Delete a ticket. Requires agent_token.",
        inputSchema={
            "type": "object",
            "properties": {
                "ticket_id": {"type": "integer", "description": "Ticket ID"},
                "agent_token": {"type": "string", "description": "Your agent token (required)"},
            },
            "required": ["ticket_id", "agent_token"],
        },
    ),
    types.Tool(
        name="reorder_tickets",
        description="Reorder tickets across status columns. Requires agent_token.",
        inputSchema={
            "type": "object",
            "properties": {
                "agent_token": {"type": "string", "description": "Your agent token (required)"},
                "items": {"type": "array", "description": "List of {id, status, sort_order} objects"},
            },
            "required": ["agent_token", "items"],
        },
    ),
    types.Tool(
        name="add_comment",
        description="Add a comment to a ticket. Requires agent_token.",
        inputSchema={
            "type": "object",
            "properties": {
                "ticket_id": {"type": "integer"}, "body": {"type": "string"},
                "agent_token": {"type": "string", "description": "Your agent token (required)"},
                "pr_url": {"type": "string"}, "pr_title": {"type": "string"},
            },
            "required": ["ticket_id", "body", "agent_token"],
        },
    ),
    types.Tool(
        name="list_comments",
        description="List comments on a ticket.",
        inputSchema={
            "type": "object",
            "properties": {"ticket_id": {"type": "integer"}},
            "required": ["ticket_id"],
        },
    ),
    types.Tool(
        name="submit_pr_link",
        description="Link a PR to a ticket. Requires agent_token.",
        inputSchema={
            "type": "object",
            "properties": {
                "ticket_id": {"type": "integer"}, "url": {"type": "string"},
                "agent_token": {"type": "string", "description": "Your agent token (required)"},
                "title": {"type": "string"}, "status": {"type": "string"},
            },
            "required": ["ticket_id", "url", "agent_token"],
        },
    ),
    types.Tool(
        name="list_pr_links",
        description="List PR links for a ticket.",
        inputSchema={
            "type": "object",
            "properties": {"ticket_id": {"type": "integer"}},
            "required": ["ticket_id"],
        },
    ),
    types.Tool(
        name="delete_pr_link",
        description="Remove a PR link. Requires agent_token.",
        inputSchema={
            "type": "object",
            "properties": {
                "ticket_id": {"type": "integer"}, "pr_id": {"type": "integer"},
                "agent_token": {"type": "string", "description": "Your agent token (required)"},
            },
            "required": ["ticket_id", "pr_id", "agent_token"],
        },
    ),
    types.Tool(
        name="list_relationships",
        description="List ticket relationships (dependencies, blocks, related).",
        inputSchema={
            "type": "object",
            "properties": {"ticket_id": {"type": "integer"}},
            "required": ["ticket_id"],
        },
    ),
    types.Tool(
        name="add_relationship",
        description="Create a relationship between tickets. Requires agent_token.",
        inputSchema={
            "type": "object",
            "properties": {
                "ticket_id": {"type": "integer"}, "agent_token": {"type": "string", "description": "Your agent token (required)"},
                "related_ticket_id": {"type": "integer"}, "relationship_type": {"type": "string"},
            },
            "required": ["ticket_id", "agent_token", "related_ticket_id"],
        },
    ),
    types.Tool(
        name="remove_relationship",
        description="Remove a ticket relationship. Requires agent_token.",
        inputSchema={
            "type": "object",
            "properties": {
                "ticket_id": {"type": "integer"}, "relationship_id": {"type": "integer"},
                "agent_token": {"type": "string", "description": "Your agent token (required)"},
            },
            "required": ["ticket_id", "relationship_id", "agent_token"],
        },
    ),
    types.Tool(
        name="get_ticket_history",
        description="Get change history for a ticket.",
        inputSchema={
            "type": "object",
            "properties": {"ticket_id": {"type": "integer"}},
            "required": ["ticket_id"],
        },
    ),
    types.Tool(
        name="get_stats",
        description="Get aggregate dashboard stats: inbox count, triage count, my tickets count.",
        inputSchema={
            "type": "object",
            "properties": {"cycle_id": {"type": "integer", "description": "Filter by cycle"}},
        },
    ),
    types.Tool(
        name="list_projects",
        description="List projects with id, name, description, color, git_repo_url, and ticket counts. Read-only.",
        inputSchema={
            "type": "object",
            "properties": {
                "cycle_id": {"type": "integer", "description": "Only return projects attached to this cycle"},
            },
        },
    ),
    types.Tool(
        name="list_cycles",
        description="List cycles with id, title, status, dates, project_ids, and ticket_count. Read-only.",
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {"type": "integer", "description": "Only return cycles attached to this project"},
                "status": {"type": "string", "description": "Filter by cycle status (pending, in_progress, completed, cancelled)"},
            },
        },
    ),
    types.Tool(
        name="create_cycle",
        description="Create a new cycle. Requires agent_token.",
        inputSchema={
            "type": "object",
            "properties": {
                "agent_token": {"type": "string", "description": "Your agent token (required)"},
                "title": {"type": "string", "description": "Cycle title (required)"},
                "description": {"type": "string"},
                "status": {"type": "string", "description": "pending / in_progress / completed / cancelled"},
                "start_date": {"type": "string", "description": "YYYY-MM-DD"},
                "end_date": {"type": "string", "description": "YYYY-MM-DD"},
                "project_ids": {"type": "array", "items": {"type": "integer"}, "description": "Projects to attach to the cycle"},
            },
            "required": ["agent_token", "title"],
        },
    ),
    types.Tool(
        name="update_cycle",
        description="Update a cycle. PATCH semantics — only fields provided are changed. Requires agent_token.",
        inputSchema={
            "type": "object",
            "properties": {
                "agent_token": {"type": "string", "description": "Your agent token (required)"},
                "cycle_id": {"type": "integer", "description": "Cycle ID (required)"},
                "title": {"type": "string"},
                "description": {"type": "string"},
                "status": {"type": "string"},
                "start_date": {"type": "string", "description": "YYYY-MM-DD"},
                "end_date": {"type": "string", "description": "YYYY-MM-DD"},
                "project_ids": {"type": "array", "items": {"type": "integer"}},
            },
            "required": ["agent_token", "cycle_id"],
        },
    ),
]


def call_tool(name: str, arguments: dict) -> str:
    token = arguments.get('agent_token', '')
    tid = arguments.get('ticket_id')

    with get_client(token) as client:
        if name == "list_tickets":
            params = {k: v for k, v in arguments.items()
                      if k in ('cycle_id', 'project_id', 'status', 'assignee', 'assignee_id', 'search') and v}
            if arguments.get('no_cycle'):
                params['no_cycle'] = '1'
            r = client.get(api_url('/tickets'), params=params)
            r.raise_for_status()
            tickets = r.json()
            result = [{'id': t['id'], 'display_id': t['display_id'], 'name': t['name'],
                       'type': t['type'], 'priority': t['priority'], 'status': t['status'],
                       'project_name': t.get('project_name', ''),
                       'assignee': t.get('assignee', ''), 'comment_count': t.get('comment_count', 0),
                       'created_at': t['created_at']} for t in tickets]
            return json.dumps(result, indent=2)

        elif name == "get_ticket":
            r = client.get(api_url(f'/tickets/{tid}'))
            r.raise_for_status()
            return json.dumps(r.json(), indent=2)

        elif name == "create_ticket":
            r = client.post(api_url('/tickets'), json={
                'name': arguments['name'],
                'description': arguments.get('description', ''),
                'type': arguments.get('type', 'feature'),
                'priority': arguments.get('priority', 'medium'),
                'status': arguments.get('status', 'backlog'),
                'project_id': arguments.get('project_id'),
                'cycle_id': arguments.get('cycle_id'),
                'assignee': arguments.get('assignee', ''),
                'assignee_id': arguments.get('assignee_id'),
                'due_date': arguments.get('due_date'),
            })
            r.raise_for_status()
            return json.dumps(r.json(), indent=2)

        elif name == "update_ticket":
            data = {k: v for k, v in arguments.items()
                    if k in ('name', 'description', 'type', 'priority', 'status', 'assignee', 'assignee_id', 'due_date') and v is not None}
            if not data: return json.dumps({"error": "No fields to update"})
            r = client.patch(api_url(f'/tickets/{tid}'), json=data)
            r.raise_for_status()
            return json.dumps(r.json(), indent=2)

        elif name == "delete_ticket":
            r = client.delete(api_url(f'/tickets/{tid}'))
            r.raise_for_status()
            return json.dumps({"deleted": True})

        elif name == "reorder_tickets":
            r = client.put(api_url('/tickets/reorder'),
                          json={'items': arguments['items']})
            r.raise_for_status()
            return json.dumps(r.json(), indent=2)

        elif name == "add_comment":
            data = {'body': arguments['body'], 'author_type': 'agent', 'author_name': 'AI Agent'}
            if arguments.get('pr_url'):
                data['pr_url'] = arguments['pr_url']
                data['pr_title'] = arguments.get('pr_title', '')
            r = client.post(api_url(f'/tickets/{tid}/comments'), json=data)
            r.raise_for_status()
            return json.dumps({"status": "Comment added", "ticket_id": tid})

        elif name == "list_comments":
            r = client.get(api_url(f'/tickets/{tid}/comments'))
            r.raise_for_status()
            return json.dumps(r.json(), indent=2)

        elif name == "submit_pr_link":
            r = client.post(api_url(f'/tickets/{tid}/pr-links'), json={
                'url': arguments['url'],
                'title': arguments.get('title', ''),
                'status': arguments.get('status', 'open'),
            })
            r.raise_for_status()
            return json.dumps({"status": "PR link submitted", "ticket_id": tid})

        elif name == "list_pr_links":
            r = client.get(api_url(f'/tickets/{tid}/pr-links'))
            r.raise_for_status()
            return json.dumps(r.json(), indent=2)

        elif name == "delete_pr_link":
            pid = arguments['pr_id']
            r = client.delete(api_url(f'/tickets/{tid}/pr-links/{pid}'))
            r.raise_for_status()
            return json.dumps({"deleted": True})

        elif name == "list_relationships":
            r = client.get(api_url(f'/tickets/{tid}/relationships'))
            r.raise_for_status()
            return json.dumps(r.json(), indent=2)

        elif name == "add_relationship":
            r = client.post(api_url(f'/tickets/{tid}/relationships'), json={
                'related_ticket_id': arguments['related_ticket_id'],
                'relationship_type': arguments.get('relationship_type', 'related'),
            })
            r.raise_for_status()
            return json.dumps(r.json(), indent=2)

        elif name == "remove_relationship":
            rid = arguments['relationship_id']
            r = client.delete(api_url(f'/tickets/{tid}/relationships/{rid}'))
            r.raise_for_status()
            return json.dumps({"deleted": True})

        elif name == "get_ticket_history":
            r = client.get(api_url(f'/tickets/{tid}/history'))
            r.raise_for_status()
            return json.dumps(r.json(), indent=2)

        elif name == "get_stats":
            params = {}
            if arguments.get('cycle_id'):
                params['cycle_id'] = arguments['cycle_id']
            r = client.get(api_url('/stats'), params=params)
            r.raise_for_status()
            return json.dumps(r.json(), indent=2)

        elif name == "list_projects":
            params = {}
            if arguments.get('cycle_id'):
                params['cycle_id'] = arguments['cycle_id']
            r = client.get(api_url('/projects'), params=params)
            r.raise_for_status()
            return json.dumps(r.json(), indent=2)

        elif name == "list_cycles":
            params = {k: v for k, v in arguments.items()
                      if k in ('project_id', 'status') and v}
            r = client.get(api_url('/cycles'), params=params)
            r.raise_for_status()
            return json.dumps(r.json(), indent=2)

        elif name == "create_cycle":
            data = {k: v for k, v in arguments.items()
                    if k in ('title', 'description', 'status', 'start_date', 'end_date', 'project_ids') and v is not None}
            r = client.post(api_url('/cycles'), json=data)
            r.raise_for_status()
            return json.dumps(r.json(), indent=2)

        elif name == "update_cycle":
            cid = arguments['cycle_id']
            data = {k: v for k, v in arguments.items()
                    if k in ('title', 'description', 'status', 'start_date', 'end_date', 'project_ids') and v is not None}
            if not data:
                return json.dumps({"error": "No fields to update"})
            r = client.put(api_url(f'/cycles/{cid}'), json=data)
            r.raise_for_status()
            return json.dumps(r.json(), indent=2)

        return json.dumps({"error": f"Unknown tool: {name}"})
