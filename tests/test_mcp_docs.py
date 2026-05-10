def test_all_doc_tools_registered():
    from src.mcp.tools import TOOL_DEFS
    names = {t.name for t in TOOL_DEFS}
    expected = {
        'list_folders', 'create_folder', 'update_folder', 'delete_folder',
        'list_documents', 'get_document', 'create_document',
        'update_document_metadata', 'save_document', 'delete_document',
        'search_documents',
        'list_document_versions', 'get_document_version', 'rollback_document',
        'list_tags', 'create_tag', 'delete_tag',
        'link_document_to_ticket', 'unlink_document_from_ticket',
        'list_linked_tickets',
        'upload_document_attachment', 'list_document_attachments',
    }
    missing = expected - names
    assert not missing, f"Missing MCP tools: {missing}"
