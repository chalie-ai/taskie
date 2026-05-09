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
from src.models.activity_log import ActivityLog
# Deprecated alias kept for one release; remove in v0.4.0 once all callers
# import ActivityLog directly. See src/services/history_service.py for the
# matching ``log(ticket_id, ...)`` compat shim.
TicketHistory = ActivityLog
from src.models.user import User
from src.models.attachment import Attachment
from src.models.folder import Folder
from src.models.document_version import DocumentVersion
from src.models.document import Document
