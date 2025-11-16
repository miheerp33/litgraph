from fastapi import FastAPI
from .database import Base, engine
from . import models
from .routes import nodes, edges, graph

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(nodes.router)
app.include_router(edges.router)
app.include_router(graph.router)
@app.get("/")
def root():
    return {"message": "LitGraph backend running!"}
