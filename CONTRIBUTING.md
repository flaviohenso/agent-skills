# Contribuindo

## Onde colocar uma nova skill

Escolha a pasta de categoria conforme o foco principal:

| Categoria | Uso |
|-----------|-----|
| `requirements/` | Histórias de negócio, refinamento, critérios de aceite, perguntas a stakeholders |
| `solution-design/` | Opções técnicas, trade-offs, escopo MVP/incremental |
| `architecture/` | ADR, C4, integrações, modelo de dados |
| `quality-risk/` | NFRs, riscos, segurança por design |
| `documentation/` | RFC, diagramas, comunicação com o time ou negócio |
| `stack/<linguagem>/` | Skills fortemente acopladas a uma stack (ex.: Java/Spring) |

Cada skill é um diretório com `SKILL.md` na raiz desse diretório.

## Checklist de qualidade

- **Nome da pasta:** `kebab-case`, curto; deve ser **único em todo o repositório** (o sync achatado copia só o nome da pasta da skill).
- **Frontmatter:** `name` (≤64 caracteres, `a-z`, `0-9`, `-`) e `description` (≤1024 caracteres, não vazia).
- **Descrição:** terceira pessoa; incluir **o quê** a skill faz e **quando** usar (termos que ajudem descoberta automática).
- **Corpo:** preferir `SKILL.md` enxuto; usar `reference.md` ou `examples.md` no mesmo nível para detalhes.
- **Links:** do `SKILL.md`, preferir apenas um nível de profundidade para outros arquivos.
- **Scripts:** se existir `scripts/`, documentar no `SKILL.md` se o agente deve executar ou apenas ler.

## Como testar localmente

1. Copie a pasta da skill para o diretório de skills da sua ferramenta (veja [docs/how-to-install-skills.md](docs/how-to-install-skills.md)).
2. Regenere o índice opcional: `python3 scripts/generate_skill_index.py`

## Índice gerado

O ficheiro [SKILL_INDEX.md](SKILL_INDEX.md) é gerado pelo script; em PRs que alterem skills, execute o script e inclua as alterações no índice, ou deixe o CI atualizar conforme a configuração do repositório.
