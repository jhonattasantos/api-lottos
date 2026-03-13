# API Lottos

API REST para gerenciamento de loterias brasileiras. O sistema permite cadastrar modalidades de loteria, registrar sorteios, gerenciar apostas de usuários e apurar resultados automaticamente.

---

## O Desafio

Construir uma API capaz de suportar o ciclo completo de uma loteria:

1. Um usuário se cadastra e realiza apostas em modalidades como Mega-Sena, Quina ou Lotofácil
2. Em uma data programada, um sorteio é realizado e os números são registrados
3. O sistema processa automaticamente todas as apostas do sorteio, identifica os ganhadores e calcula os prêmios
4. O usuário consulta o resultado da sua aposta e verifica se ganhou

---

## Funcionalidades

### Autenticação
- Cadastro de usuário com e-mail e senha
- Login com retorno de JWT
- Refresh token
- Proteção de rotas autenticadas

### Categorias
- CRUD de modalidades de loteria (Mega-Sena, Quina, Lotofácil, etc.)
- Cada categoria define a quantidade de números apostados e sorteados, a faixa de números e as regras de premiação por acerto

### Sorteios
- Criação de sorteios vinculados a uma categoria com data e hora agendada
- Registro dos números sorteados
- Status do sorteio: `scheduled` → `open` → `closed` → `processed`
- Histórico completo de sorteios por categoria

### Apostas
- Registro de apostas por usuário em um sorteio aberto
- Validação dos números conforme as regras da categoria (quantidade e faixa)
- Impedimento de apostas em sorteios fechados ou já realizados
- Histórico de apostas do usuário

### Resultados
- Processamento automático via Celery após o fechamento do sorteio
- Comparação das apostas com os números sorteados
- Cálculo de acertos por aposta
- Classificação por faixa de premiação (ex: sena, quina, quadra)
- Notificação do resultado ao usuário

### Estatísticas
- Números mais sorteados por categoria
- Total arrecadado por sorteio
- Ranking de apostadores
- Histórico de premiações

---

## Stack

| Ferramenta | Função |
|---|---|
| FastAPI | Framework web |
| PostgreSQL | Banco de dados |
| SQLAlchemy (async) | ORM |
| Alembic | Migrações |
| Celery + Redis | Processamento assíncrono de resultados |
| Flower | Monitoramento de tasks |
| uv | Gerenciamento de dependências |
| Docker Compose | Orquestração dos serviços |
| pytest | Testes |

---

## Estrutura do Projeto

```
api_lottos/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── worker.py
│   ├── models/
│   │   ├── base.py
│   │   ├── category.py
│   │   ├── draw.py           # sorteios
│   │   ├── bet.py            # apostas
│   │   └── user.py
│   ├── schemas/
│   │   ├── category.py
│   │   ├── draw.py
│   │   ├── bet.py
│   │   └── user.py
│   ├── routers/
│   │   ├── health.py
│   │   ├── auth.py
│   │   ├── categories.py
│   │   ├── draws.py
│   │   └── bets.py
│   └── tasks/
│       ├── categories.py
│       └── draws.py          # processamento de resultados
├── alembic/
│   └── versions/
├── seeds/
│   ├── runner.py
│   └── categories.py
├── tests/
├── docs/
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── pyproject.toml
```

---

## Como Rodar

```bash
# Setup completo (primeira vez)
make setup

# Subir o ambiente
make up

# Monitorar tasks
make flower
```

### Serviços disponíveis

| Serviço | URL |
|---|---|
| API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Flower | http://localhost:5555 |

---

## Documentação

| Arquivo | Conteúdo |
|---|---|
| `docs/01-setup.md` | Configuração do projeto e stack |
| `docs/02-tests.md` | Estratégia e execução de testes |
| `docs/03-models-and-migrations.md` | Models SQLAlchemy e Alembic |
| `docs/04-seeds.md` | Seeds de dados iniciais |
| `docs/05-endpoints-categories.md` | Endpoints de categorias |
| `docs/06-celery-flower.md` | Tasks assíncronas com Celery |

---

## Endpoints

### Públicos
| Método | Rota | Descrição |
|---|---|---|
| GET | `/health` | Status da API |
| POST | `/auth/register` | Cadastro de usuário |
| POST | `/auth/login` | Login e geração de JWT |

### Autenticados
| Método | Rota | Descrição |
|---|---|---|
| GET | `/categories` | Lista modalidades |
| GET | `/draws` | Lista sorteios abertos |
| GET | `/draws/{id}` | Detalhe do sorteio |
| POST | `/bets` | Registrar aposta |
| GET | `/bets` | Minhas apostas |
| GET | `/bets/{id}` | Resultado da aposta |

### Admin
| Método | Rota | Descrição |
|---|---|---|
| POST | `/categories` | Criar modalidade |
| PUT | `/categories/{id}` | Editar modalidade |
| DELETE | `/categories/{id}` | Remover modalidade |
| POST | `/draws` | Criar sorteio |
| PUT | `/draws/{id}/numbers` | Registrar números sorteados |
