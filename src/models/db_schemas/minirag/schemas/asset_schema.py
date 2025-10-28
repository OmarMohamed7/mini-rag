from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import DateTime
from .minirag_base_schema import SQLAlchemyBase
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime
from sqlalchemy import func


class AssetSchema(SQLAlchemyBase):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True)
    asset_id = Column(
        UUID(as_uuid=True), default=uuid.uuid4, nullable=False, unique=True
    )
    asset_name = Column(String, nullable=False)
    asset_type = Column(String, nullable=False, index=True)
    asset_size = Column(Float, nullable=False)
    asset_config = Column(JSONB, nullable=False)

    asset_project_id = Column(
        Integer, ForeignKey("projects.id"), nullable=False, index=True
    )

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    project = relationship("ProjectSchema", back_populates="assets", lazy="joined")
