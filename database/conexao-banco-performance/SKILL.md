---
name: conexao-banco-performance
description: >-
  Orienta criação e revisão de código de ligação e acesso a bases de dados
  (drivers, pools, sessões, consultas, transações) com foco em desempenho e
  fiabilidade, incluindo reutilização de planos de execução (texto SQL estável,
  bind variables, PreparedStatement, cache no driver). Use ao implementar ou
  rever JDBC, connection strings, HikariCP, ORMs, Spring Data/JPA, Hibernate,
  clientes NoSQL, timeouts, pooling, ou quando o utilizador pedir plan cache,
  otimização de I/O, latência ou revisão da camada de persistência.
---

# Conexão à base de dados e desempenho

## Quando aplicar

- Pedidos para **criar** infraestrutura de acesso a dados (novo módulo, serviço, repositório).
- Pedidos para **rever** código existente ligado a conexões, consultas ou transações.
- Palavras-chave: pool, connection string, timeout, JDBC, datasource, ORM, N+1, batch, índice, sessão, leak, plan cache, bind variable, PreparedStatement.

## Fluxo de trabalho

1. **Identificar stack**: motor (PostgreSQL, MySQL, SQL Server, Oracle, MongoDB, etc.), runtime (JVM, Node, Python, Go, .NET) e bibliotecas (driver nativo, ORM, query builder).
2. **Determinar modo**:
   - **Criar**: propor arquitetura mínima (configuração, ciclo de vida, limites) antes de detalhar implementação.
   - **Rever**: mapear todos os pontos que abrem sessão/conexão, executam I/O e fecham recursos; priorizar riscos de desempenho e estabilidade.
3. **Aplicar a checklist** abaixo; para matrizes por tipo de stack e anti-padrões, ver [reference.md](reference.md).

## Checklist (criar e rever)

### Ligação e ciclo de vida

- Uma **fonte de verdade** para configuração (URL, credenciais, SSL); sem duplicar pools por pedido.
- **Pool dimensionado**: tamanho máximo coerente com workers da app e limites do servidor de BD; evitar `max pool = threads` sem justificação.
- **Timeouts explícitos**: conexão, leitura de socket, tempo máximo de empréstimo do pool (quando aplicável).
- **Encerramento ordenado** no shutdown da aplicação (drenar pool, fechar recursos).
- **Health check** alinhado ao pool/driver (evitar queries pesadas em cada ping).

### Consultas e modelo de dados

- **Prepared statements** / **bind variables**: o texto SQL enviado ao motor deve ser **idêntico** entre chamadas (placeholders `?` / nomeados); literais concatenados geram SQL diferente, invalidam **plan cache** no servidor e pioram parse/optimize. Ver secção seguinte e [reference.md](reference.md).
- Evitar **N+1**: joins adequados, batch fetch, Dataloader ou queries agregadas quando fizer sentido.
- **Projeções** estreitas (`SELECT` só do necessário); paginação com `LIMIT`/cursor em listagens grandes.
- **Transações** com escopo mínimo: não manter transação aberta durante I/O externo ou CPU longa.
- **Isolamento** coerente com requisitos (evitar locks desnecessários; documentar trade-offs).

### Desempenho e observabilidade

- **Índices** e ordem de colunas em `WHERE`/`JOIN` alinhados ao que a query precisa (sugerir verificação com `EXPLAIN` quando relevante).
- **Batch inserts/updates** onde o volume justificar; tamanho de batch tunável.
- **Cache** só com política de invalidação clara (não mascarar inconsistência).
- **Métricas**: tempo de query, uso do pool (ativas, à espera, rejeitadas), erros de timeout; correlação com traces.

### Segurança mínima na camada de dados

- Sem credenciais em código; preferir segredos/variáveis de ambiente ou vault.
- Princípio do menor privilégio na conta de BD usada pela aplicação.

## Plan cache no servidor e lado cliente (Java / Spring)

- **Servidor**: muitos motores associam planos ao texto normalizado/hash da query; **uma linha SQL nova por literal** ⇒ novo parse/optimize (ou novo plano). Preferir sempre parâmetros em vez de incorporar valores na string.
- **JDBC**: `PreparedStatement` com SQL fixo + `setX`; evitar `Statement` + concatenação em caminhos quentes.
- **Spring / JPA / Hibernate**: não concatenar valores em JPQL/Criteria; usar `@Param` / `setParameter`. Cuidado com **`IN` dinâmico** (`IN (?,?)` vs `IN (?,?,?)`) — listas de tamanho variável multiplicam planos; avaliar padding de parâmetros (Hibernate). Literais em Criteria: preferir modo que force bind (propriedade Hibernate).
- **Pool (HikariCP) + driver**: o cache de **objetos** `PreparedStatement` no cliente fica no **driver JDBC** (Hikari delega); ativar/tunar parâmetros na **URL** ou propriedades do datasource conforme PostgreSQL, MySQL, etc. Detalhes e exemplos YAML em [reference.md](reference.md).

## Formato da resposta (revisão)

Estruturar o feedback assim:

1. **Resumo** (2–4 frases): risco principal de desempenho ou estabilidade.
2. **Crítico** — corrigir antes de produção (leaks, pool ilimitado, transações erradas, SQL injection).
3. **Desempenho** — ganhos prováveis (índice, batch, N+1, timeouts, texto SQL estável / plan cache, cache de prepared no driver).
4. **Sugestões** — melhorias opcionais (observabilidade, configuração fina).
5. **Verificações** — o que medir ou testar depois (carga, `EXPLAIN`, métricas do pool).

## Recursos adicionais

- Detalhes e anti-padrões: [reference.md](reference.md)
