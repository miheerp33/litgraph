from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(prefix="/nodes", tags=["nodes"])

@router.post("/", response_model=schemas.NodeRead)
def create_node(node: schemas.NodeCreate, db: Session = Depends(database.get_db)):
    db_node = db.query(models.Node).filter(models.Node.name == node.name).first()
    if db_node:
        raise HTTPException(status_code=400, detail="Node already exists")
    new_node = models.Node(name=node.name, type=node.type)
    db.add(new_node)
    db.commit()
    db.refresh(new_node)
    return new_node

@router.get("/", response_model=list[schemas.NodeRead])
def get_nodes(db: Session = Depends(database.get_db)):
    return db.query(models.Node).all()
