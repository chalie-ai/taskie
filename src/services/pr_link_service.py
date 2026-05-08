from src.models import db, Ticket, PRLink
from src.services.history_service import HistoryService


class PRLinkService:

    @staticmethod
    def list_pr_links(ticket_id):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return None
        return [{
            'id': p.id, 'url': p.url, 'title': p.title, 'status': p.status,
            'comment_id': p.comment_id, 'created_at': str(p.created_at),
        } for p in ticket.pr_links.all()]

    @staticmethod
    def add_pr_link(ticket_id, data):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return None
        pr = PRLink(
            ticket_id=ticket_id,
            url=data['url'],
            title=data.get('title'),
            status=data.get('status', 'open'),
        )
        db.session.add(pr)
        HistoryService.log(ticket_id, 'pr_linked', None, pr.title or pr.url)
        db.session.commit()
        return {'id': pr.id, 'url': pr.url, 'title': pr.title,
                'status': pr.status, 'created_at': str(pr.created_at)}

    @staticmethod
    def delete_pr_link(pr_id):
        pr = PRLink.query.get(pr_id)
        if not pr:
            return False
        HistoryService.log(pr.ticket_id, 'pr_removed', pr.title or pr.url, None)
        db.session.delete(pr)
        db.session.commit()
        return True
