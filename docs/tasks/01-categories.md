# Task 01 — Categories

**Status:** done

### Descrição
Categories é a base de toda a aplicação. Cada categoria representa um tipo de loteria (ex: Mega-Sena, Quina) e define as regras do jogo: faixa de números, quantidade de picks e as faixas de premiação. Sem categorias configuradas, não é possível criar sorteios nem aceitar apostas.

### Use cases
- Administrador cadastra uma nova modalidade de loteria com suas regras
- Sistema lista as categorias disponíveis para o usuário escolher onde apostar
- Aplicação valida apostas e sorteios com base nas regras da categoria (min/max, picks, draws)
- Seed inicial popula as 10 loterias reais do Brasil para uso imediato

## O que foi implementado

### Models
- `Category`: id, name, slug, min_number, max_number, picks, draws
- `PrizeRule`: id, category_id, label, hits

### Migrations (Alembic)
1. Criação inicial da tabela `categories`
2. Expansão dos campos + tabela `prize_rules`
3. Adição do campo `slug`

### Seeds
- 10 loterias reais do Brasil populadas via seed
- Upsert por `slug` (idempotente)

### Endpoints
- `GET /categories` — lista todas as categorias
- `GET /categories/{id}` — busca por id
- `GET /categories/{slug}` — busca por slug
- `POST /categories` — cria categoria
- `PUT /categories/{id}` — atualiza categoria
- `DELETE /categories/{id}` — remove categoria

### Dependências adicionadas
- `python-slugify`: geração automática de slug no campo `name`

### Task Celery
- `process_after_create`: disparada automaticamente no `POST /categories`

### Testes
- Cobertura dos endpoints com mock do banco via `conftest.py`
