from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)  # e.g. "character", "theme", "idea"

    # relationships
    outgoing_edges = relationship(
        "Edge", back_populates="source", foreign_keys="Edge.source_id"
    )
    incoming_edges = relationship(
        "Edge", back_populates="target", foreign_keys="Edge.target_id"
    )

class Edge(Base):
    __tablename__ = "edges"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("nodes.id"), nullable=False)
    target_id = Column(Integer, ForeignKey("nodes.id"), nullable=False)
    relationship_type = Column(String, nullable=False)

    source = relationship("Node", back_populates="outgoing_edges", foreign_keys=[source_id])
    target = relationship("Node", back_populates="incoming_edges", foreign_keys=[target_id])
