# Roadmap do AURAX - STATUS ATUAL

**✅ Sprint 0 (MVP): CONCLUÍDO** - Sistema RAG + LLM funcional  
**✅ Sprint 1 (Autonomia Web): CONCLUÍDO** - Scraping autônomo integrado  
**🎯 Sprint 2 (Multi-Model): PRÓXIMO** - Roteamento inteligente de modelos  
**📅 Sprint 3 (UI Profissional): PLANEJADO** - Interface completa  
**📅 Sprint 4 (Escalonamento): PLANEJADO** - Produção com 100 usuários  

---

## Visão Geral
| Fase       | Status | Duração   | Objetivo Principal                          | Entregáveis                           |
|------------|--------|-----------|---------------------------------------------|---------------------------------------|
| **Sprint 0** | ✅ CONCLUÍDO | 1 semana  | MVP Funcional                               | Sistema básico com RAG + 1 modelo     |
| **Sprint 1** | ✅ CONCLUÍDO | 2 semanas | Autonomia Web                               | Scraping automático integrado         |
| **Sprint 2** | 🎯 PRÓXIMO | 3 semanas | Multi-Model                                 | Roteamento entre Qwen3 + Mistral      |
| **Sprint 3** | 📅 PLANEJADO | 4 semanas | UI Profissional                             | Interface completa com anti-abuso     |
| **Sprint 4** | 📅 PLANEJADO | 2 semanas | Escalonamento                               | Suporte a 100 usuários simultâneos    |

## Detalhamento do Sprint 0 (MVP em 7 Dias)

| Dia  | Tarefa                                      | Saída Esperada                              | Responsável |
|------|---------------------------------------------|---------------------------------------------|-------------|
| 1    | Configurar RunPod Serverless                | Endpoint da API funcionando                 | DevOps      |
| 2    | Implementar RAG básico com Qdrant           | Busca vetorial retornando resultados        | Backend     |
| 3    | Integrar Mistral 7B                         | Respostas coerentes com contexto            | Backend     |
| 4    | Criar UI mínima (Next.js)                   | Interface com campo de texto + enviar       | Frontend    |
| 5    | Implementar device fingerprinting           | Bloqueio de contas compartilhadas           | Security    |
| 6    | Testes de carga (Locust)                    | Sistema suporta 10 usuários simultâneos     | QA          |
| 7    | Documentação básica                         | Guia de uso para usuários beta              | Tech Writer |

## Detalhamento do Sprint 1 (Autonomia Web - 2 Semanas)

| Semana | Tarefa                                           | Saída Esperada                                         | Responsável |
|--------|--------------------------------------------------|--------------------------------------------------------|-------------|
| 1      | Integrar Playwright para scraping web            | Navegador automatizado capaz de acessar páginas        | Backend     |
| 1      | Implementar parser de conteúdo (HTML -> texto)   | Texto estruturado extraído de páginas web              | Backend     |
| 2      | Criar pipeline de atualização do RAG             | Sistema busca, processa e insere dados no RAG sozinho  | Backend     |
| 2      | Adicionar logs e monitoramento do scraping       | Registro de atividades e possíveis erros               | DevOps      |

## Detalhamento do Sprint 2 (Multi-Model - 3 Semanas)

| Semana | Tarefa                                           | Saída Esperada                                         | Responsável |
|--------|--------------------------------------------------|--------------------------------------------------------|-------------|
| 1      | Integrar Qwen3 Coder para tarefas de código      | Sistema identifica e usa Qwen3 para prompts de código  | Backend     |
| 1      | Configurar roteamento de modelos (LangChain)     | Prompt é direcionado ao modelo correto automaticamente | Backend     |
| 2      | Adicionar Stable Diffusion para geração de imagem| Sistema gera imagens a partir de prompts               | Backend     |
| 2      | Criar interface para visualizar múltiplos tipos de saída | UI mostra texto, código e imagens de forma integrada | Frontend    |
| 3      | Otimizar uso de recursos (GPU/Memória)           | Modelos carregados e descarregados conforme necessário | Backend     |
| 3      | Testes de integração entre modelos               | Fluxos complexos (pesquisa -> código -> imagem) funcionam | QA        |

## Detalhamento do Sprint 3 (UI Profissional - 4 Semanas)

| Semana | Tarefa                                           | Saída Esperada                                         | Responsável |
|--------|--------------------------------------------------|--------------------------------------------------------|-------------|
| 1      | Redesign completo da interface (Figma)           | Protótipo de alta fidelidade                           | Designer    |
| 1      | Implementar design do Figma em Next.js           | UI profissional e responsiva                         | Frontend    |
| 2      | Adicionar sistema de autenticação (usuário/senha)| Usuários podem criar contas e fazer login             | Backend     |
| 2      | Implementar painel de histórico de conversas     | Usuários veem histórico de interações                  | Frontend    |
| 3      | Integrar sistema anti-abuso na UI                | Indicadores visuais de limites e bloqueios             | Frontend    |
| 3      | Adicionar suporte a temas (claro/escuro)         | Interface personalizável                               | Frontend    |
| 4      | Testes de usabilidade com usuários reais         | Feedback coletado e problemas identificados            | QA/UX       |
| 4      | Correções e melhorias finais                     | UI finalizada e otimizada                              | Equipe      |

## Detalhamento do Sprint 4 (Escalonamento - 2 Semanas)

| Semana | Tarefa                                           | Saída Esperada                                         | Responsável |
|--------|--------------------------------------------------|--------------------------------------------------------|-------------|
| 1      | Configurar monitoramento de performance (Grafana/Prometheus) | Métricas de CPU, memória, requisições em tempo real | DevOps      |
| 1      | Implementar auto-scaling na RunPod               | Sistema escala recursos automaticamente                | DevOps      |
| 2      | Realizar testes de carga com 100 usuários        | Sistema suporta carga sem degradação                   | QA          |
| 2      | Documentar processo de deploy e escalonamento    | Guia para operação em produção                         | DevOps      |

---

## Histórico de Conclusões

### ✅ Sprint 0 (MVP) - Concluído em Janeiro 2025

**Implementações realizadas:**
- ✅ Estrutura básica do projeto com FastAPI
- ✅ Sistema RAG (Retrieval Augmented Generation) com Qdrant
- ✅ Integração com LLM (Mistral 7B via Ollama)
- ✅ Pipeline RAG + LLM para respostas contextuais
- ✅ Sistema de orquestração inteligente
- ✅ Endpoints API: `/generate`, `/health`, `/system/status`
- ✅ Configuração via variáveis de ambiente com Pydantic Settings
- ✅ Containerização completa com Docker
- ✅ Tratamento robusto de erros e fallbacks

**Funcionalidades entregues:**
- API funcional com geração de respostas contextuais
- Base de conhecimento vetorial operacional
- Integração completa entre componentes RAG e LLM
- Sistema pronto para receber conteúdo e gerar respostas inteligentes

### ✅ Sprint 1 (Autonomia Web) - Concluído em Janeiro 2025

**Implementações realizadas:**
- ✅ Sistema de scraping web com Playwright e Chromium headless
- ✅ Processamento inteligente de conteúdo web com Trafilatura
- ✅ Pipeline de chunking otimizado para RAG (LangChain Text Splitters)
- ✅ Integração automática: Web Scraping → Processamento → RAG
- ✅ Endpoints de scraping: `/scrape`, `/scrape/batch`, `/scrape/stats`
- ✅ Filtragem avançada e limpeza de conteúdo web
- ✅ Detecção automática de tipos de conteúdo e tópicos
- ✅ Suporte completo a Docker com dependências do Playwright
- ✅ Validação de segurança para URLs

**Funcionalidades entregues:**
- Sistema completamente autônomo para enriquecer base de conhecimento
- Capacidade de scraping individual e em lote (até 10 URLs)
- Processamento inteligente que filtra ruído e mantém conteúdo relevante
- Integração perfeita com sistema RAG existente
- API expandida com funcionalidades de scraping web

**Status atual do backend AURAX:**
O backend está funcional e autônomo, com capacidades completas de:
- Geração de respostas contextuais usando RAG + LLM
- Scraping automático de conteúdo web
- Processamento e chunking inteligente de documentos
- Base de conhecimento vetorial dinâmica e expansível
- API robusta com tratamento de erros e validações de segurança

### 🎯 Próximo: Sprint 2 (Multi-Model)
Objetivo: Implementar roteamento inteligente entre múltiplos modelos LLM (Qwen3 Coder + Mistral + Stable Diffusion) para diferentes tipos de tarefas.
