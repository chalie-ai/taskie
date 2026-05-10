from flask import Blueprint, request, jsonify
from src.services.document_search_service import DocumentSearchService
from src.auth.jwt import optional_auth

search_bp = Blueprint('document_search', __name__)


@search_bp.route('/documents/search', methods=['GET'])
@optional_auth
def search():
    return jsonify(DocumentSearchService.search(
        q=request.args.get('q', ''),
        space=request.args.get('space'),
        project_id=request.args.get('project_id', type=int),
        tag=request.args.get('tag'),
        limit=request.args.get('limit', default=20, type=int),
    ))
