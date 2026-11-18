# Requisitos do MVP

## Requisitos funcionais

| ID | Prioridade | Requisito | Regra ou condição | Evidência de cumprimento | Dependência |
|---|---|---|---|---|---|
| RF01 | Obrigatório | Cadastrar família com responsável, quantidade de membros, telefone, endereço e status. | Nome, quantidade de membros e endereço são obrigatórios; membros > 0. | A família aparece na consulta com identificador único. | — |
| RF02 | Obrigatório | Registrar entrega de cesta para uma família cadastrada. | A família deve existir e o estoque deve ser suficiente. | Registro da entrega criado e confirmação exibida. | RF01 |
| RF03 | Obrigatório | Atualizar o estoque após uma entrega válida. | Estoque reduzido pela quantidade entregue, nunca negativo. | Consulta do estoque mostra a quantidade atualizada. | RF02 |
| RF04 | Obrigatório | Consultar o histórico de entregas de uma família. | Exibe apenas as entregas vinculadas à família. | Lista de entregas com data e quantidade. | RF01, RF02 |
| RF05 | Desejável | Listar famílias com status "aguardando". | Considera apenas status = aguardando. | Lista contendo somente essas famílias. | RF01 |

Ordem de implementação: RF01 → RF02 → RF03 → RF04 → RF05.

## Requisitos não funcionais

- **RNF01 — Autenticação:** acesso restrito a voluntários autenticados; senhas armazenadas apenas como hash Argon2id com salt (nunca em texto limpo, MD5 ou SHA-1); sessão encerrada por logout e por inatividade.
- **RNF02 — OWASP e proteção de dados:** consultas parametrizadas (contra SQL Injection), escape da saída nos templates (contra XSS), autorização verificada no servidor, mensagens de erro genéricas e dependências atualizadas.
- **Minimização de dados:** não são coletados CPF nem documentos pessoais.

## Modelo de dados

```
familia (1) ──< entrega (N)          estoque (registro único)
```

- **familia**: id_familia (PK), nome_responsavel, quantidade_membros, telefone, endereco, data_cadastro, status
- **entrega**: id_entrega (PK), id_familia (FK), data_entrega, quantidade_cestas, observacao
- **estoque**: id_estoque (PK), quantidade_disponivel, data_atualizacao

O script de criação está em [`database/schema.sql`](../database/schema.sql).
