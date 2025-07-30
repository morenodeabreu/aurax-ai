# Roadmap do AURAX

## Visão Geral
| Fase       | Duração   | Objetivo Principal                          | Entregáveis                           |
|------------|-----------|---------------------------------------------|---------------------------------------|
| **Sprint 0** | 1 semana  | MVP Funcional                               | Sistema básico com RAG + 1 modelo     |
| **Sprint 1** | 2 semanas | Autonomia Web                               | Scraping automático integrado         |
| **Sprint 2** | 3 semanas | Multi-Model                                 | Roteamento entre Qwen3 + Mistral      |
| **Sprint 3** | 4 semanas | UI Profissional                             | Interface completa com anti-abuso     |
| **Sprint 4** | 2 semanas | Escalonamento                               | Suporte a 100 usuários simultâneos    |

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
