"""Register MCP tools against the server instance."""


def register_tools(server, list_tickets_fn, get_ticket_fn, add_comment_fn, submit_pr_link_fn):
    server.tool()(list_tickets_fn)
    server.tool()(get_ticket_fn)
    server.tool()(add_comment_fn)
    server.tool()(submit_pr_link_fn)
