
<div align="center">

# 🛠️ Sistema de Chamados de TI

<img
  src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&duration=3000&pause=1000&color=40C3D6&center=true&vCenter=true&width=850&lines=Sistema+de+Chamados+de+TI;Python+%7C+FastAPI+%7C+SQLite;API+REST+e+testes+automatizados;Evoluindo+para+uma+aplicacao+Full-stack"
  alt="Apresentação animada do Sistema de Chamados de TI"
/>

**Sistema para gerenciamento de chamados técnicos, desenvolvido como projeto de portfólio em Engenharia de Software.**

[![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-40C3D6?style=for-the-badge)](https://github.com/DEV-LFS/sistema-chamados-ti)
[![Testes](https://img.shields.io/badge/Testes_Locais-21_Aprovados-238636?style=for-the-badge&logo=pytest&logoColor=white)](https://github.com/DEV-LFS/sistema-chamados-ti)
[![API](https://img.shields.io/badge/API-REST-0047F7?style=for-the-badge)](https://github.com/DEV-LFS/sistema-chamados-ti)

</div>

---

## 📌 Sobre o projeto

O **Sistema de Chamados de TI** é uma aplicação para registrar, consultar, acompanhar e gerenciar solicitações de suporte técnico.

O projeto foi criado para aplicar, na prática, conceitos de **Engenharia de Software, desenvolvimento back-end, persistência de dados, APIs REST, validação de informações e testes automatizados**.

Inicialmente desenvolvido como uma aplicação executada pelo terminal, o sistema evoluiu para utilizar banco de dados SQLite e uma API REST construída com FastAPI.

O objetivo é continuar essa evolução até obter uma aplicação full-stack, com interface web integrada ao back-end.

### 🎯 Objetivos

- Desenvolver conhecimentos práticos em Python.
- Aplicar conceitos de arquitetura e organização de software.
- Implementar operações CRUD e APIs REST.
- Trabalhar com bancos de dados relacionais.
- Definir e validar regras de negócio.
- Criar testes automatizados e documentar endpoints.
- Evoluir gradualmente para uma aplicação full-stack.
- Documentar a evolução do projeto no GitHub.

> **Escopo atual:** projeto educacional e de portfólio. A API funciona localmente, mas ainda não possui autenticação, autorização de usuários ou preparação completa para uso em produção.

---

## 🚀 Tecnologias utilizadas

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)

![OpenAPI](https://img.shields.io/badge/OpenAPI-6BA539?style=for-the-badge&logo=openapiinitiative&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-4051B5?style=for-the-badge)
![HTTPX](https://img.shields.io/badge/HTTPX-35495E?style=for-the-badge)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)

</div>

| Tecnologia | Aplicação no projeto |
|---|---|
| Python | Linguagem principal |
| FastAPI | Desenvolvimento da API REST |
| SQLite | Persistência dos chamados |
| SQL | Consultas e manipulação de dados |
| Pydantic | Modelos e validação de dados |
| Pytest | Execução dos testes automatizados |
| HTTPX | Dependência utilizada nos testes da API |
| Uvicorn | Servidor ASGI para execução local |
| Swagger / OpenAPI | Documentação interativa dos endpoints |
| Git / GitHub | Versionamento e histórico de evolução |

---

## ⚙️ Funcionalidades implementadas

| Funcionalidade | Descrição | Situação |
|---|---|---|
| Criar chamado | Cadastra uma solicitação técnica | ✅ |
| Listar chamados | Consulta os registros cadastrados | ✅ |
| Buscar por ID | Localiza um chamado específico | ✅ |
| Atualizar status | Modifica o estado de um chamado | ✅ |
| Excluir chamado | Remove um registro | ✅ |
| Persistência SQLite | Armazena os dados localmente | ✅ |
| Validação de entrada na API | Verifica os dados recebidos | ✅ |
| Regras de transição | Restringe mudanças de status | ✅ |
| Tratamento HTTP | Retorna códigos apropriados | ✅ |
| Swagger/OpenAPI | Documentação automática | ✅ |
| Testes automatizados | Verificação da API e do terminal | ✅ |
| Interface web | Interação visual pelo navegador | ⏳ |
| Autenticação | Identificação de usuários | ⏳ |
| Filtros e paginação | Consultas mais específicas | ⏳ |

---

## 🔄 Fluxo dos chamados

Os chamados seguem um fluxo de estados definido pelas regras de negócio.

```mermaid
flowchart LR
    A["Aberto"] --> B["Em andamento"]
    B --> C["Resolvido"]
    C --> D["Fechado"]

    classDef etapa fill:#09318D,stroke:#40C3D6,color:#FFFFFF,stroke-width:2px;
    class A,B,C,D etapa;
```

### Regras de transição

| Status atual | Próximo status permitido |
|---|---|
| Aberto | Em andamento |
| Em andamento | Resolvido |
| Resolvido | Fechado |
| Fechado | Nenhum novo estado |

Regras adicionais:

- É permitido solicitar novamente o status atual.
- Saltos indevidos entre estados são bloqueados.
- Chamados fechados não podem ser reabertos nessa versão.
- A API retorna `HTTP 409 Conflict` para transições proibidas.
- Transições rejeitadas não devem alterar o estado armazenado.

As regras estão definidas em `status_rules.py`. A consolidação completa de sua utilização entre API e terminal está em revisão.

---

## 🗂️ Estrutura do código

```text
sistema-chamados-ti/
│
├── tests/
│   ├── test_api.py
│   └── test_main.py
│
├── .gitignore
├── api.py
├── main.py
├── status_rules.py
├── requirements.txt
└── README.md
```

### Responsabilidade dos arquivos

| Arquivo | Responsabilidade |
|---|---|
| `api.py` | Endpoints, modelos, validações e operações da API |
| `main.py` | Interface interativa executada pelo terminal |
| `status_rules.py` | Definição reutilizável das regras de transição |
| `tests/test_api.py` | Testes automatizados da API REST |
| `tests/test_main.py` | Testes automatizados do terminal |
| `requirements.txt` | Dependências Python do projeto |
| `.gitignore` | Exclusão de arquivos locais do versionamento |
| `README.md` | Documentação do projeto |

O arquivo `chamados.db` é utilizado localmente e não é versionado.

Ambientes virtuais, caches e arquivos temporários também são ignorados pelo Git.

---

## 🗄️ Modelo de dados

O projeto utiliza uma tabela chamada `chamados`.

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | INTEGER | Identificador do chamado |
| `titulo` | TEXT | Título da solicitação |
| `descricao` | TEXT | Detalhamento do problema |
| `categoria` | TEXT | Categoria do chamado |
| `prioridade` | TEXT | Baixa, Média ou Alta |
| `status` | TEXT | Estado atual |
| `data_criacao` | TEXT | Data e horário de criação |

### Estrutura SQL

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

A tabela é criada automaticamente pela aplicação quando necessário.

---

## 🌐 Endpoints da API

A API disponibiliza seis endpoints.

| Método | Endpoint | Operação |
|---|---|---|
| GET | `/` | Verificar funcionamento |
| GET | `/chamados` | Listar chamados |
| GET | `/chamados/{id_chamado}` | Buscar chamado por ID |
| POST | `/chamados` | Criar chamado |
| PATCH | `/chamados/{id_chamado}/status` | Atualizar status |
| DELETE | `/chamados/{id_chamado}` | Excluir chamado |

### Exemplo: criar um chamado

**Requisição:**

```http
POST /chamados
Content-Type: application/json
```

**Corpo JSON:**

```json
{
  "titulo": "Computador sem internet",
  "descricao": "O computador não consegue acessar nenhum site.",
  "categoria": "Rede",
  "prioridade": "Alta"
}
```

A API cadastra o chamado com status inicial `Aberto` e retorna o registro criado com HTTP 201.

### Exemplo: atualizar o status

**Requisição:**

```http
PATCH /chamados/1/status
Content-Type: application/json
```

**Corpo JSON:**

```json
{
  "status": "Em andamento"
}
```

Se a transição for válida, o registro é atualizado e a API retorna HTTP 200.

### Exemplo: transição proibida

Caso um chamado esteja `Fechado` e seja solicitada sua alteração para `Aberto`, a API retorna:

**HTTP 409 Conflict**

```json
{
  "detail": "Transição de status não permitida: 'Fechado' para 'Aberto'."
}
```

### Códigos HTTP

| Código | Significado |
|---|---|
| 200 | Operação concluída |
| 201 | Chamado criado |
| 404 | Chamado não encontrado |
| 409 | Conflito nas regras de transição |
| 422 | Erro de validação |

---

## 🧪 Testes automatizados

O projeto utiliza Pytest para validar o comportamento das funcionalidades.

<div align="center">

![Testes](https://img.shields.io/badge/Pytest-21_Testes_Aprovados-238636?style=for-the-badge&logo=pytest&logoColor=white)

</div>

### Última execução local validada

| Categoria | Casos aprovados |
|---|---:|
| API REST | 18 |
| Interface de terminal | 3 |
| **Total** | **21** |

Os testes abrangem:

- Funcionamento e operações CRUD da API.
- Validação de dados e respostas HTTP.
- Atualização válida de status.
- Bloqueio de reabertura de chamados fechados.
- Rejeição de saltos de etapas.
- Repetição do mesmo status.
- Sete casos parametrizados de transições inválidas.
- Validação de transições na interface de terminal.

Os testes utilizam bancos SQLite temporários, evitando modificar o banco principal.

> Os 21 testes foram aprovados localmente. A execução automática por GitHub Actions ainda não foi implementada.

### Executar os testes

No terminal, dentro da pasta do projeto:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Para executar somente os testes da API:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_api.py -v
```

Para executar somente os testes do terminal:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_main.py -v
```

---

## 💻 Como executar o projeto

### Pré-requisitos

- Python instalado.
- Git instalado.
- Terminal ou PowerShell.
- Editor de código, como VS Code.

### 1. Clonar o repositório

```powershell
git clone https://github.com/DEV-LFS/sistema-chamados-ti.git
cd sistema-chamados-ti
```

Enquanto o Pull Request de transições estiver em desenvolvimento, utilize a branch:

```powershell
git switch feature/status-transitions
```

### 2. Criar o ambiente virtual

```powershell
py -m venv .venv
```

### 3. Instalar as dependências

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Iniciar a API REST

```powershell
.\.venv\Scripts\python.exe -m uvicorn api:app --reload
```

A API estará disponível em:

`http://127.0.0.1:8000`

### 5. Acessar a documentação

**Swagger UI:**

`http://127.0.0.1:8000/docs`

**ReDoc:**

`http://127.0.0.1:8000/redoc`

### 6. Executar a versão de terminal

Em outro terminal, na pasta do projeto:

```powershell
.\.venv\Scripts\python.exe main.py
```

O menu permite criar, listar, consultar, atualizar e excluir chamados.

---

## 📈 Histórico de evolução

O desenvolvimento foi realizado progressivamente.

| Etapa | Evolução |
|---|---|
| 1 | Criação do sistema executado pelo terminal |
| 2 | Persistência inicial em arquivo JSON |
| 3 | Migração para SQLite |
| 4 | Implementação das operações CRUD |
| 5 | Criação da API REST com FastAPI |
| 6 | Documentação Swagger/OpenAPI |
| 7 | Validação de dados com Pydantic |
| 8 | Implementação de testes com Pytest |
| 9 | Criação de regras de transição de status |
| 10 | Testes de transições inválidas e HTTP 409 |
| 11 | Integração das regras à versão de terminal |
| 12 | Expansão da suíte para 21 testes locais |

### Desenvolvimento incremental

O objetivo não é apenas apresentar uma aplicação funcionando, mas registrar decisões, melhorias, testes e correções durante sua evolução.

O histórico de commits e Pull Requests documenta esse processo.

---

## 🧭 Próximas melhorias

### Back-end

- [ ] Finalizar a centralização das regras de negócio.
- [ ] Refatorar fixtures dos testes.
- [ ] Ampliar validações de entrada no terminal.
- [ ] Revisar consistência das atualizações concorrentes.
- [ ] Implementar filtros por categoria, prioridade e status.
- [ ] Adicionar paginação à listagem.
- [ ] Avaliar autenticação e permissões.
- [ ] Implementar integração contínua com GitHub Actions.

### Front-end

- [ ] Estruturar a interface web.
- [ ] Criar dashboard de chamados.
- [ ] Implementar formulário de abertura.
- [ ] Exibir listagem e detalhes dos chamados.
- [ ] Integrar as ações à API REST.
- [ ] Adicionar indicadores e filtros.
- [ ] Implementar feedback visual de erros e validações.

### Evoluções futuras

- [ ] Avaliar migração para PostgreSQL.
- [ ] Preparar o deploy.
- [ ] Documentar a arquitetura full-stack.
- [ ] Adicionar demonstração visual do sistema.

---

## 👨‍💻 Autor

**Luis Felipe Sebastião**

Estudante de **Ciência da Computação na Faculdade Impacta de Tecnologia**, com foco em desenvolvimento back-end e Engenharia de Software.

Este projeto está sendo desenvolvido como parte da minha evolução técnica e construção de portfólio profissional.

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-DEV--LFS-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/DEV-LFS)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Luis_Felipe-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/luis-felipe-sebastiao/)
[![Portfólio](https://img.shields.io/badge/Portfolio-Acessar-0047F7?style=for-the-badge&logo=vercel&logoColor=white)](https://portfolio-dev-lfs.vercel.app/)

---

<img
  src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=16&duration=3500&pause=1200&color=40C3D6&center=true&vCenter=true&width=700&lines=Desenvolvimento+incremental;Codigo%2C+testes+e+evolucao+continua"
  alt="Mensagem animada de encerramento"
/>

**Projeto em desenvolvimento contínuo.**

</div>
