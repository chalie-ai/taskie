from flask import g, has_request_context
from src.models import db, Ticket, Comment, PRLink
from src.services.history_service import HistoryService


class CommentService:

    @staticmethod
    def list_comments(ticket_id):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return None
        return [{
            'id': c.id, 'body': c.body, 'author_type': c.author_type,
            'author_name': c.author_name, 'created_at': str(c.created_at),
            'pr_link': {
                'id': c.pr_link.id, 'url': c.pr_link.url, 'title': c.pr_link.title,
                'status': c.pr_link.status,
            } if c.pr_link else None,
        } for c in ticket.comments.all()]

    @staticmethod
    def add_comment(ticket_id, data):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return None
        author_name = data.get('author_name')
        author_type = data.get('author_type', 'human')
        if not author_name and has_request_context():
            author_name = getattr(g, 'user_name', None)
        if not author_name:
            author_name = 'Anonymous'
        c = Comment(
            ticket_id=ticket_id,
            body=data['body'],
            author_type=author_type,
            author_name=author_name,
        )
        db.session.add(c)
        db.session.flush()

        if data.get('pr_url'):
            pr = PRLink(
                ticket_id=ticket_id,
                comment_id=c.id,
                url=data['pr_url'],
                title=data.get('pr_title'),
                status=data.get('pr_status', 'open'),
            )
            db.session.add(pr)
            HistoryService.log_ticket(ticket_id, 'pr_linked', None,
                                      data.get('pr_title') or data['pr_url'],
                                      author_name=author_name)

        # First 80 chars are enough for the activity preview; the comment
        # itself remains the source of truth.
        preview = (c.body or '').strip().splitlines()[0][:80] if c.body else ''
        HistoryService.log_ticket(ticket_id, 'comment_added', None, preview,
                                  author_name=author_name)

        db.session.commit()
        return CommentService.list_comments(ticket_id)
