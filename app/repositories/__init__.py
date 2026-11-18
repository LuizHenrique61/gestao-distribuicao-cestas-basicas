"""Camada de dados: acesso ao banco SQLite.

Os repositórios apenas executam comandos SQL parametrizados. Quem confirma
(commit) ou desfaz (rollback) uma operação é a camada de serviços, que conhece
a regra de negócio completa.
"""
