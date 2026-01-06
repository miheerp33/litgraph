from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from ..database import get_db

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=schemas.BookRead)
def create_book(book: schemas.BookCreate, db: Session = Depends(database.get_db)):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.get("/", response_model=list[schemas.BookRead])
def list_books(db: Session = Depends(database.get_db)):
    return db.query(models.Book).all()

@router.get("/{book_id}/graph", response_model=schemas.GraphRead)
def get_book_graph(book_id: int, db: Session = Depends(database.get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    nodes = (
        db.query(models.Node)
        .filter(models.Node.book_id == book_id)
        .all()
    )

    node_ids = [n.id for n in nodes]

    edges = (
        db.query(models.Edge)
        .filter(models.Edge.source_id.in_(node_ids))
        .filter(models.Edge.target_id.in_(node_ids))
        .all()
    )

    return {"book": book, "nodes": nodes, "edges": edges}
@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(database.get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return