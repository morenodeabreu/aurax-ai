# AURAX Backend

Sistema autônomo de IA para geração de aplicações completas - Backend API

## Funcionalidades Implementadas

### Sprint 0 (MVP) - Concluído
- ✅ Estrutura básica do projeto com FastAPI
- ✅ Sistema RAG (Retrieval Augmented Generation) com Qdrant
- ✅ Integração com LLM (Mistral 7B via Ollama)
- ✅ Pipeline RAG + LLM para respostas contextuais
- ✅ Sistema de orquestração inteligente
- ✅ Endpoint de geração com busca de contexto e IA
- ✅ Configuração via variáveis de ambiente
- ✅ Containerização com Docker
- ✅ Tratamento robusto de erros e fallbacks

## Estrutura do Projeto

```
backend/
├── api/              # Endpoints da API (futura expansão)
├── core/             # Lógica central
│   ├── __init__.py
│   ├── orchestrator.py       # Orquestrador RAG + LLM
│   ├── rag/          # Sistema RAG
│   │   ├── __init__.py
│   │   ├── qdrant_client.py    # Cliente Qdrant
│   │   └── retriever.py        # Lógica de recuperação
│   └── llm/          # Sistema LLM
│       ├── __init__.py
│       └── ollama_client.py    # Cliente Ollama
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
- Ollama rodando em `localhost:11434` com modelo `mistral:7b-instruct-q4_K_M`
  ```bash
  # Instalar Ollama: https://ollama.ai
  ollama pull mistral:7b-instruct-q4_K_M
  ollama serve
  ```

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
Endpoint principal de geração com RAG + LLM
- **Entrada**: 
  ```json
  {
    "prompt": "sua consulta aqui",
    "model": "mistral:7b-instruct-q4_K_M",  // opcional
    "context_threshold": 0.7  // opcional, padrão 0.5
  }
  ```
- **Saída**: 
  ```json
  {
    "success": true,
    "query": "consulta original",
    "context": [{"text": "...", "score": 0.8}],
    "response": "resposta gerada pelo LLM",
    "metadata": {"context_docs_count": 2, "model_used": "mistral:7b"}
  }
  ```

### `GET /system/status`
Status completo do sistema (LLM + RAG)
- **Saída**: Informações sobre disponibilidade dos serviços, modelos disponíveis e estatísticas da base de conhecimento

### `GET /rag/info`
Informações sobre a base de conhecimento RAG (endpoint legado)

### `POST /knowledge/add`
Adicionar documentos à base de conhecimento
- **Entrada**: Lista de documentos com campo "text"

### `GET /docs`
Documentação interativa da API (Swagger)

## Configurações

Todas as configurações são gerenciadas via `../config/settings.py` usando Pydantic Settings:

### Qdrant (RAG):
- `QDRANT_URL`: URL do servidor Qdrant (padrão: `http://localhost:6333`)
- `QDRANT_COLLECTION_NAME`: Nome da collection (padrão: `aurax_knowledge_base`)
- `QDRANT_VECTOR_SIZE`: Tamanho dos vetores (padrão: 384 para all-MiniLM-L6-v2)

### Ollama (LLM):
- `OLLAMA_BASE_URL`: URL do servidor Ollama (padrão: `http://localhost:11434`)
- `DEFAULT_MODEL`: Modelo padrão (padrão: `mistral:7b-instruct-q4_K_M`)
- `OLLAMA_TIMEOUT`: Timeout para requisições (padrão: 120s)
- `MAX_TOKENS`: Máximo de tokens para geração (padrão: 2000)
- `TEMPERATURE`: Temperatura para geração (padrão: 0.7)

## Arquitetura RAG + LLM

O sistema utiliza uma arquitetura de pipeline integrada:

### Componentes RAG:
- **Qdrant**: Banco de dados vetorial para armazenamento e busca
- **sentence-transformers**: Geração de embeddings (modelo: all-MiniLM-L6-v2)
- **Busca por similaridade**: Recuperação dos top-k documentos mais relevantes

### Componentes LLM:
- **Ollama**: Servidor local para modelos de linguagem
- **Mistral 7B Instruct**: Modelo de linguagem para geração contextual
- **Pipeline RAG→LLM**: Contexto recuperado é formatado e enviado ao LLM

### Orquestração:
- **AuraxOrchestrator**: Coordena o fluxo RAG + LLM
- **Tratamento de erros**: Fallbacks quando serviços não estão disponíveis
- **Formatação inteligente**: Templates de prompt otimizados para RAG

## Próximos Passos (Sprint 1)

- [ ] Web scraping automático com Playwright para alimentar a base de conhecimento
- [ ] Pipeline de atualização automática do RAG
- [ ] Sistema de autenticação e autorização
- [ ] Rate limiting e medidas de segurança avançadas
- [ ] Monitoramento e logs estruturados

## Desenvolvimento

### Estrutura de Logs
A aplicação utiliza logging padrão do Python com níveis INFO/ERROR. Logs incluem:
- Operações RAG (busca de contexto, inserção de documentos)
- Operações LLM (geração de respostas, status do modelo)
- Erros de comunicação com serviços externos

### Tratamento de Erros
- Validação robusta de entrada com Pydantic
- Try/catch em todas as operações críticas
- Fallbacks inteligentes quando serviços não estão disponíveis
- Respostas de erro estruturadas (não HTTP exceptions)
- Verificação de disponibilidade de serviços