from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _get_owned_task(task_id: int, db: Session, user: models.User) -> models.Task:
    """Busca uma tarefa pelo ID e garante que ela pertence ao usuário logado."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )
    return task


@router.post("/", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Cria uma nova tarefa associada ao usuário autenticado."""
    task = models.Task(**task_in.model_dump(), owner_id=current_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/", response_model=List[schemas.TaskOut])
def list_tasks(
    status_filter: Optional[models.StatusEnum] = None,
    priority: Optional[models.PriorityEnum] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Lista apenas as tarefas pertencentes ao usuário autenticado, com suporte a filtros."""
    query = db.query(models.Task).filter(models.Task.owner_id == current_user.id)
    if status_filter:
        query = query.filter(models.Task.status == status_filter)
    if priority:
        query = query.filter(models.Task.priority == priority)
    if tag:
        query = query.filter(models.Task.tag == tag)
    if search:
        query = query.filter(models.Task.title.ilike(f"%{search}%"))
    return query.order_by(models.Task.created_at.desc()).all()


@router.get("/{task_id}", response_model=schemas.TaskOut)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Retorna os detalhes de uma tarefa específica do usuário autenticado."""
    return _get_owned_task(task_id, db, current_user)


@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int,
    task_in: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Atualiza parcialmente os campos de uma tarefa existente."""
    task = _get_owned_task(task_id, db, current_user)
    for field, value in task_in.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Remove uma tarefa do usuário autenticado."""
    task = _get_owned_task(task_id, db, current_user)
    db.delete(task)
    db.commit()
    return None
