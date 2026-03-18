# Task 02 — Authentication

**Status:** pending

### Descrição
Autenticação é o pré-requisito para qualquer interação personalizada na plataforma. Sem ela, não é possível associar apostas a usuários, proteger rotas administrativas ou controlar acesso a dados sensíveis. O fluxo JWT com refresh token garante sessões seguras sem exigir reautenticação frequente.

### Use cases
- Usuário cria uma conta com e-mail e senha para começar a apostar
- Usuário faz login e recebe tokens para autenticar as próximas requisições
- Cliente renova o access token expirado usando o refresh token, sem precisar logar novamente
- Rotas de administração e apostas rejeitam requisições sem token válido

## Escopo

### Model
- `User`: id, email, password_hash, created_at

### Migration
- Criar tabela `users`

### Dependências a adicionar
- `python-jose` ou `PyJWT` — geração e validação de JWT
- `passlib[bcrypt]` ou `bcrypt` — hashing de senha

### Endpoints
- `POST /auth/register` — cadastro de novo usuário
- `POST /auth/login` — autenticação, retorna access + refresh token
- `POST /auth/refresh` — renova access token via refresh token

### JWT
- Geração de access token (curta duração) e refresh token (longa duração)
- Validação de assinatura e expiração
- Payload com `sub` (user_id) e `exp`

### Dependency
- `get_current_user`: dependency FastAPI para proteger rotas autenticadas
- Extrai e valida Bearer token do header `Authorization`

### Testes
- Registro com e-mail duplicado retorna erro
- Login com senha errada retorna 401
- Acesso a rota protegida sem token retorna 401
- Refresh token válido e inválido
