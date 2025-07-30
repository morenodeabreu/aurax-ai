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

## Primeiros Passos
1.  Clone o repositório: `git clone https://github.com/seu-usuario/aurax.git`
2.  Leia a documentação em `docs/` para entender a arquitetura e os planos.
3.  Configure o ambiente de desenvolvimento conforme instruções em `docs/QUICK_START.md` (a ser criado).

## Contribuindo
Contribuições são bem-vindas! Por favor, leia `CONTRIBUTING.md` (a ser criado) para detalhes sobre nosso código de conduta e o processo de envio de pedidos de pull.

## Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo `LICENSE` (a ser criado) para detalhes.

[👉 Ver Documentação Completa](./docs/ARCHITECTURE.md)
