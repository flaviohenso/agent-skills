---
name: java-concorrencia-moderna
description: >-
  Analisa e projeta concorrência em Java (JDK 21+), escolhendo virtual vs
  platform threads, concorrência estruturada, limites com Semaphore e
  alternativas a ThreadLocal. Usa ao criar serviços paralelos, rever código
  concorrente, refatorar pools/CompletableFuture, migrar para virtual threads,
  ou quando o utilizador mencionar StructuredTaskScope, pinning, ScopedValue,
  I/O-bound, CPU-bound ou escalabilidade de threads.
---

# Java: concorrência moderna (criar e rever código)

## Objetivo

Orientar **design**, **implementação** e **code review** de concorrência em Java com foco em **escalabilidade**, **uso de recursos** e **resiliência**, alinhado ao JDK alvo do projeto (confirmar assinaturas e APIs na documentação oficial da versão em uso).

## Matriz de decisão: que tipo de thread?

### Preferir Virtual Threads quando

- A carga for **dominada por I/O bloqueante** (rede, BD, ficheiros) e o código passa muito tempo à espera.
- For necessária **concorrência em grande escala** (muitas tarefas simultâneas) sem um thread do SO por tarefa.

**Instanciação (orientação):** não usar pool de tamanho fixo pequeno como “otimização” para virtual threads. Padrões usuais: `Executors.newVirtualThreadPerTaskExecutor()` ou `Thread.ofVirtual().start(...)` / `Thread.ofVirtual().factory()`, conforme o estilo do projeto.

### Preferir Platform Threads (e pool limitado) quando

- A carga for **intensiva em CPU** (cálculo pesado, criptografia pesada, etc.): mais virtual threads que núcleos **não** aumentam throughput de CPU; pode haver overhead.
- Há **JNI/código nativo** ou bibliotecas que **fixem** o uso ao carrier de forma problemática e não seja viável refatorar (avaliar com profiling).

**Instanciação:** pools fixos limitados (por exemplo ao número de núcleos ou ligeiramente acima), com política clara de fila/rejeição se aplicável.

## Checklist de revisão (antipadrões)

### Virtual threads

1. **Pool fixo dedicado a virtual threads** — Evitar tratar virtual thread como “recurso escasso”; pool fixo pode **capar** escalabilidade. Rever se o pool existe por **limite de recurso externo** (aí o limite deve ser explícito, p.ex. semáforo), não por hábito de OS threads.

2. **Pinning** — Blocos/métodos `synchronized` (e outras causas de pinning) envolvendo **I/O bloqueante** podem **prender** a virtual thread ao carrier e anular benefícios. **Preferir** `java.util.concurrent.locks.ReentrantLock` (e APIs de alto nível não bloqueantes onde fizer sentido). Comportamento exato varia com a versão do JDK; validar no JDK do projeto.

3. **ThreadLocal em excesso (objetos pesados)** — Com muitas virtual threads ativas, **ThreadLocal** pode **crescer** de forma problemática. **Preferir** contexto com **escopo delimitado**: avaliar **ScopedValue** quando o JDK e o estilo do projeto o permitirem; caso contrário, reduzir estado por thread, reutilizar com controlo ou externalizar estado.

4. **Rate limiting só pelo tamanho do thread pool** — Com virtual threads “ilimitadas”, o gargalo desloca-se para **BD/serviços externos**. Usar **`Semaphore`** (ou filas, bulkhead, limites no cliente HTTP/connection pool) para **capar concorrência** contra recursos finitos.

### Concorrência estruturada

5. **Várias tarefas paralelas sem escopo** — Coleções de `CompletableFuture` ou `ExecutorService` sem política clara de cancelamento podem deixar trabalho **órfão** ou latência estranha em falhas. **Preferir** `StructuredTaskScope` (ou equivalente alinhado ao JDK) com política de junção explícita.

**Políticas de junção (conceito — validar API no JDK alvo):**

- **Falhar rápido (“tudo ou nada”):** qualquer falha cancela o resto; útil quando o resultado só é válido se tudo correr bem.
- **Primeiro sucesso (race):** primeira conclusão bem-sucedida cancela as outras; útil para tentar várias fontes/caches.
- **Aguardar todas (com ou sem falhas):** cenários de resiliência/notificações onde interessa o estado de cada ramo.
- **Todas com sucesso com resultados agregados:** quando é preciso juntar dados de várias subtarefas sem falhas.

Adaptar os **métodos exatos** (`Joiner`, `ShutdownOnFailure`, etc.) à versão do JDK em uso.

## Geração de código: modelo mental

Para serviços que fazem **várias operações relacionadas** em paralelo:

1. Abrir um **escopo estruturado** com política de junção adequada.
2. **Fork** de subtarefas (tipicamente em virtual thread executor quando I/O-bound).
3. **Join** / aguardar conforme a política.
4. Compor o resultado ou mapear falhas de forma **única** e clara (evitar exceções perdidas).

Incluir **timeout** e **cancelamento** quando o domínio exigir (APIs variam por JDK).

## Tríade rápida (validação antes de concluir)

- **É principalmente I/O-bound?** → virtual threads costumam ser o eixo certo (com proteção de recursos externos).
- **Há recurso externo limitado (BD, API, fila)?** → limitar concorrência com **Semaphore** / pool de conexões / bulkhead, não só “contar threads”.
- **Várias subtarefas com ciclo de vida partilhado?** → **StructuredTaskScope** (ou padrão equivalente) em vez de composição ad hoc de futures.

## Modo de uso com o pedido do utilizador

- **Criar projeto / feature:** propor executor, limites de concorrência, timeouts e estrutura de escopo antes de detalhar classes.
- **Rever / refatorar:** listar antipadrões encontrados, impacto (escalabilidade, latência, memória), e patch conceitual ou código sugerido **compatível com o JDK declarado**.

## Notas

- Confirmar **JDK mínimo** do repositório antes de recomendar APIs preview/final.
- Complementar com testes de carga e profiling (pinning, tempo em I/O vs CPU) quando o utilizador pedir otimização fina.
