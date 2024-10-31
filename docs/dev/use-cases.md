# Casos de Uso
Documento contendo os casos de uso para desenvolvimento da API do sistema.

## Cadastro de Usuário

### Descrição
Um novo usuário se cadastra no sistema informando suas informações básicas

### Atores, interfaces
Atores: Usuário, Interfaces: Password Hash, User Repository

### Fluxo

1. Receber informações do usuário: username, name, email, password
2. Validação dos dados: username não pode conter menos de 2 caracteres e mais de 30, somente pode conter letras, números e ponto e underscores, e devem ser únicos no sistema. Name deve conter pelo menos 2 caracteres e no máximo 150. Verificar se o email informado é um email com formato válido. A senha deve deve conter no minimo 8 caracteres e no máximo 80, conter pelo menos uma letra maiúscula, uma minuscula, um número e um símbolo.
3. Fazer o hash da senha.
4. Salvar as informações no banco de dados.
5. Responder com mensagem de sucesso.

### Fluxo alternativo

1. Caso ocorra erro na validação dos dados, informar uma mensagem com explicação do erro.
2. Caso ocorra erro no hash ou ao salvar as informações, informar um mensagem de erro interno no sistema. 

