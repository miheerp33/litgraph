from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(prefix="/graph", tags=["graph"])

@router.get("/")

def get_graph(db: Session = Depends(database.get_db)):
    nodes = db.query(models.Node).all()
    edges = db.query(models.Edge).all()

    edges_data = [schemas.EdgeRead.model_validate(edge) for edge in edges]
    nodes_data = [schemas.NodeRead.model_validate(node) for node in nodes]

    return {"nodes": nodes_data, "edges": edges_data}