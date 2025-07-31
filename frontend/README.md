# AURAX Frontend

Interface de usuário moderna e responsiva para o sistema AURAX AI, construída com Next.js 14, TypeScript e Tailwind CSS.

## 🚀 Sprint 3: UI Profissional

Este projeto frontend foi desenvolvido como parte do Sprint 3 do AURAX, focando em criar uma interface profissional para interação com o sistema AI multi-modelo.

## ✨ Funcionalidades

### Interface de Chat
- **Chat em tempo real** com o sistema AURAX AI
- **Detecção automática de tipo de resposta** (texto, código, imagem)
- **Indicadores visuais** para diferentes tipos de modelo utilizados
- **Histórico de conversas** com timestamps
- **Status de conexão** em tempo real com o backend

### Integração Multi-Modelo
- Suporte completo ao **sistema de roteamento inteligente** do backend
- Visualização especializada para **código** com syntax highlighting
- Preparado para **geração de imagens** (Stable Diffusion)
- **Contexto RAG** visível com contador de documentos utilizados

### UX/UI Features
- **Design responsivo** otimizado para desktop e mobile
- **Tema moderno** com Tailwind CSS
- **Animações suaves** e transições
- **Estados de loading** e feedback visual
- **Tratamento de erros** user-friendly

## 🛠️ Tecnologias

- **Next.js 14** - React framework com App Router
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Utility-first CSS framework
- **React Hooks** - Gerenciamento de estado moderno

## 🏗️ Estrutura do Projeto

```
frontend/
├── src/
│   ├── app/                    # App Router (Next.js 14)
│   │   ├── layout.tsx         # Layout raiz da aplicação
│   │   ├── page.tsx           # Página inicial
│   │   └── globals.css        # Estilos globais + Tailwind
│   ├── components/            # Componentes React
│   │   ├── ChatInterface.tsx  # Interface principal do chat  
│   │   └── MessageBubble.tsx  # Componente de mensagem individual
│   ├── lib/                   # Utilitários e configurações
│   │   └── api.ts            # Cliente HTTP para backend API
│   └── types/                 # Definições TypeScript
│       └── api.ts            # Tipos da API backend
├── public/                    # Arquivos estáticos
├── .env.local                # Variáveis de ambiente
├── package.json              # Dependências e scripts
├── tailwind.config.ts        # Configuração Tailwind CSS
└── tsconfig.json            # Configuração TypeScript
```

## 🚀 Instalação e Execução

### Pré-requisitos
- Node.js 18+ 
- npm ou yarn
- Backend AURAX rodando em `http://localhost:8000`

### Instalação
```bash
# Navegar para o diretório frontend
cd aurax/frontend

# Instalar dependências
npm install
```

### Desenvolvimento
```bash
# Executar em modo desenvolvimento
npm run dev

# Acessar http://localhost:3000
```

### Produção
```bash
# Build para produção
npm run build

# Executar build de produção
npm start
```

### Scripts Disponíveis
```bash
npm run dev      # Desenvolvimento com hot-reload
npm run build    # Build otimizado para produção
npm start        # Executar build de produção
npm run lint     # Linting com ESLint
```

## 🔧 Configuração

### Variáveis de Ambiente
```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000  # URL do backend AURAX
NEXT_PUBLIC_APP_NAME=AURAX AI
NEXT_PUBLIC_APP_VERSION=1.0.0
```

### Integração com Backend
O frontend se conecta automaticamente com a API do backend AURAX. Certifique-se de que:

1. **Backend está rodando** em `http://localhost:8000`
2. **CORS está configurado** para permitir requisições do frontend  
3. **Endpoints estão funcionais**: `/health`, `/generate`, `/system/status`

## 📡 API Integration

### Endpoints Utilizados
- `GET /health` - Verificação de saúde do sistema
- `POST /generate` - Geração de conteúdo multi-modelo  
- `GET /system/status` - Status dos componentes (LLM, RAG)
- `POST /route` - Teste de roteamento de modelos
- `POST /scrape` - Web scraping (futuro)

### Tipos de Resposta
- **Texto**: Respostas gerais do Mistral 7B
- **Código**: Geração especializada via Qwen3 Coder
- **Imagem**: Criação via Stable Diffusion (futuro)

## 🎨 Customização

### Temas e Estilos
O projeto usa Tailwind CSS para estilização. Para customizar:

```typescript
// tailwind.config.ts
module.exports = {
  theme: {
    extend: {
      colors: {
        // Cores customizadas
      }
    }
  }
}
```

### Componentes
Todos os componentes são modulares e reutilizáveis:

```typescript
// Exemplo de uso do ChatInterface
import ChatInterface from '@/components/ChatInterface';

export default function Page() {
  return <ChatInterface className="h-screen" />;
}
```

## 🔮 Próximos Passos

### Recursos Planejados
- [ ] **Autenticação** de usuários
- [ ] **Histórico persistente** de conversas
- [ ] **Temas claro/escuro**
- [ ] **Upload de arquivos** para contexto RAG
- [ ] **Exportação** de conversas
- [ ] **Configurações** de modelo avançadas
- [ ] **Rate limiting** visual
- [ ] **PWA** (Progressive Web App)

### Melhorias Técnicas
- [ ] **Testing** com Jest e React Testing Library
- [ ] **Storybook** para documentação de componentes
- [ ] **Bundle analyzer** para otimização
- [ ] **Service Worker** para offline
- [ ] **Animações** com Framer Motion

## 🐛 Troubleshooting

### Problemas Comuns

**1. Conexão com Backend Falhando**
```bash
# Verificar se backend está rodando
curl http://localhost:8000/health

# Verificar variável de ambiente
echo $NEXT_PUBLIC_API_URL
```

**2. Erro de Build**
```bash
# Limpar cache
rm -rf .next
npm run build
```

**3. Problemas de Estilo**
```bash
# Recompilar Tailwind
npm run dev
```

## 📝 Contribuição

1. Fork do projeto
2. Criar branch para feature (`git checkout -b feature/AmazingFeature`)
3. Commit das mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para branch (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licença

Este projeto faz parte do sistema AURAX AI e segue a mesma licença do projeto principal.

---

**AURAX AI Frontend** - Interface moderna para sistemas autônomos de IA multi-modelo.