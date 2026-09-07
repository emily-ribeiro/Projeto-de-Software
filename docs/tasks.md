# Endpoints de tarefas

Os endpoints ficam em `app/routers/tasks.py` e exigem autenticação JWT.
O usuário autenticado é obtido pela dependência `get_current_user`. Cada tarefa é
criada com o `owner_id` do usuário logado.

## CRUD

| Método | Endpoint | Comportamento |
|---|---|---|
| POST | `/tasks/` | Cria uma tarefa e retorna `201`. |
| GET | `/tasks/` | Lista somente as tarefas do usuário autenticado. |
| GET | `/tasks/{task_id}` | Retorna uma tarefa específica. |
| PUT | `/tasks/{task_id}` | Atualiza parcialmente os campos enviados. |
| DELETE | `/tasks/{task_id}` | Remove uma tarefa e retorna `204`. |

Ao buscar, atualizar ou remover uma tarefa, a API retorna `404` quando ela não existe
e `403` quando pertence a outro usuário.

## Filtros

O endpoint `GET /tasks/` aceita os seguintes parâmetros opcionais:

- `status`: `pending`, `in_progress` ou `done`;
- `priority`: `low`, `medium` ou `high`;
- `tag`: filtra pela tag exata;
- `search`: procura por correspondência parcial e case-insensitive no título.

Os filtros podem ser combinados. A consulta sempre restringe os resultados ao usuário
autenticado antes de aplicar os filtros.

Exemplo:

```text
GET /tasks/?status=done&priority=high&tag=backend&search=api
```

As descrições das funções também estão disponíveis como docstrings no código e são
exibidas pelo FastAPI em `http://localhost:8000/docs`.
