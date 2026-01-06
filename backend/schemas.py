from pydantic import BaseModel, ConfigDict

class NodeBase(BaseModel):
    name: str
    type: str

class NodeCreate(NodeBase):
    book_id: int

class NodeRead(BaseModel):
    id: int
    name: str
    type: str
    book_id: int
    model_config = ConfigDict(from_attributes=True)


class EdgeBase(BaseModel):
    source_id: int
    target_id: int
    relationship_type: str

class EdgeCreate(EdgeBase):
    pass


class EdgeRead(BaseModel):
    id: int
    source_id: int
    target_id: int
    relationship_type: str

    model_config = ConfigDict(from_attributes=True)

class BookBase(BaseModel):
    title: str

class BookCreate(BookBase):
    pass

class BookRead(BookBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class GraphRead(BaseModel):
    book: BookRead
    nodes: list[NodeRead]
    edges: list[EdgeRead]