-- Modelo de dados do MVP: familia, entrega e estoque

CREATE TABLE IF NOT EXISTS familia (
    id_familia         INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_responsavel   TEXT    NOT NULL,
    quantidade_membros INTEGER NOT NULL CHECK (quantidade_membros > 0),
    telefone           TEXT,
    endereco           TEXT    NOT NULL,
    data_cadastro      DATE    NOT NULL DEFAULT (DATE('now')),
    status             TEXT    NOT NULL DEFAULT 'aguardando'
                       CHECK (status IN ('aguardando', 'atendida'))
);

CREATE TABLE IF NOT EXISTS entrega (
    id_entrega        INTEGER PRIMARY KEY AUTOINCREMENT,
    id_familia        INTEGER NOT NULL REFERENCES familia (id_familia),
    data_entrega      DATE    NOT NULL DEFAULT (DATE('now')),
    quantidade_cestas INTEGER NOT NULL CHECK (quantidade_cestas > 0),
    observacao        TEXT
);

CREATE TABLE IF NOT EXISTS estoque (
    id_estoque            INTEGER PRIMARY KEY AUTOINCREMENT,
    quantidade_disponivel INTEGER NOT NULL DEFAULT 0 CHECK (quantidade_disponivel >= 0),
    data_atualizacao      DATE    NOT NULL DEFAULT (DATE('now'))
);

-- Garante um registro inicial de estoque
INSERT INTO estoque (id_estoque, quantidade_disponivel)
SELECT 1, 0
WHERE NOT EXISTS (SELECT 1 FROM estoque WHERE id_estoque = 1);

-- RNF01: voluntários com acesso ao sistema (senha somente em hash Argon2id)
CREATE TABLE IF NOT EXISTS voluntario (
    id_voluntario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome          TEXT    NOT NULL,
    email         TEXT    NOT NULL UNIQUE,
    senha_hash    TEXT    NOT NULL
);
