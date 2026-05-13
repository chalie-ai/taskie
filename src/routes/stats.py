from flask import Blueprint, request, jsonify
from src.models import Ticket

stats_bp = Blueprint('stats', __name__)


@stats_bp.route('/stats', methods=['GET'])
def get_stats():
    cycle_id = request.args.get('cycle_id', type=int)
    q = Ticket.query
    if cycle_id:
        q = q.filter(Ticket.cycle_id == cycle_id)
    inbox = q.filter(Ticket.status.notin_(['done', 'cancel'])).count()
    triage = q.filter(Ticket.cycle_id.is_(None)).count()
    return jsonify({
        'inbox': inbox,
        'triage': triage,
        'mine': q.filter(Ticket.assignee == 'dy', Ticket.status.notin_(['done', 'cancel'])).count(),
    })
