# Task 04 — Bets

**Status:** pending

### Descrição
Bets (apostas) são a ação principal do usuário na plataforma. É aqui que o usuário escolhe seus números e participa de um sorteio. A task garante que apenas apostas válidas sejam aceitas — respeitando regras da categoria e o status do sorteio — e que cada usuário tenha controle e visibilidade sobre suas próprias apostas.

### Use cases
- Usuário autenticado escolhe números e registra uma aposta em um sorteio aberto
- Usuário consulta o histórico de suas apostas
- Sistema rejeita apostas com números inválidos ou em sorteios já encerrados
- Sistema impede que o mesmo usuário aposte duas vezes no mesmo sorteio

## Escopo

### Model
- `Bet`: id, user_id, draw_id, numbers[], created_at
- `numbers`: array de inteiros escolhidos pelo usuário

### Migration
- Criar tabela `bets` com FK para `users` e `draws`

### Endpoints
- `POST /bets` — registra uma aposta
- `GET /bets` — lista apostas do usuário autenticado
- `GET /bets/{id}` — detalhe de uma aposta

### Validações
- Sorteio deve estar com status `open`
- Quantidade de números deve ser igual a `picks` da categoria
- Números devem estar na faixa `min_number`–`max_number` da categoria
- Números não podem se repetir dentro da mesma aposta
- Usuário não pode apostar duas vezes no mesmo sorteio

### Autenticação
- Todos os endpoints exigem `get_current_user`
- Usuário só acessa as próprias apostas

### Testes
- Aposta válida criada com sucesso
- Aposta em sorteio fechado retorna erro
- Números fora da faixa retornam erro
- Quantidade incorreta de números retorna erro
- Aposta duplicada no mesmo sorteio retorna erro
