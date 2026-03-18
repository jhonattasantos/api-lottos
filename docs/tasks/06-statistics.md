# Task 06 — Statistics

**Status:** pending

### Descrição
Statistics agrega dados históricos da plataforma para oferecer inteligência sobre os sorteios e comportamento dos usuários. Esses endpoints enriquecem a experiência do apostador (quais números saem mais?) e fornecem visibilidade operacional para o administrador (quanto foi distribuído em prêmios?). Queries pesadas podem ser cacheadas no Redis para não impactar a performance da API.

### Use cases
- Usuário consulta os números mais sorteados de uma categoria para embasar suas escolhas
- Administrador visualiza o total de prêmios distribuídos por sorteio
- Plataforma exibe um ranking público dos apostadores com mais prêmios ganhos
- Sistema retorna estatísticas de um sorteio específico: vencedores por faixa e total arrecadado

## Escopo

### Endpoints

#### `GET /categories/{id}/stats`
- Números mais sorteados na categoria (frequência histórica)
- Total de apostas realizadas
- Total de prêmios distribuídos

#### `GET /draws/{id}/stats`
- Total arrecadado no sorteio (total de apostas × valor do bilhete, se aplicável)
- Quantidade de vencedores por faixa de `PrizeRule`
- Números sorteados

#### `GET /users/ranking`
- Ranking de apostadores por prêmios ganhos
- Campos: user_id, email, total_prizes, total_hits

### Implementação
- Queries agregadas com SQLAlchemy: `func.count`, `func.sum`, `group_by`
- Joins entre `Bet`, `BetResult`, `Draw`, `Category`, `PrizeRule`
- Paginação nos endpoints de listagem

### Cache (opcional)
- Queries pesadas (frequência de números, ranking) podem ser cacheadas no Redis
- TTL curto para ranking (ex: 5 min), TTL maior para stats históricas

### Testes
- Frequência de números calculada corretamente
- Ranking ordenado por prêmios decrescente
- Stats de sorteio refletem resultados processados
