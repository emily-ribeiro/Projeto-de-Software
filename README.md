# Task Tracker API — Avaliação de Assistentes de IA no Desenvolvimento de Software

> Estudo de caso prático para avaliar, comparar e documentar a eficiência de diferentes
> combinações de IDEs e assistentes de IA (LLMs) no processo de desenvolvimento de software.

## 1. Sumário

- [Objetivo](#objetivo)
- [Arquitetura do Estudo de Caso](#arquitetura-do-estudo-de-caso)
- [Ambiente de Testes](#ambiente-de-testes)
- [Metodologia](#metodologia)
- [Critérios de Avaliação](#critérios-de-avaliação)
- [Tabela Comparativa](#tabela-comparativa)
- [Conclusão](#conclusão)
- [Como Rodar o Projeto](#como-rodar-o-projeto)

## Objetivo

Comparar, na prática, duas (ou mais) combinações de IDE + assistente de IA usadas para
desenvolver o mesmo sistema, medindo velocidade, qualidade de código, geração de testes
e facilidade de refatoração/documentação.

## Arquitetura do Estudo de Caso

**Sistema escolhido:** Task Tracker API — uma API REST de gerenciamento de tarefas.

**Justificativa:** complexidade baixa/moderada, mas com superfície suficiente para
exercitar os quatro critérios de avaliação: autenticação (lógica com estado e segurança),
CRUD (repetição de padrões — bom para medir velocidade), filtros/buscas (regras de negócio
não triviais) e um bug real de compatibilidade de dependências encontrado durante o
desenvolvimento (ótimo caso para avaliar debugging assistido por IA).

**Stack:**
- Python 3.12
- FastAPI (framework web)
- SQLAlchemy (ORM) + SQLite (banco de dados)
- Pydantic v2 (validação de dados)
- python-jose + passlib/bcrypt (autenticação JWT)
- Pytest + httpx (testes automatizados)

**Módulos do sistema:**

| Módulo | Responsabilidade |
|---|---|
| `app/models.py` | Modelos de dados (User, Task) via SQLAlchemy |
| `app/schemas.py` | Contratos de entrada/saída da API (Pydantic) |
| `app/auth.py` | Hash de senha, geração/validação de JWT |
| `app/routers/auth_router.py` | Endpoints de registro e login |
| `app/routers/tasks.py` | CRUD de tarefas + filtros (status, prioridade, tag, busca) |
| `app/database.py` | Configuração de conexão e sessão do banco |
| `tests/` | Testes unitários e de integração (Pytest) |

**Diagrama simplificado do fluxo de requisição:**

```
Cliente → FastAPI Router → Depends(get_current_user) [valida JWT]
                          → Depends(get_db) [sessão do banco]
                          → Lógica do endpoint
                          → SQLAlchemy ORM → SQLite
                          → Response (Pydantic Schema)
```

## Ambiente de Testes


Ferramentas testadas (mínimo de duas combinações gratuitas):

| Combinação | IDE | Assistente de IA | Plano usado |
|---|---|---|---|
| A | VS Code | GitHub Copilot | Free / Estudante |
| B | Cursor | Modelo integrado (free tier) | Free |
| C | Antigravaty + Gemini | Free


Durante os testes, a Combinação B planejada inicialmente (Cursor free tier) esbarrou no limite de tokens do plano gratuito antes de completar o Módulo 1, impossibilitando a conclusão do teste nessa ferramenta. Além disso, constatou-se que o Gemini Code Assist para contas individuais foi descontinuado pelo Google em 18/06/2026, sendo substituído pela plataforma Antigravity. Diante disso, a Combinação C foi adicionada [Antigravity+Gemini], mantendo a mesma metodologia de testes.

## Metodologia

1. O sistema foi dividido em módulos equivalentes (autenticação, CRUD de tarefas, filtros,
   testes, refatoração/documentação).
2. Cada módulo foi implementado **do zero, de forma independente, em cada combinação
   IDE + LLM**, partindo do mesmo enunciado de requisitos, para manter a comparação justa.
3. Para cada sessão de desenvolvimento, foi preenchido um registro em
   [`docs/log-sessoes.csv`](docs/log-sessoes.csv) contendo: tempo gasto, número de
   sugestões aceitas/rejeitadas, bugs introduzidos pela IA, e observações qualitativas.
4. Ao final de cada módulo, foi solicitado à IA: (a) gerar testes unitários/integração,
   (b) explicar o código gerado, (c) sugerir uma refatoração — e o resultado foi avaliado
   segundo os critérios abaixo.
5. Um mesmo bug real (incompatibilidade `bcrypt`/`passlib`, documentado neste projeto) foi
   apresentado a cada ferramenta para comparar a capacidade de diagnóstico e correção.

## Critérios de Avaliação

- **Qualidade do Código** — as sugestões seguiram boas práticas? Introduziram bugs?
  Precisou de correção manual?
- **Velocidade** — tempo real gasto implementando cada módulo com IA vs. estimativa
  do tempo sem IA (baseline).
- **Geração de Testes** — os testes gerados compilam/rodam de primeira? Cobrem casos de
  borda (ex.: tarefa de outro usuário, senha errada, tarefa inexistente)? Há falsos
  positivos (testes que passam mas não testam nada relevante)?
- **Refatoração e Documentação** — qualidade das explicações pedidas à IA, clareza da
  documentação gerada, facilidade de pedir mudanças incrementais sem quebrar o código.

## Tabela Comparativa

| Critério | Combinação A | Combinação B | Combinação C |
|---|---|---|---|
| Velocidade média por módulo | — | — | — |
| Taxa de sugestões aceitas | — | — | — |
| Bugs introduzidos pela IA | — | — | — |
| Qualidade dos testes gerados | — | — | — |
| Facilidade de refatoração | — | — | — |
| Qualidade da documentação gerada | — | — | — |
| Prós | — | — | — |
| Contras | — | — | — |

## Conclusão

## Como Rodar o Projeto

```bash
# 1. Criar ambiente virtual (opcional, mas recomendado)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Rodar a API
uvicorn app.main:app --reload

# 4. Acessar a documentação interativa
# http://localhost:8000/docs

# 5. Rodar os testes
pytest -v
```

### Nota técnica: bug real encontrado

Durante o desenvolvimento, `passlib[bcrypt]==1.7.4` combinado com a versão mais recente
do pacote `bcrypt` (5.x) quebra com o erro
`ValueError: password cannot be longer than 72 bytes`, causado por uma mudança de API
não compatível entre as bibliotecas. Correção: fixar `bcrypt==4.0.1` no `requirements.txt`.
Isso foi usado como caso de teste para avaliar a capacidade de diagnóstico das IAs.
