from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError
from .database import Base


class Node(Base):
    __tablename__ = "nodes"
    __table_args__ = (
        UniqueConstraint("book_id", "name", name="uq_nodes_book_id_name"),
    )
    id = Column(Integer, primary_key=True, index=True)


    name = Column(String, nullable=False)
    type = Column(String, nullable=False)

    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)


    # relationships

    book = relationship(
        "Book", back_populates="nodes"
    )
    outgoing_edges = relationship(
        "Edge", back_populates="source", foreign_keys="Edge.source_id", passive_deletes=True,
    )
    incoming_edges = relationship(
        "Edge", back_populates="target", foreign_keys="Edge.target_id", passive_deletes=True,
    )



class Edge(Base):
    __tablename__ = "edges"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("nodes.id", ondelete="CASCADE"), nullable=False)
    target_id = Column(Integer, ForeignKey("nodes.id", ondelete="CASCADE"), nullable=False)
    relationship_type = Column(String, nullable=False)

    source = relationship("Node", back_populates="outgoing_edges", foreign_keys=[source_id])
    target = relationship("Node", back_populates="incoming_edges", foreign_keys=[target_id])

    __table_args__ = (
        UniqueConstraint(
            "source_id",
            "target_id",
            "relationship_type",
            name="uq_edge_unique"
        ),
    )

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)

    nodes = relationship("Node", back_populates="book", cascade="all, delete-orphan", passive_deletes=True,)