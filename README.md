# AURAX - Sistema Autônomo de IA

![AURAX Architecture](https://i.imgur.com/3Vx5BdR.png) <!-- Substitua por uma imagem real do seu diagrama -->

**Objetivo**: Criar um concorrente do Manus/Suna com capacidades autônomas completas usando LLMs open source.

## Visão do Sistema
- ✅ Entenda intenções complexas com 1-2 prompts
- ✅ Scanne a web automaticamente para coletar dados frescos
- ✅ Aprenda continuamente via RAG vetorial + fine-tuning
- ✅ Execute tarefas sem intervenção humana

## Tecnologias-Chave
| Categoria       | Tecnologia Escolhida      | Por Que?                                      |
|-----------------|---------------------------|-----------------------------------------------|
| **Backend**     | FastAPI + Python 3.11     | Alto desempenho para I/O intensivo            |
| **Frontend**    | Next.js 14 + Tailwind CSS | SSR para SEO + design responsivo              |
| **Banco**       | Qdrant + PostgreSQL       | Vetores + metadados estruturados              |
| **Orquestração**| LangChain + LlamaIndex    | Roteamento inteligente de modelos             |
| **Deploy**      | RunPod Serverless         | Custo otimizado para cargas variáveis         |

## Planos de Assinatura
| Recurso                     | Gratuito | Pro ($19/mês) | Master ($59/mês) |
|-----------------------------|----------|---------------|------------------|
| **Contexto Máximo**         | 8k tokens| 32k tokens    | 128k tokens      |
| **Limite de Uso**           | 10h/mês  | 55h/mês       | 170h/mês         |
| **Dispositivos**            | 1        | 1             | 2                |
| **Geração de Código**       | ✘        | ✔             | ✔                |
| **Geração de Imagens**      | ✘        | ✔ (5/dia)     | ✔ (ilimitado)    |
| **Prioridade na GPU**       | Baixa    | Média         | Alta             |
| **Suporte**                 | Comunidade| 24h          | 2h               |

## Estrutura do Projeto

```
aurax/
├── backend/          # FastAPI + RAG + Multi-LLM (Sprints 0-2 ✅)
├── frontend/         # Next.js 14 + TypeScript + Tailwind (Sprint 3 ✅)
├── config/           # Configurações e variáveis de ambiente
├── docs/             # Documentação técnica e ROADMAP
├── infrastructure/   # Docker, Kubernetes, CI/CD (futuro)
├── scripts/          # Scripts de automação e deploy
└── tests/            # Testes integrados (futuro)
```

## Status dos Sprints

### ✅ Sprint 0 (MVP) - Concluído
- Backend FastAPI com sistema RAG + Qdrant
- Integração LLM (Mistral 7B via Ollama)
- Pipeline RAG → LLM funcional
- Containerização Docker

### ✅ Sprint 1 (Autonomia Web) - Concluído  
- Web scraping autônomo com Playwright
- Processamento inteligente de conteúdo
- Integração automática scraping → RAG
- Endpoints de scraping individual e batch

### ✅ Sprint 2 (Multi-Model) - Concluído
- Sistema de roteamento inteligente de modelos
- Adaptador Qwen3 Coder para programação
- Adaptador Stable Diffusion para imagens
- Detecção automática de intenção
- API multi-modelo unificada

### ✅ Sprint 3 (UI Profissional) - Concluído
- Interface moderna com Next.js 14 + TypeScript
- Chat em tempo real com backend multi-modelo
- Design responsivo com Tailwind CSS
- Indicadores visuais por tipo de resposta
- Integração completa com API backend

## Primeiros Passos

### Backend (Sprints 0-2)
```bash
cd backend/
pip install -r requirements.txt
python main.py
# Acesse http://localhost:8000/docs para API docs
```

### Frontend (Sprint 3)  
```bash
cd frontend/
npm install
npm run dev
# Acesse http://localhost:3000 para a interface
```

### Documentação
- [Arquitetura Completa](./docs/ARCHITECTURE.md)
- [ROADMAP Detalhado](./docs/ROADMAP.md)
- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)

## Contribuindo
Contribuições são bem-vindas! Por favor, leia `CONTRIBUTING.md` (a ser criado) para detalhes sobre nosso código de conduta e o processo de envio de pedidos de pull.

## Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo `LICENSE` (a ser criado) para detalhes.

[👉 Ver Documentação Completa](./docs/ARCHITECTURE.md)
