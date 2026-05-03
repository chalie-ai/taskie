from src.models import db, Cycle, Ticket


class CycleService:

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
        return CycleService.get_cycle(c.id)

    @staticmethod
    def update_cycle(cycle_id, data):
        c = db.session.get(Cycle, cycle_id)
        if not c:
            return None
        for field in ['title', 'description', 'status', 'start_date', 'end_date']:
            if field in data:
                setattr(c, field, data[field])
        db.session.commit()
        return CycleService.get_cycle(c.id)

    @staticmethod
    def delete_cycle(cycle_id):
        c = db.session.get(Cycle, cycle_id)
        if not c:
            return False
        db.session.delete(c)
        db.session.commit()
        return True
