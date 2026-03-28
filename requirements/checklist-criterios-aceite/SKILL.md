---
name: checklist-criterios-aceite
description: >-
  Refina histórias de utilizador ou requisitos funcionais em critérios de aceite
  testáveis, cenários Given/When/Then e deteção de lacunas. Use ao refinamento de
  backlog, escrita de user stories, definição de DoR ou quando o utilizador pedir
  critérios de aceite, BDD ou clareza de escopo.
---

# Checklist de critérios de aceite

## Objetivo

Transformar descrições vagas de negócio em critérios **específicos**, **mensuráveis** e **testáveis**, alinhados ao valor pretendido.

## Passos

1. **Extrair o resultado desejado** em uma frase sem jargão técnico desnecessário.
2. **Listar atores e pré-condições** (estado inicial, permissões, dados mínimos).
3. **Para cada critério**, usar formato verificável:
   - Preferir bullets com condição observável + resultado esperado; ou
   - Cenários **Given / When / Then** quando ajudar testes automatizados.
4. **Marcar ambiguidades** com perguntas explícitas ao negócio (não adivinhar regras críticas).
5. **Separar escopo MVP** do que é “nice to have” se a história for grande.

## Checklist rápida

- [ ] Cada critério pode ser validado por quem testa (QA ou negócio) sem interpretação subjetiva excessiva
- [ ] Erros e estados limite estão cobertos ou explicitamente fora de escopo
- [ ] Integrações externas têm comportamento definido (sucesso, timeout, indisponibilidade)
- [ ] Não há dependência implícita de outra história sem referência

## Saída sugerida

```markdown
## História
[Resumo]

## Critérios de aceite
1. ...
2. ...

## Perguntas em aberto
- ...
```
