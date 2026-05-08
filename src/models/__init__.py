from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import uuid

db = SQLAlchemy()


def utcnow():
    return datetime.now(timezone.utc)


from src.models.cycle import Cycle
from src.models.cycle_project import CycleProject
from src.models.project import Project
from src.models.ticket import Ticket
from src.models.comment import Comment
from src.models.pr_link import PRLink
from src.models.ticket_relationship import TicketRelationship
from src.models.ticket_history import TicketHistory
from src.models.user import User
from src.models.attachment import Attachment
