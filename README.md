# 🚀 Apache Spark - Data Lake com MinIO

Projeto de estudo sobre **Apache Spark para Engenharia de Dados** implementando um **Data Lake** completo usando **MinIO** como storage de objetos e **JupyterLab** como ambiente de desenvolvimento.

## 📋 Sobre o Projeto

Este projeto implementa a arquitetura de **Data Lake** seguindo o padrão **Medallion Architecture** (Bronze, Silver, Gold), simulando um ambiente real de engenharia de dados com diferentes fontes de dados e formatos.

### 🏗️ Arquitetura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Landing Zone  │───▶│   Bronze Zone   │───▶│   Silver Zone   │───▶│    Gold Zone    │
│   (Dados Brutos)│    │  (Dados Limpos) │    │(Dados Process.) │    │ (Dados Finais) │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Tecnologias Utilizadas

- **🐳 Docker & Docker Compose** - Containerização do ambiente
- **📦 MinIO** - Storage de objetos compatível com S3
- **📊 JupyterLab** - Ambiente de desenvolvimento e análise
- **🐍 Python** - Linguagem principal
- **📈 Apache Spark** - Processamento distribuído (PySpark)
- **🎭 Faker** - Geração de dados sintéticos
- **📋 Pandas** - Manipulação de dados
- **🏹 PyArrow** - Formato Parquet otimizado

## 🚀 Como Executar

### Pré-requisitos

- Docker Desktop instalado e rodando
- Git instalado
- UV (gerenciador de pacotes Python) - opcional

### 1. Clone o repositório

```bash
git clone https://github.com/eduardowanderleyde/spark-module1.git
cd spark-module1
```

### 2. Inicie o ambiente

```bash
docker compose up
```

### 3. Acesse as interfaces

- **JupyterLab**: http://localhost:8888
  - Token: `password`
- **MinIO Console**: http://localhost:9001
  - Usuário: `minioadmin`
  - Senha: `minioadmin`

### 4. Execute os scripts de configuração

```bash
# Instalar dependências (se usando UV)
uv sync

# Criar buckets no MinIO
uv run src/02_setup/01_create_buckets.py

# Gerar dados de exemplo
uv run src/02_setup/02_landing_csv.py    # Dados CSV (Protheus)
uv run src/02_setup/03_landing_json.py   # Dados JSON (SAP)
uv run src/02_setup/04_landing_parquet.py # Dados Parquet (Cloud X)

# Gerar dados para outras zonas
uv run src/02_setup/03_bronze_zone.py    # Bronze Zone
uv run src/02_setup/04_silver_zone.py    # Silver Zone
uv run src/02_setup/05_gold_zone.py      # Gold Zone
```

## 📁 Estrutura do Projeto

```
spark-module1/
├── docker-compose.yml          # Configuração do ambiente
├── pyproject.toml              # Dependências Python
├── uv.lock                     # Lock file das dependências
├── README.md                   # Este arquivo
└── src/
    └── 02_setup/
        ├── 01_create_buckets.py     # Criação dos buckets
        ├── 02_landing_csv.py        # Dados CSV - Landing Zone
        ├── 03_landing_json.py       # Dados JSON - Landing Zone
        ├── 04_landing_parquet.py    # Dados Parquet - Landing Zone
        ├── 03_bronze_zone.py        # Dados limpos - Bronze Zone
        ├── 04_silver_zone.py        # Dados processados - Silver Zone
        └── 05_gold_zone.py          # Dados finais - Gold Zone
```

## 🗄️ Estrutura dos Buckets

### Landing Zone (Dados Brutos)
- **`dataway/protheus/clients/`** - Dados CSV do sistema Protheus
- **`dataway/sap/clients/`** - Dados JSON do sistema SAP
- **`dataway/cloud_x/clients/`** - Dados Parquet do sistema Cloud X

### Bronze Zone (Dados Limpos)
- **`processed/protheus/`** - Dados estruturados e limpos

### Silver Zone (Dados Processados)
- **`enriched/sap/`** - Dados enriquecidos com objetos aninhados

### Gold Zone (Dados Finais)
- **`analytics/cloud_x/`** - Dados otimizados para analytics

## 📊 Tipos de Dados Gerados

### CSV (Protheus)
- Dados estruturados de clientes
- Campos: ID, nome, email, telefone, endereço, salário, etc.

### JSON (SAP)
- Dados aninhados com objetos complexos
- Estruturas: dados_pessoais, endereco, dados_profissionais, preferencias

### Parquet (Cloud X)
- Dados otimizados com métricas calculadas
- Campos: score_credito, valor_vida_cliente, propensao_compra, etc.

## 🔧 Configurações

### MinIO
- **Porta API**: 9000
- **Porta Console**: 9001
- **Credenciais**: minioadmin / minioadmin

### JupyterLab
- **Porta**: 8888
- **Token**: password
- **Volume**: `./notebooks:/home/jovyan/work`

## 📚 Próximos Passos

1. **Análise com PySpark** - Processar dados usando Apache Spark
2. **ETL Pipelines** - Implementar pipelines de transformação
3. **Visualizações** - Criar dashboards com os dados
4. **ML Pipeline** - Implementar modelos de machine learning

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**Eduardo Wanderley**
- GitHub: [@eduardowanderleyde](https://github.com/eduardowanderleyde)

---

⭐ **Se este projeto foi útil para você, deixe uma estrela!**
