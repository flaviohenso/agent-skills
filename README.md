# agent-skills

Repositório de **Agent Skills** em Markdown com frontmatter YAML (`name`, `description`), pensado para engenharia de software, arquitetura e análise de histórias de negócio. O mesmo conteúdo pode ser instalado no **Cursor**, **Gemini CLI** e **Claude Code** — apenas muda o diretório de destino.

## Estrutura

| Pasta | Conteúdo |
|-------|----------|
| `requirements/` | Negócio, histórias, refinamento, critérios de aceite |
| `solution-design/` | Opções técnicas, trade-offs, escopo incremental |
| `architecture/` | ADR, C4, integrações, modelo de dados |
| `quality-risk/` | NFRs, risco, segurança por design |
| `documentation/` | RFC, diagramas, comunicação com time/negócio |
| `stack/<linguagem>/` | Skills acopladas a uma stack (ex.: Java) |
| `_templates/skill-template/` | Modelo para novas skills |

Cada skill é `categoria/nome-da-skill/SKILL.md`. O nome da pasta da skill deve ser **único em todo o repositório** (instalação “achatada”).

## Índice

Ver [SKILL_INDEX.md](SKILL_INDEX.md) (gerado automaticamente). Para atualizar após editar skills:

```bash
python3 scripts/generate_skill_index.py
```

## Onde instalar (por ferramenta)

| Ferramenta | Destino típico |
|------------|----------------|
| **Cursor** | `~/.cursor/skills/<skill>/` ou `.cursor/skills/<skill>/` no projeto |
| **Gemini CLI** | `~/.gemini/skills/<skill>/` ou `.gemini/skills/` no projeto |
| **Claude Code** | `.claude/skills/<skill>/` no projeto |

Não use `~/.cursor/skills-cursor/` para skills suas — é área reservada ao Cursor.

Guia passo a passo: [docs/how-to-install-skills.md](docs/how-to-install-skills.md).

## Sincronizar todas as skills

Na raiz do repositório clonado:

```bash
./scripts/sync-skills.sh cursor
./scripts/sync-skills.sh gemini
./scripts/sync-skills.sh claude /caminho/do/seu/projeto
```

## Contribuir

Leia [CONTRIBUTING.md](CONTRIBUTING.md).

## Licença

MIT — ver [LICENSE](LICENSE).
