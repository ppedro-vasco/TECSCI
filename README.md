# API de Monitoramento de Usinas Fotovoltaicas

Protótipo de API REST desenvolvida como parte do processo seletivo da TECSCI, com foco em ingestão, armazenamento e análise de dados de geração de energia de usinas fotovoltaicas.

---

## Tecnologias Utilizadas

- Python 3.11+
- PostgreSQL
- `http.server` (padrão da biblioteca do Python)
- Organização em camadas (MVC)
- `dataclasses`, `typing`, `datetime`, `json`

---

## Objetivos Técnicos

- Ingerir e validar dados operacionais a partir de arquivos externos (`metrics.json`)
- Persistir os dados em um banco relacional
- Implementar uma API REST (sem frameworks) com endpoints para CRUDs e análises
- Fornecer insights operacionais: geração total, potência máxima, temperatura média

---

## Arquitetura do Projeto

/app
├── api/                ← Servidor HTTP e roteamento
│   ├── router.py       ← Roteador principal
│   └── handlers/       ← Handlers por domínio (usina, inversor, insights)
├── model/              ← Camada de acesso a dados (DAO)
├── service/            ← Camada de lógica de negócio
├── dto/                ← Data Transfer Objects para validação
├── controller/         ← (não utilizada; handlers assumem o papel de controller)
├── static/             ← Arquivos de entrada (e.g. metrics.json)
├── db/                 ← Scripts SQL e conexão com banco
├── main.py             ← Ponto de entrada do servidor

## Sobre a camada controller

- O projeto adota uma abordagem simplificada onde os arquivos em api/handlers/ assumem o papel de controladores (controller), recebendo requisições HTTP, extraindo parâmetros e encaminhando para os serviços (service).
- A pasta controller/ foi mantida por organização, mas não é usada diretamente, pois o roteamento está centralizado nos handlers, de forma adequada ao escopo sem frameworks.

## Instalação e Execução

1. Clonar o repositório
    git clone https://github.com/ppedro-vasco/TECSCI.git

2. Criar e ativar um ambiente virtual
    python -m venv .venv
    .venv\Scripts\activate  # Windows

3. Instalar dependências
    pip install -r requirements.txt

4. Configurar o banco de dados PostgreSQL
    4.1 Criar um banco monitoramento
    4.2 Rodar o script db/init.sql para criar as tabelas
    4.3 Ajustar a conexão no arquivo db/connection.py

5. Popular dados iniciais
    python app/m_setup_iniciais.py          # Popula usinas e inversores
    python app/carregar_metrics.py          # Carrega medições do metrics.json

6. Iniciar o servidor HTTP
    python app/main.py

## Endpoints Disponíveis

1. CRUD: Usinas
    Método	    Rota	        Descrição
    GET	        /usinas	        Lista todas as usinas
    POST	    /usinas	        Cria nova usina
    PUT	        /usinas	        Atualiza uma usina
    DELETE	    /usinas	        Remove uma usina

2. CRUD: Inversores
    Método	    Rota	        Descrição
    GET	        /inversores	    Lista todos os inversores
    POST	    /inversores	    Cria um novo inversor
    PUT	        /inversores	    Atualiza um inversor
    DELETE	    /inversores	    Remove um inversor

## Insights Operacionais

- Geração total por inversor
    GET /geracao/inversor?inversor_id=1&data_inicio=2025-01-01T00:00:00&data_fim=2025-01-07T23:59:59

- Geração total por usina
    GET /geracao/usina?usina_id=1&data_inicio=2025-01-01T00:00:00&data_fim=2025-01-07T23:59:59

- Potência máxima por dia
    GET /potencia-maxima?inversor_id=1&data_inicio=2025-01-01T00:00:00&data_fim=2025-01-07T23:59:59

- Temperatura média por dia
    GET /temperatura-media?inversor_id=1&data_inicio=2025-01-01T00:00:00&data_fim=2025-01-07T23:59:59

## Validação dos Dados

- Cada linha do arquivo metrics.json é validada via MedicaoDTO
- Erros de formato ou campos nulos são tratados com segurança (mas não são cadastrados no banco)
- Campos considerados: inversor_id, datetime, potencia_ativa_watt, temperatura_celsius
- Exemplo de dados não cadastrados:
    1. {'datetime': {'$date': '2025-01-07T13:58:52.428Z'}, 'inversor_id': 3, 'potencia_ativa_watt': None, 'temperatura_celsius': None} → float() argument
    2. {'datetime': {'$date': '2025-01-07T17:26:12.458Z'}, 'inversor_id': 4, 'potencia_ativa_watt': None, 'temperatura_celsius': None} → float() argument

## Modelagem do Banco

CREATE TABLE usina (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

CREATE TABLE inversor (
    id INTEGER PRIMARY KEY,
    usina_id INTEGER NOT NULL REFERENCES usina(id)
);

CREATE TABLE medicao (
    id SERIAL PRIMARY KEY,
    inversor_id INTEGER NOT NULL REFERENCES inversor(id),
    data_hora TIMESTAMP NOT NULL,
    potencia_ativa_watt REAL,
    temperatura_celsius REAL
);

CREATE UNIQUE INDEX idx_medicao_inversor_data
  ON medicao (inversor_id, data_hora);

- Essas três tabelas compõem o modelo relacional central do projeto:

    usina: identifica a planta solar
    inversor: associa inversores a uma usina
    medicao: armazena as leituras de potência e temperatura

- O índice garante que não sejam inseridas medições duplicadas para o mesmo inversor na mesma data/hora.
* Usado quando implementamos o DTO para metrics.json
* Evita duplicação ao reprocessar o arquivo JSON

- Permissões de acesso (GRANT)
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin;

* Esses comandos foram executados via pgAdmin para resolver o erro de:
    psycopg2.errors.InsufficientPrivilege: ERRO:  permissão negada para tabela usina
* Isso ocorre porque o PostgreSQL, por padrão, pode limitar permissões mesmo para tabelas criadas pelo próprio usuário.

- Criação e associação dos registros iniciais
* Este passo foi feito via código Python no arquivo m_setup_iniciais.py, que executa:
    INSERT INTO usina (nome) VALUES ('Usina 1');
    INSERT INTO usina (nome) VALUES ('Usina 2');

    INSERT INTO inversor (id, usina_id) VALUES (1, 1);
    -- ... até (8, 2)

## Descrições Técnicas

- Por que não foi usado um framework?
    * O projeto optou por não utilizar Flask, FastAPI ou Django para:
    * Demonstrar domínio da arquitetura MVC sem abstrações
    * Controlar manualmente verbos HTTP, headers, e tratamento de requisições
    * Cumprir o escopo em tempo reduzido, focando na lógica e separação de camadas

- Apesar disso, o projeto foi estruturado de forma que pode facilmente ser migrado para qualquer framework com roteamento baseado em função.

## Licença

- Esse conteúdo cobre **100% das exigências técnicas, organizacionais e documentais** que o processo seletivo descreve.
