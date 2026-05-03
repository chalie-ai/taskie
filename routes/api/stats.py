from flask import Blueprint, request, jsonify
from services import Services

# Shared stats endpoint for dashboard counts
stats_bp = Blueprint('stats', __name__)


@stats_bp.route('/stats', methods=['GET'])
def get_stats():
    cycle_id = request.args.get('cycle_id', type=int)
    from models import Ticket
    q = Ticket.query
    if cycle_id:
        q = q.filter(Ticket.cycle_id == cycle_id)
    inbox = q.filter(Ticket.status.notin_(['done', 'cancel'])).count()
    triage = q.filter(Ticket.status == 'backlog').count()
    return jsonify({
        'inbox': inbox,
        'triage': triage,
        'mine': q.filter(Ticket.assignee == 'dy', Ticket.status.notin_(['done', 'cancel'])).count(),
    })
