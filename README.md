# Sistema de Gestão de Distribuição de Cestas Básicas

MVP (Produto Mínimo Viável) desenvolvido como projeto acadêmico do curso de **Análise e Desenvolvimento de Sistemas** da **Cruzeiro do Sul**.

O sistema apoia os voluntários do programa **Mãos Abertas**, da **Remar Brasil** (Guarulhos/SP), na organização da distribuição de cestas básicas para famílias em situação de vulnerabilidade social.

---

## 📌 Problema

A organização precisa acompanhar os cadastros das famílias atendidas, as entregas de cestas básicas realizadas e as famílias que ainda aguardam atendimento. Quando essas informações ficam espalhadas em anotações, planilhas ou conversas, surgem retrabalho, perda de registros e dificuldade para saber quem já recebeu a cesta e quantas cestas ainda estão disponíveis.

## 🎯 Objetivo do MVP

Centralizar em uma aplicação web simples o fluxo de distribuição:

- cadastrar famílias;
- registrar entregas de cestas;
- atualizar automaticamente o estoque;
- consultar o histórico de entregas de cada família;
- identificar famílias que aguardam atendimento.

## 👥 Público-alvo

| Grupo | Descrição |
|---|---|
| **Usuários diretos** | Responsáveis e voluntários da Remar Brasil que cadastram famílias, controlam o estoque e registram as entregas. |
| **Beneficiários indiretos** | Famílias em situação de vulnerabilidade atendidas pelo programa Mãos Abertas. |

## 🌱 ODS relacionado

**ODS 2 — Fome Zero e Agricultura Sustentável**: o sistema contribui para uma distribuição de alimentos mais organizada, reduzindo falhas no controle das entregas e ajudando a direcionar as cestas a quem ainda aguarda atendimento.

## ✅ Requisitos funcionais

| ID | Prioridade | Requisito |
|---|---|---|
| RF01 | Obrigatório | Cadastrar família (responsável, nº de membros, telefone, endereço e status). |
| RF02 | Obrigatório | Registrar entrega de cesta para uma família cadastrada. |
| RF03 | Obrigatório | Atualizar o estoque após uma entrega válida (nunca negativo). |
| RF04 | Obrigatório | Consultar o histórico de entregas de uma família. |
| RF05 | Desejável | Listar as famílias com status "aguardando". |

Detalhes em [`docs/requisitos.md`](docs/requisitos.md).

## 🛠️ Tecnologias

| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.12 | Linguagem principal e regras de negócio |
| Flask | 3.x | Rotas e servidor web |
| Jinja2 | 3.x | Templates das telas |
| HTML5 / CSS3 | — | Interface responsiva |
| SQLite | 3 | Banco de dados embarcado |
| argon2-cffi | 23+ | Hash de senhas com Argon2id |
| pytest | 8.x | Testes automatizados |

## 🏗️ Arquitetura

Arquitetura **monolítica em camadas**:

```
Interface (templates + rotas)  →  Regras de negócio (services)  →  Dados (repositories + SQLite)
```

- **Apresentação** (`app/routes.py`, `app/templates/`, `app/static/`): telas e formulários usados pelos voluntários.
- **Aplicação** (`app/services/familia_service.py`, `app/services/entrega_service.py`): validações e regras, como impedir entrega sem estoque suficiente.
- **Dados** (`app/repositories/*_repository.py`, `database/schema.sql`): leitura e gravação no SQLite com consultas parametrizadas.

Fluxo principal (registrar entrega): o voluntário envia o formulário → `entrega_service` verifica se a família existe e se há estoque → grava a entrega, dá baixa no estoque e marca a família como atendida em uma única transação → a tela mostra a confirmação e o histórico atualizado.

## 📁 Estrutura do repositório

```
.
├── app/
│   ├── __init__.py          # Criação da aplicação Flask
│   ├── routes.py            # Camada de apresentação (rotas)
│   ├── services/            # Camada de aplicação (regras de negócio)
│   ├── repositories/        # Camada de dados (acesso ao SQLite)
│   ├── templates/           # Telas HTML (Jinja2)
│   └── static/css/          # Estilos
├── database/
│   └── schema.sql           # Tabelas: familia, entrega, estoque
├── docs/
│   └── requisitos.md        # Requisitos e modelo de dados
├── tests/                   # Testes com pytest
├── requirements.txt
├── run.py                   # Ponto de entrada
└── README.md
```

## 🗃️ Modelo de dados

- **familia** — `id_familia`, `nome_responsavel`, `quantidade_membros`, `telefone`, `endereco`, `data_cadastro`, `status` (aguardando/atendida)
- **entrega** — `id_entrega`, `id_familia` (FK), `data_entrega`, `quantidade_cestas`, `observacao`
- **estoque** — `id_estoque`, `quantidade_disponivel`, `data_atualizacao`

Uma família pode ter várias entregas; cada entrega pertence a uma família e reduz o estoque. Por minimização de dados, o sistema **não** coleta CPF nem documentos pessoais.

## ▶️ Como executar

```bash
# 1. Clonar o repositório
git clone https://github.com/LuizHenrique61/gestao-distribuicao-cestas-basicas.git
cd gestao-distribuicao-cestas-basicas

# 2. Criar e ativar o ambiente virtual
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Criar o primeiro voluntário (pede nome, e-mail e senha)
flask --app run criar-voluntario

# 5. Iniciar a aplicação
python run.py
```

Acesse em `http://127.0.0.1:5000` e entre com o e-mail e a senha do voluntário criado.

Para rodar os testes (25 testes cobrindo RF01 a RF05, autenticação e entradas maliciosas):

```bash
pytest
```

## 🚧 Status

| Requisito | Situação |
|---|---|
| RF01 — Cadastro de famílias | ✅ Implementado |
| RF02 — Registro de entregas | ✅ Implementado |
| RF03 — Atualização do estoque | ✅ Implementado |
| RF04 — Histórico de entregas | ✅ Implementado |
| RF05 — Famílias aguardando | ✅ Implementado |
| RNF01 — Autenticação (Argon2id) | ✅ Implementado |

## 🖥️ Telas disponíveis

| Rota | Função |
|---|---|
| `/login` | Entrada do voluntário (única rota pública) |
| `/` | Início, com a quantidade de cestas em estoque |
| `/familias/nova` | Cadastro de família (RF01) |
| `/familias` | Lista de famílias cadastradas |
| `/familias/<id>` | Detalhes, registro de entrega (RF02/RF03) e histórico (RF04) |
| `/familias/aguardando` | Famílias aguardando atendimento (RF05) |
| `/estoque` | Consulta e entrada de cestas no estoque |

## 🔐 Segurança

- Senhas guardadas somente como hash **Argon2id** com salt (nunca em texto limpo, MD5 ou SHA-1).
- Todas as rotas, exceto `/login`, exigem voluntário autenticado, verificado no servidor.
- Sessão expira após 30 minutos de inatividade; cookie `HttpOnly` e `SameSite=Lax`.
- Consultas SQL parametrizadas e escape automático do Jinja2 contra SQL Injection e XSS.
- Em produção, defina as variáveis `SECRET_KEY` (valor aleatório) e `SESSION_COOKIE_SECURE=1` (HTTPS).

## 📝 Padrão de commits

Este repositório segue mensagens semânticas:

- `feat:` nova funcionalidade
- `fix:` correção de erro
- `test:` criação ou ajuste de testes
- `docs:` documentação

## 👤 Autor

Projeto acadêmico — Análise e Desenvolvimento de Sistemas, Cruzeiro do Sul.
