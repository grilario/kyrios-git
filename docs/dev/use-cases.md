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

## Autenticação de Usuário

### Descrição
Usuário informa suas credenciais para conseguir um token de acesso ao sistema facilitando próximas autenticações.

### Atores, interfaces
Atores: Usuário, Interfaces: Password Hash, User Repository, Authorization

### Fluxo

#### Criando tokens

1. Receber informações do usuário: identification - email ou username, password, user agent, IP address.
2. Checar se identification é um email ou username.
3. Buscar usuário no banco de dados.
4. Checar se senhas se coincidem.
5. Criar access token and refresh token para futuras autenticações do usuário.
6. Salvar refresh, user agent, IP address no banco de dados.
6. Retornar os tokens.

#### Revalidando access token

1. Receber informações: refresh token, user agent, IP address.
2. Buscar refresh token no banco de dados.
3. Checar se o refresh token foi expirado (2 months).
4. Gerar um novo access_token.
5. Modificar user agent, IP address salvos no banco.
6. Retornar access token gerado.

### Fluxo alternativo

#### Criando tokens

1. Caso identification não bata com validações nem de username e email retornar 403, credenciais são inválidas.
2. Caso não encontre nenhum usuário no banco de dados retornar 403, credenciais são inválidas.
3. Caso as senhas não se coincidem retornar 403, credenciais inválidas.

#### Revalidando access token

1. Caso não encontrar um refresh token retornar - 404, não encontrado.
2. Caso token foi expirado retornar - 403, token expirado.

## Recuperação de senha

### Descrição
Caso o usuário tenha perdido a senha usar email cadastrado como um método de recuperação

### Atores, interfaces
Atores: Usuário, Interfaces: User Repository, Email, Hash Password

### Fluxo

#### Código de recuperação de conta

1. Receber identification - email ou username.
2. Checar se identification é um email ou username.
3. Buscar usuário no banco de dados.
4. Gerar e armazenar um código de recuperação de 5 minutos e identification recebida associando ao usuário (armazenar um único código por usuário).
5. Enviar código para email do usuário.
6. Retornar email escondido parcialmente.

#### Código de atualização de senha

1. Receber código de recuperação, e identification recebida anteriormente.
2. Buscar no banco de dados o código, identification.
3. Checar se os dados batem, e se o código não foi expirado.
4. Gerar um código para receber posteriormente a nova senha (tempo de expiração de 5 minutos).
5. Retornar código gerado.

#### Atualização de senha

1. Receber código gerado, a nova senha e identification recebida anteriormente.
2. Buscar no banco o código a partir de identification.
3. Checar se os códigos se coincidem, e se está expirado.
4. Fazer o hash da nova senha.
5. Salvar o hash no banco de dados.
6. Retornar sucesso.

### Fluxo alternativo

#### Código de recuperação de conta

1. Caso identification não bata com validações nem de username e email retornar - usuário não encontrado.
2. Caso não encontrar nenhum usuário no banco retornar - usuário não encontrado.

#### Código de atualização de senha

1. Caso não encontrar nenhum código no banco de dados retornar - código inválido ou expirado.
2. Caso os códigos não se coincidem ou expirou retornar - código inválido ou expirado.
  
#### Atualização de senha

1. Caso não encontrar nenhum código no banco de dados retornar - código inválido ou expirado.
2. Caso os códigos não se coincidem ou expirou retornar - código inválido ou expirado.

