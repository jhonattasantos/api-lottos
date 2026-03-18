# Task 03 — Draws

**Status:** pending

### Descrição
Draws (sorteios) são o evento central da plataforma. Eles ligam uma categoria a um momento específico no tempo e controlam o ciclo de vida das apostas: quando elas podem ser feitas, quando são encerradas e quando o resultado é apurado. O gerenciamento correto dos status garante integridade entre apostas e resultados.

### Use cases
- Administrador agenda um novo sorteio para uma categoria específica
- Sistema abre o sorteio no momento programado, habilitando apostas
- Administrador encerra o período de apostas e registra os números sorteados
- Sistema processa automaticamente os resultados após o registro dos números

## Escopo

### Model
- `Draw`: id, category_id, scheduled_at, status, drawn_numbers[]
- `status`: enum com valores `scheduled`, `open`, `closed`, `processed`
- `drawn_numbers`: array de inteiros (ex: ARRAY ou JSON dependendo do banco)

### Migration
- Criar tabela `draws` com FK para `categories`

### Status lifecycle
```
scheduled → open → closed → processed
```
- `scheduled`: sorteio agendado, apostas ainda não abertas
- `open`: apostas habilitadas
- `closed`: apostas encerradas, aguardando resultado
- `processed`: resultado apurado e resultados calculados

### Endpoints
- `GET /draws` — lista sorteios (filtros por categoria, status)
- `GET /draws/{id}` — detalhe de um sorteio
- `POST /draws` — cria sorteio (admin)
- `PUT /draws/{id}/status` — atualiza status (admin)
- `PUT /draws/{id}/numbers` — registra números sorteados (admin, muda status para `processed`)

### Validações
- `drawn_numbers` deve respeitar `min_number` e `max_number` da categoria
- Quantidade de números deve ser igual a `draws` da categoria
- Não pode registrar números em sorteio que não está `closed`

### Task Celery
- Disparada após `PUT /draws/{id}/numbers` para processar resultados das apostas

### Testes
- Ciclo completo de status
- Validação de números fora da faixa
- Validação de quantidade de números incorreta
