# Task 05 — Results

**Status:** pending

### Descrição
Results é a etapa que fecha o ciclo de uma aposta. Após o sorteio ser concluído, a task Celery compara automaticamente os números de cada aposta com os números sorteados, calcula os acertos e associa o prêmio correspondente conforme as prize rules da categoria. Sem essa task, os sorteios seriam registrados mas nenhum usuário saberia se ganhou.

### Use cases
- Sistema processa automaticamente os resultados de todas as apostas após o sorteio ser fechado
- Usuário consulta sua aposta e vê quantos acertos teve e qual prêmio ganhou
- Sistema classifica cada aposta na faixa de premiação correta com base nas prize rules
- Task pode ser reexecutada sem duplicar resultados (idempotência)

## Escopo

### Model
- `BetResult`: id, bet_id, hits, prize_rule_id, processed_at
- Alternativa: adicionar campos `hits` e `prize_rule_id` diretamente no model `Bet`

### Migration
- Criar tabela `bet_results` (ou alterar `bets`)

### Task Celery — `process_draw_results(draw_id)`
- Busca todas as apostas do sorteio com status `closed`
- Para cada aposta: compara `numbers` com `drawn_numbers` do sorteio
- Conta acertos (`hits`)
- Busca `PrizeRule` da categoria com `hits` correspondente
- Salva `BetResult` com `hits`, `prize_rule_id` e `processed_at`
- Atualiza status do sorteio para `processed`

### Disparo automático
- Task disparada quando `PUT /draws/{id}/numbers` é chamado com sucesso

### Endpoints
- `GET /bets/{id}` atualizado para retornar resultado processado quando disponível (hits, prêmio ganho)

### Testes
- Aposta com todos os acertos classifica na prize rule correta
- Aposta sem acertos não gera resultado premiado
- Task idempotente: executar duas vezes não duplica resultados
- Sorteio marcado como `processed` após execução da task
