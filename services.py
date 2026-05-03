from models import db, Cycle, CycleProject, Project, Ticket, Comment, PRLink, TicketRelationship, TicketHistory, User
from datetime import datetime, timezone


class Services:
    @staticmethod
    def ticker():
        """Next display ID counter. In production this would use an auto-incrementing sequence."""
        latest = Ticket.query.order_by(Ticket.id.desc()).first()
        num = (latest.id + 1) if latest else 1
        return f"TKT-{num:02d}"

    # ── Cycles ──

    @staticmethod
    def list_cycles():
        cycles = Cycle.query.order_by(Cycle.created_at.desc()).all()
        result = []
        for c in cycles:
            total = c.tickets.count()
            done = c.tickets.filter(Ticket.status.in_(['done', 'cancel'])).count()
            result.append({
                'id': c.id, 'title': c.title, 'description': c.description,
                'status': c.status, 'start_date': str(c.start_date) if c.start_date else None,
                'end_date': str(c.end_date) if c.end_date else None,
                'active': c.status == 'in_progress',
                'total': total, 'done': done,
                'created_at': str(c.created_at), 'updated_at': str(c.updated_at),
            })
        return result

    @staticmethod
    def get_cycle(cycle_id):
        c = db.session.get(Cycle, cycle_id)
        if not c:
            return None
        total = c.tickets.count()
        done = c.tickets.filter(Ticket.status.in_(['done', 'cancel'])).count()
        return {
            'id': c.id, 'title': c.title, 'description': c.description,
            'status': c.status, 'start_date': str(c.start_date) if c.start_date else None,
            'end_date': str(c.end_date) if c.end_date else None,
            'active': c.status == 'in_progress',
            'total': total, 'done': done,
            'projects': [{'id': p.id, 'name': p.name, 'color': p.color} for p in c.projects],
            'created_at': str(c.created_at), 'updated_at': str(c.updated_at),
        }

    @staticmethod
    def create_cycle(data):
        c = Cycle(
            title=data['title'],
            description=data.get('description'),
            status=data.get('status', 'pending'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
        )
        db.session.add(c)
        db.session.commit()
        return Services.get_cycle(c.id)

    @staticmethod
    def update_cycle(cycle_id, data):
        c = db.session.get(Cycle, cycle_id)
        if not c:
            return None
        for field in ['title', 'description', 'status', 'start_date', 'end_date']:
            if field in data:
                setattr(c, field, data[field])
        db.session.commit()
        return Services.get_cycle(c.id)

    @staticmethod
    def delete_cycle(cycle_id):
        c = db.session.get(Cycle, cycle_id)
        if not c:
            return False
        db.session.delete(c)
        db.session.commit()
        return True

    # ── Projects ──

    @staticmethod
    def list_projects(cycle_id=None):
        q = Project.query
        if cycle_id:
            q = q.join(CycleProject).filter(CycleProject.cycle_id == cycle_id)
        projects = q.order_by(Project.name).all()
        return [{
            'id': p.id, 'name': p.name, 'location': p.location,
            'description': p.description, 'agent_instructions': p.agent_instructions,
            'color': p.color, 'git_repo_url': p.git_repo_url,
            'ticket_count': p.tickets.count(),
            'open_count': p.tickets.filter(Ticket.status.notin_(['done', 'cancel'])).count(),
            'progress_count': p.tickets.filter(Ticket.status == 'progress').count(),
            'created_at': str(p.created_at), 'updated_at': str(p.updated_at),
        } for p in projects]

    @staticmethod
    def get_project(project_id):
        p = db.session.get(Project, project_id)
        if not p:
            return None
        return {
            'id': p.id, 'name': p.name, 'location': p.location,
            'description': p.description, 'agent_instructions': p.agent_instructions,
            'color': p.color, 'git_repo_url': p.git_repo_url,
            'ticket_count': p.tickets.count(),
            'open_count': p.tickets.filter(Ticket.status.notin_(['done', 'cancel'])).count(),
            'progress_count': p.tickets.filter(Ticket.status == 'progress').count(),
            'created_at': str(p.created_at), 'updated_at': str(p.updated_at),
        }

    @staticmethod
    def create_project(data):
        p = Project(
            name=data['name'],
            location=data.get('location'),
            description=data.get('description'),
            agent_instructions=data.get('agent_instructions'),
            color=data.get('color', 'oklch(0.55 0.15 265)'),
            git_repo_url=data.get('git_repo_url'),
        )
        db.session.add(p)
        db.session.commit()
        return Services.get_project(p.id)

    @staticmethod
    def update_project(project_id, data):
        p = db.session.get(Project, project_id)
        if not p:
            return None
        for field in ['name', 'location', 'description', 'agent_instructions', 'color', 'git_repo_url']:
            if field in data:
                setattr(p, field, data[field])
        db.session.commit()
        return Services.get_project(p.id)

    @staticmethod
    def delete_project(project_id):
        p = db.session.get(Project, project_id)
        if not p:
            return False
        db.session.delete(p)
        db.session.commit()
        return True

    # ── Tickets ──

    @staticmethod
    def list_tickets(cycle_id=None, project_id=None, status=None, assignee=None, search=None):
        q = Ticket.query
        if cycle_id:
            q = q.filter(Ticket.cycle_id == cycle_id)
        if project_id:
            q = q.filter(Ticket.project_id == project_id)
        if status:
            q = q.filter(Ticket.status == status)
        if assignee:
            q = q.filter(Ticket.assignee == assignee)
        if search:
            like = f'%{search}%'
            q = q.filter(
                db.or_(
                    Ticket.name.ilike(like),
                    Ticket.description.ilike(like),
                    Ticket.display_id.ilike(like),
                )
            )
        tickets = q.order_by(Ticket.sort_order, Ticket.created_at.desc()).all()
        return [_serialize_ticket(t) for t in tickets]

    @staticmethod
    def get_ticket(ticket_id):
        t = Ticket.query.get(ticket_id)
        if not t:
            return None
        return _serialize_ticket(t, include_details=True)

    @staticmethod
    def create_ticket(data):
        due_date = data.get('due_date')
        if isinstance(due_date, str) and due_date:
            due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
        elif due_date == '':
            due_date = None
        max_order = db.session.query(db.func.max(Ticket.sort_order)).filter(Ticket.status == data.get('status', 'backlog')).scalar() or 0
        t = Ticket(
            display_id=Services.ticker(),
            name=data['name'],
            description=data.get('description'),
            type=data.get('type', 'feature'),
            priority=data.get('priority', 'none'),
            status=data.get('status', 'backlog'),
            project_id=data.get('project_id'),
            cycle_id=data.get('cycle_id'),
            assignee=data.get('assignee'),
            due_date=due_date,
            sort_order=max_order + 1,
        )
        db.session.add(t)
        db.session.commit()
        return Services.get_ticket(t.id)

    @staticmethod
    def update_ticket(ticket_id, data):
        t = Ticket.query.get(ticket_id)
        if not t:
            return None
        author = data.get('author_name', 'Dylan')
        allowed = ['name', 'description', 'type', 'priority', 'status', 'project_id', 'cycle_id', 'assignee', 'due_date', 'sort_order']
        for field in allowed:
            if field in data:
                old_val = getattr(t, field)
                new_val = data[field]
                if field == 'due_date' and isinstance(new_val, str):
                    if new_val:
                        new_val = datetime.strptime(new_val, '%Y-%m-%d').date()
                    else:
                        new_val = None
                if str(old_val) != str(new_val):
                    setattr(t, field, new_val)
                    h = TicketHistory(
                        ticket_id=ticket_id, author_name=author,
                        field_name=field, old_value=str(old_val) if old_val is not None else None,
                        new_value=str(new_val),
                    )
                    db.session.add(h)
        db.session.commit()
        return Services.get_ticket(ticket_id)

    @staticmethod
    def reorder_tickets(items):
        """Batch update sort_order and status. items = [{id, status, sort_order}, ...]"""
        for item in items:
            t = Ticket.query.get(item['id'])
            if t:
                if 'status' in item:
                    t.status = item['status']
                if 'sort_order' in item:
                    t.sort_order = item['sort_order']
        db.session.commit()
        return {'ok': True}

    @staticmethod
    def delete_ticket(ticket_id):
        t = Ticket.query.get(ticket_id)
        if not t:
            return False
        db.session.delete(t)
        db.session.commit()
        return True

    # ── Comments ──

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
        c = Comment(
            ticket_id=ticket_id,
            body=data['body'],
            author_type=data.get('author_type', 'human'),
            author_name=data.get('author_name', 'Dylan'),
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

        db.session.commit()
        return Services.list_comments(ticket_id)

    # ── PR Links ──

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
        db.session.commit()
        return {'id': pr.id, 'url': pr.url, 'title': pr.title, 'status': pr.status, 'created_at': str(pr.created_at)}

    @staticmethod
    def delete_pr_link(pr_id):
        pr = PRLink.query.get(pr_id)
        if not pr:
            return False
        db.session.delete(pr)
        db.session.commit()
        return True


    # ── Ticket Relationships ──

    @staticmethod
    def list_relationships(ticket_id):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return None
        return [{
            'id': r.id, 'ticket_id': r.ticket_id, 'related_ticket_id': r.related_ticket_id,
            'relationship_type': r.relationship_type,
            'related_ticket_display_id': r.related_ticket.display_id,
            'related_ticket_name': r.related_ticket.name,
            'related_ticket_status': r.related_ticket.status,
            'created_at': str(r.created_at),
        } for r in ticket.relationships]

    @staticmethod
    def add_relationship(ticket_id, data):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return None
        rel_type = data.get('relationship_type')
        if rel_type not in ('related', 'blocked_by', 'blocks'):
            return {'error': "relationship_type must be 'related', 'blocked_by', or 'blocks'"}
        related_id = data.get('related_ticket_id')
        if not related_id or not Ticket.query.get(related_id):
            return {'error': 'related_ticket_id is invalid'}
        if ticket_id == related_id:
            return {'error': 'Cannot relate a ticket to itself'}
        existing = TicketRelationship.query.filter_by(
            ticket_id=ticket_id, related_ticket_id=related_id, relationship_type=rel_type).first()
        if existing:
            return {'error': 'Relationship already exists'}
        r = TicketRelationship(
            ticket_id=ticket_id,
            related_ticket_id=related_id,
            relationship_type=rel_type,
        )
        db.session.add(r)
        db.session.commit()
        return Services.list_relationships(ticket_id)

    @staticmethod
    def remove_relationship(relationship_id):
        r = TicketRelationship.query.get(relationship_id)
        if not r:
            return False
        db.session.delete(r)
        db.session.commit()
        return True

    # ── Ticket History ──

    @staticmethod
    def get_ticket_history(ticket_id):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return None
        return [{
            'id': h.id, 'author_name': h.author_name,
            'field_name': h.field_name, 'old_value': h.old_value,
            'new_value': h.new_value, 'created_at': str(h.created_at),
        } for h in ticket.history_entries]


    # ── Users ──

    @staticmethod
    def list_users():
        users = User.query.order_by(User.name).all()
        return [_serialize_user(u) for u in users]

    @staticmethod
    def get_user(user_id):
        u = db.session.get(User, user_id)
        if not u:
            return None
        return _serialize_user(u)

    @staticmethod
    def create_user(data):
        if not data.get('email'):
            return {'error': 'email is required'}
        if User.query.filter_by(email=data['email']).first():
            return {'error': 'A user with that email already exists'}
        u = User(
            name=data['name'],
            email=data['email'],
            role=data.get('role', 'member'),
            avatar_color=data.get('avatar_color', 'oklch(0.55 0.15 265)'),
        )
        db.session.add(u)
        db.session.commit()
        return _serialize_user(u)

    @staticmethod
    def update_user(user_id, data):
        u = db.session.get(User, user_id)
        if not u:
            return None
        for field in ['name', 'email', 'role', 'avatar_color']:
            if field in data:
                setattr(u, field, data[field])
        db.session.commit()
        return _serialize_user(u)

    @staticmethod
    def delete_user(user_id):
        u = db.session.get(User, user_id)
        if not u:
            return False
        db.session.delete(u)
        db.session.commit()
        return True


def _serialize_user(u):
    return {
        'id': u.id, 'name': u.name, 'email': u.email,
        'role': u.role, 'avatar_color': u.avatar_color,
        'created_at': str(u.created_at), 'updated_at': str(u.updated_at),
    }


def _serialize_ticket(t, include_details=False):
    base = {
        'id': t.id, 'display_id': t.display_id, 'name': t.name,
        'description': t.description, 'type': t.type, 'priority': t.priority,
        'status': t.status, 'project_id': t.project_id, 'cycle_id': t.cycle_id,
        'assignee': t.assignee,
        'due_date': str(t.due_date) if t.due_date else None,
        'sort_order': t.sort_order,
        'comment_count': t.comments.count(),
        'created_at': str(t.created_at), 'updated_at': str(t.updated_at),
    }
    if t.project:
        base['project_name'] = t.project.name
        base['project_color'] = t.project.color

    if include_details:
        base['comments'] = [{
            'id': c.id, 'body': c.body, 'author_type': c.author_type,
            'author_name': c.author_name, 'created_at': str(c.created_at),
            'pr_link': {
                'id': c.pr_link.id, 'url': c.pr_link.url, 'title': c.pr_link.title,
                'status': c.pr_link.status,
            } if c.pr_link else None,
        } for c in t.comments.all()]
        base['pr_links'] = [{
            'id': p.id, 'url': p.url, 'title': p.title, 'status': p.status,
            'created_at': str(p.created_at),
        } for p in t.pr_links.all()]
        base['relationships'] = Services.list_relationships(t.id)
        base['history'] = Services.get_ticket_history(t.id)

    return base
