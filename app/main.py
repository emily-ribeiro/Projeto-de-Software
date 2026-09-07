from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.database import Base, engine
from app.routers import auth_router, tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Tracker API",
    description="API para gerenciamento de tarefas - estudo de caso IA/IDE",
    version="1.0.0",
)

app.include_router(auth_router.router)
app.include_router(tasks.router)


@app.get("/", include_in_schema=False)
def root():
    """Redireciona a rota raiz para a documentação interativa /docs."""
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}
