def register_tools(server, tool_fns):
    for fn in tool_fns:
        server.tool()(fn)
