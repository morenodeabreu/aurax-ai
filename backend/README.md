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

### Sprint 1 (Autonomia Web) - Concluído
- ✅ Sistema de scraping web com Playwright
- ✅ Processamento inteligente de conteúdo web
- ✅ Integração automática scraping → RAG
- ✅ Endpoints de scraping (individual e batch)
- ✅ Filtragem e limpeza de conteúdo web
- ✅ Chunkização otimizada para RAG
- ✅ Suporte completo a Docker com Playwright

### Sprint 2 (Multi-Model) - Concluído
- ✅ Sistema de roteamento inteligente de modelos
- ✅ Adaptador Qwen3 Coder para tarefas de programação
- ✅ Adaptador Stable Diffusion para geração de imagens
- ✅ Detecção automática de intenção (código, imagem, texto)
- ✅ Integração multi-modelo com pipeline RAG
- ✅ Endpoint de teste de roteamento
- ✅ Fallbacks inteligentes entre modelos

## Estrutura do Projeto

```
backend/
├── api/              # Endpoints da API (futura expansão)
├── core/             # Lógica central
│   ├── __init__.py
│   ├── orchestrator.py       # Orquestrador RAG + Multi-LLM
│   ├── rag/          # Sistema RAG
│   │   ├── __init__.py
│   │   ├── qdrant_client.py    # Cliente Qdrant
│   │   └── retriever.py        # Lógica de recuperação
│   ├── llm/          # Sistema LLM base
│   │   ├── __init__.py
│   │   └── ollama_client.py    # Cliente Ollama
│   ├── model_router/ # Roteamento Inteligente
│   │   ├── __init__.py
│   │   └── router.py           # Roteador multi-modelo
│   ├── models/       # Adaptadores Especializados
│   │   ├── __init__.py
│   │   ├── qwen3_coder_adapter.py    # Qwen3 para código
│   │   └── stable_diffusion_adapter.py # Stable Diffusion
│   └── web_scraper/  # Sistema de Web Scraping
│       ├── __init__.py
│       ├── scraper.py          # Scraper com Playwright
│       ├── processor.py        # Processador de conteúdo
│       └── rag_updater.py      # Integração scraping → RAG
├── scripts/          # Scripts de instalação
│   └── install_playwright_deps.sh
├── utils/            # Utilitários gerais (futura expansão)
├── main.py           # Aplicação FastAPI principal
├── requirements.txt  # Dependências Python
└── Dockerfile        # Containerização
```

## Instalação e Execução

### Pré-requisitos
- Python 3.11+
- Qdrant rodando em `localhost:6333`
- Ollama rodando em `localhost:11434` com modelo `mistral:7b-instruct-q4_K_M`
- Playwright e dependências do navegador

#### Instalação dos Serviços:
```bash
# Instalar Ollama: https://ollama.ai
ollama pull mistral:7b-instruct-q4_K_M
ollama serve

# Instalar Qdrant via Docker:
docker run -p 6333:6333 qdrant/qdrant

# Instalar Playwright (após pip install):
playwright install chromium
playwright install-deps chromium
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
Endpoint principal de geração com roteamento multi-modelo
- **Entrada**: 
  ```json
  {
    "prompt": "Write a Python function to sort a list",
    "model": "qwen3:coder",  // opcional, usa roteamento se omitido
    "context_threshold": 0.5,  // opcional
    "routing_metadata": {"preferred_model": "code"}  // opcional
  }
  ```
- **Saída**: 
  ```json
  {
    "success": true,
    "query": "Write a Python function to sort a list",
    "context": [{"text": "sorting algorithms...", "score": 0.8}],
    "response": "def sort_list(items): return sorted(items)",
    "response_type": "code",
    "routing_info": {"model_type": "qwen3:coder", "confidence": 0.9},
    "metadata": {"context_docs_count": 2, "model_used": "qwen3:coder"}
  }
  ```

### `POST /route`
Endpoint para testar roteamento de modelos
- **Entrada**: 
  ```json
  {
    "query": "Create an image of a sunset",
    "metadata": {"category": "creative"}
  }
  ```
- **Saída**: 
  ```json
  {
    "success": true,
    "query": "Create an image of a sunset",
    "routing": {
      "model_type": "stable-diffusion",
      "confidence": 0.95,
      "reasoning": "Image generation request detected"
    }
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

### `POST /scrape`
Scraping de URL individual e adição automática à base de conhecimento
- **Entrada**: 
  ```json
  {
    "url": "https://example.com/article",
    "metadata": {"category": "tech"}  // opcional
  }
  ```
- **Saída**: 
  ```json
  {
    "success": true,
    "url": "https://example.com/article",
    "title": "Título da Página",
    "chunks_created": 5,
    "chunks_added_to_rag": 5,
    "content_length": 2500
  }
  ```

### `POST /scrape/batch`
Scraping de múltiplas URLs (máximo 10 por batch)
- **Entrada**: 
  ```json
  {
    "urls": ["https://site1.com", "https://site2.com"],
    "metadata": {"batch_id": "tech_docs_001"}
  }
  ```

### `GET /scrape/stats`
Estatísticas do conteúdo scrapeado na base de conhecimento

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

### Multi-Model System:
- Roteamento automático baseado em análise de intenção
- Suporte a modelos de código, imagem e texto
- Fallbacks inteligentes entre modelos
- Parâmetros otimizados por tipo de tarefa

### Web Scraping:
- Configurações de scraping são gerenciadas internamente
- Playwright roda em modo headless por padrão
- Timeout de 30s para carregamento de páginas
- Chunkização: 800 caracteres com overlap de 100

## Arquitetura Completa: Multi-Model AI System

O sistema utiliza uma arquitetura de pipeline integrada com roteamento inteligente:

### Roteamento Multi-Modelo:
- **ModelRouter**: Análise automática de intenção usando heurísticas avançadas
- **Detecção de Tarefas**: Identifica automáticamente código, imagens, texto geral
- **Confidence Scoring**: Sistema de confiança para decisões de roteamento
- **Fallback Inteligente**: Volta ao modelo padrão quando especializados falham

### Modelos Especializados:
- **Qwen3 Coder**: Tarefas de programação com temperatura baixa (0.3)
- **Stable Diffusion**: Geração de imagens com parâmetros otimizados
- **Mistral 7B**: Modelo padrão para tarefas gerais de texto
- **Adapters Pattern**: Interface uniforme para todos os modelos

### Componentes Web Scraping:
- **Playwright**: Navegação robusta com Chromium headless
- **Trafilatura**: Extração inteligente de conteúdo principal
- **ContentProcessor**: Limpeza, filtragem e chunkização otimizada
- **Segurança**: Validação de URLs e filtragem de conteúdo malicioso

### Componentes RAG:
- **Qdrant**: Banco de dados vetorial para armazenamento e busca
- **sentence-transformers**: Geração de embeddings (modelo: all-MiniLM-L6-v2)
- **Busca por similaridade**: Recuperação dos top-k documentos mais relevantes
- **Atualização autônoma**: Pipeline scraping → processamento → RAG

### Orquestração Avançada:
- **AuraxOrchestrator**: Coordena roteamento + RAG + multi-LLM
- **RAGUpdater**: Coordena scraping web + atualização RAG
- **Tratamento de erros**: Fallbacks robusto em todos os componentes
- **Templates Especializados**: Prompts otimizados por tipo de modelo

## Próximos Passos (Sprint 3)

- [ ] Interface gráfica profissional com Next.js
- [ ] Sistema de autenticação e autorização completo
- [ ] Painel de histórico de conversações
- [ ] Suporte a temas (claro/escuro)
- [ ] Rate limiting e medidas de segurança avançadas
- [ ] Monitoramento e logs estruturados
- [ ] Indicadores visuais de limites e bloqueios

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