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
| C | | Antigravity + Gemini | Free |

Durante os testes, a Combinação B planejada inicialmente (Cursor free tier) esbarrou no limite de tokens do plano gratuito antes de completar o Módulo 1, impossibilitando a conclusão do teste nessa ferramenta. Além disso, constatou-se que o Gemini Code Assist para contas individuais foi descontinuado pelo Google em 18/06/2026, sendo substituído pela plataforma Antigravity. Diante disso, a Combinação C foi adicionado o [Antigravity+S], mantendo a mesma metodologia de testes.

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
Com base nos testes realizados, não existe uma combinação IDE + IA objetivamente "melhor" em todos os aspectos — a escolha ideal depende do perfil e da afinidade do desenvolvedor com cada ambiente, além do estágio do projeto. Ainda assim, foi possível identificar diferenças relevantes de custo-benefício entre as ferramentas testadas:

GitHub Copilot (VS Code) entregou código funcional e com boas práticas modernas (ex.: uso de datetime com timezone e tipagem SQLAlchemy 2.0 acima do baseline), mas cometeu um deslize de segurança ao fixar a SECRET_KEY diretamente no código em vez de usar variável de ambiente — um lembrete de que sugestões da IA ainda exigem revisão crítica, mesmo quando o código "funciona".

Cursor (free tier) esbarrou no limite de tokens do plano gratuito antes de concluir o primeiro módulo, o que na prática inviabilizou seu uso contínuo sem custo — um fator de custo-benefício tão relevante quanto a qualidade técnica das sugestões.


Gemini Code Assist no VS Code, inicialmente cogitado como terceira combinação, foi descontinuado pelo Google em 18/06/2026 para contas individuais, substituído pela plataforma Antigravity, adotada como Combinação C neste estudo.
Antigravity, por ser uma plataforma "agent-first", demonstrou maior autonomia para conduzir o fluxo completo de geração, execução de testes e correção iterativa sem intervenção manual constante — vantagem clara quando o objetivo é delegar tarefas maiores à IA. Em contrapartida, essa autonomia reduziu o controle fino sobre quando e como cada etapa era executada (ex.: dificuldade de isolar o tempo de geração do tempo de validação, já que o agente encadeia as duas automaticamente).

Ferramentas de extensão dentro do próprio VS Code (Copilot, Continue.dev) oferecem mais controle granular e um ecossistema maior de opções e modelos configuráveis, o que favorece quem já tem um ambiente de desenvolvimento consolidado e não quer trocar de IDE. Já plataformas "tudo-em-um" como Antigravity favorecem quem prioriza produtividade em modo agente, aceitando abrir mão de parte do controle manual do processo.

## Como Rodar o Projeto

```bash
# 1. Criar ambiente virtual 
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


