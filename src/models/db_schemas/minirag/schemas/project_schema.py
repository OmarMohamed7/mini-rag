from datetime import datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import DateTime
from .minirag_base_schema import SQLAlchemyBase
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import func


class ProjectSchema(SQLAlchemyBase):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    project_id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        nullable=False,
        unique=True,
        primary_key=True,
    )

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
