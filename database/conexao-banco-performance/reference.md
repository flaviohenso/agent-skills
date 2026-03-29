# Referência: conexão à BD e desempenho

Documento de apoio à skill `conexao-banco-performance`. Ler quando o contexto exigir mais profundidade.

## Plan cache no servidor: texto SQL idêntico

Muitos motores reutilizam planos de execução quando a **string SQL recebida é a mesma** (ou normalizada da mesma forma): o servidor faz hash da query; se já existir entrada no plan cache, evita ou reduz parse/optimization. **Literais diferentes na SQL ⇒ texto diferente ⇒ novo trabalho de compilação** (e possivelmente plano distinto).

**Regra de ouro:** usar **bind variables** (parâmetros), não incorporar valores na SQL com concatenação.

### JDBC puro

Evitar (um plano por valor de `status` e risco de SQL injection):

```java
String sql = "SELECT * FROM transactions WHERE status = '" + status + "'";
Statement stmt = connection.createStatement();
ResultSet rs = stmt.executeQuery(sql);
```

Preferir (o motor vê sempre a mesma forma textual com `?`):

```java
String sql = "SELECT * FROM transactions WHERE status = ?";
PreparedStatement pstmt = connection.prepareStatement(sql);
pstmt.setString(1, status);
ResultSet rs = pstmt.executeQuery();
```

## Spring Boot / Hibernate / JPA

O `PreparedStatement` costuma ser usado por baixo, mas é fácil **gerar SQL distinta** sem notar:

- **JPQL/HQL dinâmico:** não concatenar valores na string da query; usar `@Param` (Spring Data) ou `setParameter()` no `EntityManager` / APIs equivalentes.
- **Criteria API e literais:** literais embutidos que variam geram formas diferentes de SQL; quando fizer sentido, forçar tratamento como bind via propriedade Hibernate, por exemplo em `application.yml`:

```yaml
spring:
  jpa:
    properties:
      hibernate:
        criteria:
          literal_handling_mode: bind
```

- **`IN` com lista de tamanho variável:** `IN (?, ?)` e `IN (?, ?, ?)` são textos diferentes → vários planos para a mesma intenção. O Hibernate pode **pad** a lista para tamanhos padronizados, reduzindo variedade de SQL:

```yaml
spring:
  jpa:
    properties:
      hibernate:
        query:
          in_clause_parameter_padding: true
```

Validar com a versão do Hibernate e o motor: o ganho depende de como o plan cache trata essas formas.

## Cache de `PreparedStatement` no driver (HikariCP)

O **HikariCP** não substitui o cache de statements do servidor: no cliente, a reutilização do **objeto** preparado costuma ser responsabilidade do **driver JDBC**. Com pool, convém ativar/tunar isso na URL ou propriedades do datasource.

**PostgreSQL** (exemplo de parâmetros na URL; nomes e versões mínimas dependem do `postgresql` JDBC em uso):

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/mydb?preparedStatementCacheQueries=250&preparedStatementCacheSizeMiB=5
```

**MySQL** (Connector/J):

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/mydb?cachePrepStmts=true&prepStmtCacheSize=250&prepStmtCacheSqlLimit=2048
```

Outros motores (SQL Server, Oracle, etc.) têm parâmetros próprios na documentação do respetivo driver; o princípio é o mesmo: **texto SQL estável + parâmetros + cache alinhado ao driver**.

## Pooling (SQL)

- **Subdimensionar** o pool: filas longas, latência sob pico, timeouts aparentemente “aleatórios”.
- **Superdimensionar**: demasiadas conexões no servidor de BD, contenção de CPU/IO no motor, context switching.
- **Regra prática**: começar com um máximo derivado de `(número de instâncias da app × conexões por instância) ≤ limite seguro do BD`, ajustar com métricas.
- **Leak**: conexão não devolvida ao pool após exceção — rever `try/finally` ou equivalente e APIs que “escondem” o recurso.

## JDBC / JVM (exemplos de leitura)

- HikariCP: `maximumPoolSize`, `connectionTimeout`, `idleTimeout`, `maxLifetime` — `maxLifetime` abaixo do timeout de rede/BD evita conexões “mortas” no pool.
- Evitar criar `DataSource` novo por pedido; injetar singleton ou bean de aplicação.

## ORMs

- **Eager** excessivo vs **lazy** sem batch: perfilar antes de “eagerizar” tudo.
- **Second-level cache**: só com modelo de domínio e invalidação claros.
- **Bulk operations** nativas da ORM vs SQL bruto: documentar quando se opta por SQL por desempenho.

## NoSQL e clientes HTTP

- Pools de conexão HTTP do cliente reutilizados; timeouts e retries com backoff (evitar tempestade no cluster).
- Índices e cardinalidade de coleções MongoDB/análogos: mesmo espírito que índices SQL para padrões de leitura.

## Anti-padrões frequentes

- Query dentro de loop sem batch ou join.
- `SELECT *` em tabelas largas em caminhos quentes.
- Transação aberta durante chamadas a APIs externas ou leitura de ficheiros.
- Pool sem limite ou “uma conexão por thread” sem limite de threads.
- Reutilizar `Statement` com concatenação de strings (SQL injection + **plan cache ineficaz** no servidor).

## Verificação sugerida

- Traço de uma operação típica: quantas idas à BD, tempo total, paralelismo.
- Sob carga leve: fila do pool, percentil de latência de query.
- `EXPLAIN` (ou equivalente) nas queries mais custosas do caminho crítico.
