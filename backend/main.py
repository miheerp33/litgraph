from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from . import models
from .routes import nodes, edges, graph, books

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(nodes.router)
app.include_router(edges.router)
app.include_router(graph.router)
app.include_router(books.router)
@app.get("/")
def root():
    return {"message": "LitGraph backend running!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

