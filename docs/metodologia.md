# Metodologia Detalhada

## Divisão do trabalho entre as IAs

O sistema foi dividido nos seguintes módulos, cada um implementado de forma independente
(do zero) em cada combinação IDE + LLM testada, a partir do mesmo enunciado de requisitos:

1. Modelagem de dados (User, Task)
2. Autenticação (registro, login, JWT)
3. CRUD de tarefas
4. Filtros e busca
5. Geração de testes automatizados
6. Debug de um bug real (incompatibilidade bcrypt/passlib)
7. Refatoração e documentação de um trecho de código já pronto

## Protocolo de cada sessão

1. Abrir cronômetro.
2. Descrever a tarefa para a IA da mesma forma em todas as ferramentas (mesmo prompt-base).
3. Registrar quantas sugestões foram aceitas sem alteração, aceitas com alteração, ou
   rejeitadas.
4. Rodar os testes / a aplicação para verificar se o código funciona de primeira.
5. Anotar bugs introduzidos pela IA (que não existiam no requisito) e o tempo para corrigi-los.
6. Pedir explicitamente: "gere testes unitários para este módulo" e avaliar se rodam sem
   ajuste manual.
7. Pedir explicitamente: "explique este código" e "sugira uma refatoração" — avaliar clareza.
8. Preencher uma linha em `docs/log-sessoes.csv`.

## Critério de comparação justa

Para não favorecer nenhuma ferramenta, o mesmo desenvolvedor, com o mesmo nível de
familiaridade prévia com o domínio, executa as mesmas tarefas em todas as combinações,
em dias/sessões diferentes, evitando efeito de aprendizado cumulativo (ex.: fazer o
módulo de autenticação primeiro em ferramentas diferentes, alternando a ordem).
