from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(prefix="/edges", tags=["edges"])

@router.post("/", response_model=schemas.EdgeRead)
def create_edge(edge: schemas.EdgeCreate, db: Session = Depends(database.get_db)):
    source = db.query(models.Node).filter(models.Node.id == edge.source_id).first()
    target = db.query(models.Node).filter(models.Node.id == edge.target_id).first()
    if not source or not target:
        raise HTTPException(status_code=400, detail="Invalid source or target ID")

    new_edge = models.Edge(
        source_id=edge.source_id,
        target_id=edge.target_id,
        relationship_type=edge.relationship_type,
    )
    db.add(new_edge)
    db.commit()
    db.refresh(new_edge)
    return new_edge

@router.get("/", response_model=list[schemas.EdgeRead])
def get_edges(db: Session = Depends(database.get_db)):
    return db.query(models.Edge).all()
