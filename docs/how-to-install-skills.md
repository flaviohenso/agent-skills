# Instalar skills no Cursor, Gemini CLI e Claude Code

Este repositório guarda skills em `categoria/nome-da-skill/SKILL.md`. As ferramentas esperam **uma pasta por skill** no respetivo diretório de skills — ou seja, o caminho da categoria **não** vai para o destino final.

## Regra do “achatamento”

Origem no repo:

```text
requirements/checklist-criterios-aceite/SKILL.md
```

Destino típico (exemplo Cursor):

```text
~/.cursor/skills/checklist-criterios-aceite/SKILL.md
```

Garanta que **não existem duas skills com o mesmo nome de pasta** em categorias diferentes.

## Cursor

- **Global:** `~/.cursor/skills/<nome-da-skill>/`
- **Por projeto:** `<repo-do-projeto>/.cursor/skills/<nome-da-skill>/`

**Não** coloque skills personalizadas em `~/.cursor/skills-cursor/` (reservado ao Cursor).

## Gemini CLI

- **Utilizador:** `~/.gemini/skills/<nome-da-skill>/`
- **Projeto:** `.gemini/skills/<nome-da-skill>/` ou `.agents/skills/<nome-da-skill>/` (conforme a versão e documentação oficial)

## Claude Code

- **Projeto:** `<repo-do-projeto>/.claude/skills/<nome-da-skill>/`

## Script de sincronização

Na raiz do repositório clonado:

```bash
./scripts/sync-skills.sh cursor      # ~/.cursor/skills
./scripts/sync-skills.sh gemini      # ~/.gemini/skills
./scripts/sync-skills.sh claude /caminho/do/projeto   # .claude/skills dentro desse projeto
```

O script copia todas as skills (ignora `_templates` e pastas sem `SKILL.md`). Sobrescreve destinos com o mesmo nome.

## Cópia manual

```bash
cp -r requirements/checklist-criterios-aceite ~/.cursor/skills/
```

Consulte a documentação atual de cada CLI para listar, ativar ou desativar skills.
