# Sistema de Chamados de TI

API REST desenvolvida para gerenciamento de chamados técnicos de Tecnologia da Informação.

O projeto permite criar, consultar, atualizar e excluir chamados, utilizando Python, FastAPI e SQLite. A API possui validação de dados, documentação automática com Swagger e testes automatizados com Pytest.

## Funcionalidades

* Criar chamados técnicos
* Listar todos os chamados
* Buscar chamado por ID
* Atualizar o status de um chamado
* Excluir chamados
* Validar dados de entrada
* Retornar erros HTTP apropriados
* Documentar endpoints automaticamente com Swagger
* Executar testes automatizados

## Tecnologias utilizadas

* Python
* FastAPI
* Pydantic
* SQLite
* SQL
* Uvicorn
* Pytest
* HTTPX
* Git e GitHub
* Swagger / OpenAPI

## Estrutura do projeto

```text
sistema-chamados-ti/
├── tests/
│   └── test_api.py
├── .gitignore
├── api.py
├── main.py
├── README.md
└── requirements.txt
```

### Arquivos principais

* `api.py`: API REST desenvolvida com FastAPI
* `main.py`: versão do sistema executada pelo terminal
* `tests/test_api.py`: testes automatizados da API
* `requirements.txt`: dependências do projeto
* `.gitignore`: arquivos e pastas ignorados pelo Git

## Modelo de chamado

Cada chamado possui os seguintes campos:

| Campo          | Tipo    | Descrição                                  |
| -------------- | ------- | ------------------------------------------ |
| `id`           | inteiro | Identificador único                        |
| `titulo`       | texto   | Título do problema                         |
| `descricao`    | texto   | Descrição detalhada                        |
| `categoria`    | texto   | Categoria do chamado                       |
| `prioridade`   | texto   | Baixa, Média ou Alta                       |
| `status`       | texto   | Aberto, Em andamento, Resolvido ou Fechado |
| `data_criacao` | texto   | Data e hora de criação                     |

## Endpoints

| Método   | Endpoint                        | Descrição                          |
| -------- | ------------------------------- | ---------------------------------- |
| `GET`    | `/`                             | Verifica se a API está funcionando |
| `GET`    | `/chamados`                     | Lista todos os chamados            |
| `GET`    | `/chamados/{id_chamado}`        | Busca um chamado pelo ID           |
| `POST`   | `/chamados`                     | Cria um novo chamado               |
| `PATCH`  | `/chamados/{id_chamado}/status` | Atualiza o status                  |
| `DELETE` | `/chamados/{id_chamado}`        | Exclui um chamado                  |

## Exemplo de criação de chamado

Requisição:

```http
POST /chamados
```

Corpo JSON:

```json
{
  "titulo": "Computador sem acesso à internet",
  "descricao": "O computador não consegue acessar nenhum site.",
  "categoria": "Rede",
  "prioridade": "Alta"
}
```

Resposta esperada:

```json
{
  "id": 1,
  "titulo": "Computador sem acesso à internet",
  "descricao": "O computador não consegue acessar nenhum site.",
  "categoria": "Rede",
  "prioridade": "Alta",
  "status": "Aberto",
  "data_criacao": "2026-06-23 20:55:43"
}
```

## Exemplo de atualização de status

Requisição:

```http
PATCH /chamados/1/status
```

Corpo JSON:

```json
{
  "status": "Em andamento"
}
```

## Códigos HTTP utilizados

| Código | Significado                    |
| -----: | ------------------------------ |
|  `200` | Operação realizada com sucesso |
|  `201` | Chamado criado com sucesso     |
|  `404` | Chamado não encontrado         |
|  `422` | Dados enviados são inválidos   |

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta:

```bash
cd sistema-chamados-ti
```

### 2. Criar o ambiente virtual

No Windows:

```powershell
py -m venv .venv
```

### 3. Ativar o ambiente virtual

No PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Caso o PowerShell bloqueie a ativação:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Depois tente ativar novamente:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar as dependências

```powershell
python -m pip install -r requirements.txt
```

### 5. Executar a API

```powershell
python -m uvicorn api:app --reload
```

A API estará disponível em:

```text
http://127.0.0.1:8000
```

## Documentação Swagger

Com a API em execução, acesse:

```text
http://127.0.0.1:8000/docs
```

A documentação alternativa ReDoc está disponível em:

```text
http://127.0.0.1:8000/redoc
```

## Executar os testes automatizados

Na raiz do projeto:

```powershell
python -m pytest -v
```

Resultado esperado:

```text
8 passed
```

Os testes utilizam um banco SQLite temporário e não alteram o banco de desenvolvimento.

## Testes implementados

* Verificação do funcionamento da API
* Criação de chamado
* Listagem de chamados
* Busca de chamado por ID
* Busca de chamado inexistente
* Atualização de status
* Validação de status inválido
* Exclusão de chamado

## Banco de dados

O projeto utiliza SQLite.

A tabela `chamados` é criada automaticamente quando a aplicação é iniciada.

Estrutura da tabela:

```sql
CREATE TABLE IF NOT EXISTS chamados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    categoria TEXT NOT NULL,
    prioridade TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Aberto',
    data_criacao TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

O arquivo local `chamados.db` não é enviado ao GitHub, pois está configurado no `.gitignore`.

## Histórico de evolução

O projeto foi desenvolvido progressivamente:

1. Sistema de chamados executado no terminal
2. Persistência de dados em arquivo JSON
3. Migração para banco de dados SQLite
4. Implementação de busca, atualização e exclusão
5. Criação da API REST com FastAPI
6. Documentação automática com Swagger
7. Validação de dados com Pydantic
8. Tratamento de erros HTTP
9. Testes automatizados com Pytest

## Próximas melhorias

* Separar o projeto em módulos
* Implementar autenticação de usuários
* Adicionar responsáveis pelos chamados
* Adicionar filtros por prioridade, categoria e status
* Implementar paginação
* Utilizar PostgreSQL
* Criar interface web
* Executar deploy da API
* Adicionar integração contínua com GitHub Actions

## Autor

Desenvolvido por Luis Felipe como projeto de portfólio durante a graduação em Ciência da Computação.
