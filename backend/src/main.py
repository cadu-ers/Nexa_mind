from fastapi import FastAPI
from .routes import usuario, disciplina, material

app = FastAPI()

@app.get("/")
def home():
    return {"msg": "NexaMind API rodando"}

app.include_router(usuario.router)
app.include_router(disciplina.router)
app.include_router(material.router)