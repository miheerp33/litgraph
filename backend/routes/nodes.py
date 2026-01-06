from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends


router = APIRouter(prefix="/nodes", tags=["nodes"])

@router.post("/", response_model=schemas.NodeRead)
def create_node(node: schemas.NodeCreate, db: Session = Depends(database.get_db)):
    # app-level validation (nice error message)
    existing = db.query(models.Node).filter(
        models.Node.name == node.name,
        models.Node.book_id == node.book_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Node already exists for this book")

    new_node = models.Node(
        name=node.name,
        type=node.type,
        book_id=node.book_id,   # IMPORTANT
    )
    db.add(new_node)

    try:
        database.commit_or_rollback(db)
    except IntegrityError:
        # DB-level fallback (in case race condition or constraint differs)
        raise HTTPException(status_code=400, detail="Invalid node data (constraint violation)")

    db.refresh(new_node)
    return new_node

@router.get("/", response_model=list[schemas.NodeRead])
def get_nodes(db: Session = Depends(database.get_db)):
    nodes = db.query(models.Node).all()
    print("DEBUG →", nodes)
    return nodes

@router.put("/{id}", response_model=schemas.NodeRead)
def update_node(id: int, updated_node: schemas.NodeCreate, db: Session = Depends(database.get_db)):
    node = db.query(models.Node).filter(models.Node.id == id).first()
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")

    node.name = updated_node.name
    node.type = updated_node.type
    node.book_id = updated_node.book_id  # if you allow changing it; otherwise remove this line

    try:
        database.commit_or_rollback(db)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Update violates a constraint (maybe duplicate node name in this book)")

    db.refresh(node)
    return node

@router.delete("/{id}", status_code=204)
def delete_node(id: int, db: Session = Depends(database.get_db)):
    node = db.query(models.Node).filter(models.Node.id == id).first()
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    db.delete(node)
    db.commit()
    return 