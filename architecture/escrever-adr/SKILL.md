---
name: escrever-adr
description: >-
  Redige Architecture Decision Records (ADR) com contexto, decisão, consequências
  e alternativas rejeitadas. Use ao documentar escolhas arquiteturais, revisões de
  design, propostas técnicas formais ou quando o utilizador pedir ADR, registo de
  decisão ou comparativo de opções já escolhidas.
---

# Escrever ADR

## Estrutura recomendada (Markdown)

1. **Título:** número + nome curto, ex. `ADR-012: Uso de fila para notificações`
2. **Estado:** Proposto | Aceite | Depreciado | Substituído por ADR-XXX
3. **Contexto:** problema de negócio ou técnico, restrições, pressões (prazo, custo, equipe).
4. **Decisão:** o que foi (ou será) escolhido, em linguagem precisa.
5. **Consequências:** positivas, negativas e riscos aceites.
6. **Alternativas consideradas:** pelo menos uma, com motivo da rejeição.

## Princípios

- Focar na **decisão** e no **porquê**, não em tutorial da tecnologia.
- Evitar ADRs gigantes; anexar diagrama ou link se necessário.
- Se substituir decisão antiga, referenciar o ADR anterior e atualizar o estado.

## Template

```markdown
# ADR-NNN: Título

## Estado
Aceite

## Contexto
...

## Decisão
...

## Consequências
- ...

## Alternativas
- **Opção A:** rejeitada porque ...
- **Opção B:** rejeitada porque ...
```
