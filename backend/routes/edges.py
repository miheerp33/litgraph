from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from  .. database import handle_integrity_error

router = APIRouter(prefix="/edges", tags=["edges"])

@router.post("/", response_model=schemas.EdgeRead)
def create_edge(edge: schemas.EdgeCreate, db: Session = Depends(database.get_db)):
    source = db.query(models.Node).filter(models.Node.id == edge.source_id).first()
    target = db.query(models.Node).filter(models.Node.id == edge.target_id).first()

    if not source or not target:
        raise HTTPException(status_code=400, detail="Invalid source or target ID")

    if source.book_id != target.book_id:
        raise HTTPException(status_code=400, detail="Source and target must be in the same book")

    if edge.source_id == edge.target_id:
        raise HTTPException(status_code=400, detail="No self-edges allowed")

    new_edge = models.Edge(
        source_id=edge.source_id,
        target_id=edge.target_id,
        relationship_type=edge.relationship_type,
    )
    db.add(new_edge)

    try:
        database.commit_or_rollback(db)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Edge violates a constraint (maybe duplicate edge)")

    db.refresh(new_edge)
    return new_edge

@router.get("/", response_model=list[schemas.EdgeRead])
def get_edges(db: Session = Depends(database.get_db)):
    return db.query(models.Edge).all()

@router.put("/", response_model=schemas.EdgeRead)
def update_edge(id: int, updated_edge: schemas.EdgeCreate, db: Session = Depends(database.get_db)):
    edge = db.query(models.Edge).filter(models.Edge.id == id).first()
    if not edge:
        raise HTTPException(status_code=404, detail="Edge not found")
    
    validate_edge(
        db,
        edge.source_id,
        edge.target_id,
        edge.relationship_type,
        edge_id_to_ignore=id,
    )
    edge.source_id = updated_edge.source_id
    edge.target_id = updated_edge.target_id
    edge.relationship_type = updated_edge.relationship_type

    db.commit()
    db.refresh(edge)
    return edge

@router.delete("/", status_code=204)
def delete_edge(id: int, db: Session = Depends(database.get_db)):
    edge = db.query(models.Edge).filter(models.Edge.id == id).first()
    if not edge:
        raise HTTPException(status_code=404, detail="Edge not found")
    
    db.delete(edge)
    db.commit()
    return

def validate_edge(db: Session, source_id: int, target_id: int, relationship_type: str, *, edge_id_to_ignore: int | None = None):
    if source_id == target_id:
        raise HTTPException(status_code=400, detail="edge cannot connect a node to itself")
    
    source = db.query(models.Node).filter(models.Node.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source node not found")
    
    target = db.query(models.Node).filter(models.Node.id == target_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Target node not found")
    
    if source.book_id != target.book_id:
        raise HTTPException(status_code=400, detail="Source and target must be in same book")
    
    q = db.query(models.Edge).filter(
        models.Edge.source_id == source_id,
        models.Edge.target_id == target_id,
        models.Edge.relationship_type == relationship_type,
    )
    if edge_id_to_ignore is not None:
        q = q.filter(models.Edge.id != edge_id_to_ignore)
    if q.first():
        raise HTTPException(status_code=400, detail="edge already exists")
    
    return source.book_id
