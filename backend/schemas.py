from pydantic import BaseModel, ConfigDict

class NodeBase(BaseModel):
    name: str
    type: str

class NodeCreate(NodeBase):
    pass

class NodeRead(BaseModel):
    id: int
    name: str
    type: str

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
