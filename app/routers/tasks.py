from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_owned_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> models.Task:
    """
    Dependência reutilizável do FastAPI que recupera uma tarefa pelo ID
    e valida se ela pertence ao usuário atualmente autenticado.

    Lança:
        HTTPException 404: Se a tarefa não existir no banco.
        HTTPException 403: Se a tarefa pertencer a outro usuário.
    """
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    if task.owner_id != current_user.id:
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
    """
    Cria uma nova tarefa no sistema associada ao usuário autenticado.

    Args:
        task_in (TaskCreate): Dados da tarefa (título, descrição, prioridade, status, due_date, tag).
        db (Session): Sessão ativa do banco de dados (injetada via get_db).
        current_user (User): Usuário logado recuperado via token JWT (injetado via get_current_user).

    Returns:
        TaskOut: Objeto da tarefa criada com id, owner_id e created_at preenchidos.
    """
    task = models.Task(**task_in.model_dump(), owner_id=current_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/", response_model=List[schemas.TaskOut])
def list_tasks(
    status: Optional[models.StatusEnum] = None,
    status_filter: Optional[models.StatusEnum] = None,
    priority: Optional[models.PriorityEnum] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Lista todas as tarefas pertencentes ao usuário autenticado.

    Suporta parâmetros de busca e filtros combináveis:
    - **status / status_filter**: Filtra por estado da tarefa (`pending`, `in_progress`, `done`).
    - **priority**: Filtra por prioridade (`low`, `medium`, `high`).
    - **tag**: Filtra por tag exata.
    - **search**: Busca textual parcial no título (case-insensitive).

    Returns:
        List[TaskOut]: Lista de tarefas ordenadas da mais recente para a mais antiga.
    """
    query = db.query(models.Task).filter(models.Task.owner_id == current_user.id)

    target_status = status or status_filter
    if target_status:
        query = query.filter(models.Task.status == target_status)
    if priority:
        query = query.filter(models.Task.priority == priority)
    if tag:
        query = query.filter(models.Task.tag == tag)
    if search:
        query = query.filter(models.Task.title.ilike(f"%{search}%"))

    return query.order_by(models.Task.created_at.desc()).all()


@router.get("/{task_id}", response_model=schemas.TaskOut)
def get_task(task: models.Task = Depends(get_owned_task)):
    """
    Recupera os detalhes de uma tarefa específica pertencente ao usuário logado.

    Args:
        task (Task): Objeto da tarefa validado e injetado pela dependência get_owned_task.

    Returns:
        TaskOut: Dados completos da tarefa.
    """
    return task


@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_in: schemas.TaskUpdate,
    task: models.Task = Depends(get_owned_task),
    db: Session = Depends(get_db),
):
    """
    Atualiza parcialmente os campos de uma tarefa existente pertencente ao usuário.

    Args:
        task_in (TaskUpdate): Campos a serem atualizados (apenas valores fornecidos serão alterados).
        task (Task): Tarefa validada via dependência get_owned_task.
        db (Session): Sessão do banco para persisitir as alterações.

    Returns:
        TaskOut: Objeto atualizado da tarefa.
    """
    for field, value in task_in.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task: models.Task = Depends(get_owned_task),
    db: Session = Depends(get_db),
):
    """
    Remove uma tarefa existente pertencente ao usuário logado.

    Args:
        task (Task): Tarefa validada via dependência get_owned_task.
        db (Session): Sessão do banco para executar a exclusão.

    Returns:
        None: Retorna status HTTP 204 No Content no sucesso.
    """
    db.delete(task)
    db.commit()
    return None
