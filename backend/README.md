# AURAX Backend

Sistema autônomo de IA para geração de aplicações completas - Backend API

## Funcionalidades Implementadas

### Sprint 0 (MVP) - Concluído
- ✅ Estrutura básica do projeto com FastAPI
- ✅ Sistema RAG (Retrieval Augmented Generation) com Qdrant
- ✅ Endpoint de geração com busca de contexto
- ✅ Configuração via variáveis de ambiente
- ✅ Containerização com Docker

## Estrutura do Projeto

```
backend/
├── api/              # Endpoints da API (futura expansão)
├── core/             # Lógica central
│   └── rag/          # Sistema RAG
│       ├── __init__.py
│       ├── qdrant_client.py    # Cliente Qdrant
│       └── retriever.py        # Lógica de recuperação
├── models/           # Modelos Pydantic (futura expansão)
├── utils/            # Utilitários gerais (futura expansão)
├── main.py           # Aplicação FastAPI principal
├── requirements.txt  # Dependências Python
└── Dockerfile        # Containerização
```

## Instalação e Execução

### Pré-requisitos
- Python 3.11+
- Qdrant rodando em `localhost:6333` (ou configurado via variáveis de ambiente)

### Configuração Local

1. Instalar dependências:
```bash
pip install -r requirements.txt
```

2. Configurar variáveis de ambiente (opcional):
```bash
cp ../config/.env.example ../config/.env
# Editar ../config/.env conforme necessário
```

3. Executar a aplicação:
```bash
python main.py
```

### Docker

```bash
docker build -t aurax-backend .
docker run -p 8000:8000 aurax-backend
```

## Endpoints Disponíveis

### `GET /health`
Health check da aplicação

### `POST /generate`
Endpoint principal de geração com RAG
- **Entrada**: `{"prompt": "sua consulta aqui"}`
- **Saída**: JSON com query, contexto recuperado e resposta

### `GET /rag/info`
Informações sobre a base de conhecimento RAG

### `GET /docs`
Documentação interativa da API (Swagger)

## Configurações

Todas as configurações são gerenciadas via `../config/settings.py` usando Pydantic Settings:

- `QDRANT_URL`: URL do servidor Qdrant (padrão: `http://localhost:6333`)
- `QDRANT_COLLECTION_NAME`: Nome da collection (padrão: `aurax_knowledge_base`)
- `QDRANT_VECTOR_SIZE`: Tamanho dos vetores (padrão: 384 para all-MiniLM-L6-v2)

## Sistema RAG

O sistema utiliza:
- **Qdrant**: Banco de dados vetorial para armazenamento e busca
- **sentence-transformers**: Geração de embeddings (modelo: all-MiniLM-L6-v2)
- **Busca por similaridade**: Recuperação dos top-k documentos mais relevantes

## Próximos Passos (Sprint 1)

- [ ] Integração com modelos LLM (Mistral 7B via Ollama)
- [ ] Web scraping automático para alimentar a base de conhecimento
- [ ] Sistema de autenticação
- [ ] Rate limiting e medidas de segurança

## Desenvolvimento

### Estrutura de Logs
A aplicação utiliza logging padrão do Python. Logs são exibidos no console durante a execução.

### Tratamento de Erros
- Validação de entrada com Pydantic
- Try/catch em operações críticas
- Retorno de HTTP status codes apropriados