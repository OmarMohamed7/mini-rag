from sqlalchemy.orm import relationship
from .minirag_base_schema import SQLAlchemyBase
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from sqlalchemy.types import DateTime
from sqlalchemy import func


class DataChunkSchema(SQLAlchemyBase):
    __tablename__ = "chunks"
    id = Column(Integer, primary_key=True)
    chunk_id = Column(
        UUID(as_uuid=True), default=uuid.uuid4, nullable=False, unique=True
    )
    chunk_text = Column(String, nullable=False)
    chunk_metadata = Column(JSONB, nullable=False)
    chunk_order = Column(Integer, nullable=False)

    chunk_project_id = Column(
        Integer, ForeignKey("projects.project_id"), nullable=False, index=True
    )
    chunk_asset_id = Column(
        Integer, ForeignKey("assets.asset_id"), nullable=False, index=True
    )

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    project = relationship("ProjectSchema", back_populates="chunks")
    asset = relationship("AssetSchema", back_populates="chunks")
