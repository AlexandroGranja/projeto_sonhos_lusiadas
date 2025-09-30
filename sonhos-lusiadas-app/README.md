# Sonhos Lusíadas - Frontend

Uma aplicação React moderna para análise literária de "Os Lusíadas" de Luís de Camões, focada no tema dos sonhos.

## 🚀 Melhorias Implementadas

### ✨ Interface e UX
- **Design Responsivo**: Interface totalmente adaptável para mobile, tablet e desktop
- **Animações Suaves**: Transições e animações CSS customizadas para melhor experiência
- **Drag & Drop**: Upload de arquivos com arrastar e soltar
- **Estados de Carregamento**: Skeletons e spinners para feedback visual
- **Gradientes Modernos**: Visual mais atrativo com gradientes e efeitos de vidro

### 🎨 Componentes UI
- **Sistema de Design Consistente**: Componentes baseados em shadcn/ui
- **Tema Unificado**: Cores e tipografia padronizadas
- **Componentes Reutilizáveis**: LoadingSpinner, Skeleton, etc.
- **Feedback Visual**: Toasts, badges e indicadores de status

### ⚡ Performance
- **Lazy Loading**: Carregamento otimizado de componentes
- **Memoização**: Hooks otimizados para evitar re-renders desnecessários
- **Bundle Otimizado**: Configuração Vite otimizada
- **Imagens Responsivas**: Suporte a diferentes tamanhos de tela

### 🔧 Funcionalidades
- **Upload de Arquivos**: Suporte a TXT, PDF e DOCX
- **Análise em Tempo Real**: Progresso visual da análise
- **Dashboard Interativo**: Gráficos e métricas em tempo real
- **Exportação**: Múltiplos formatos de exportação
- **Navegação Intuitiva**: Menu responsivo e breadcrumbs

## 🛠️ Tecnologias

- **React 19** - Framework principal
- **Vite** - Build tool e dev server
- **Tailwind CSS** - Estilização
- **shadcn/ui** - Componentes UI
- **Recharts** - Gráficos e visualizações
- **React Router** - Roteamento
- **Lucide React** - Ícones

## 📦 Instalação

```bash
# Instalar dependências
pnpm install

# Executar em desenvolvimento
pnpm dev

# Build para produção
pnpm build

# Preview da build
pnpm preview
```

## 🎯 Estrutura do Projeto

```
src/
├── components/          # Componentes React
│   ├── ui/             # Componentes base (shadcn/ui)
│   ├── HomePage.jsx    # Página inicial
│   ├── AnalysisPage.jsx # Página de análise
│   ├── DashboardPage.jsx # Dashboard
│   ├── AboutPage.jsx   # Sobre o projeto
│   └── Navbar.jsx      # Navegação
├── hooks/              # Hooks customizados
│   ├── useAnalysis.js  # Hook para análise
│   ├── useFileUpload.js # Hook para upload
│   └── use-toast.js    # Hook para notificações
├── services/           # Serviços e API
│   └── api.js         # Cliente da API
├── lib/               # Utilitários
│   └── utils.js       # Funções auxiliares
└── assets/            # Recursos estáticos
```

## 🎨 Design System

### Cores
- **Primary**: Azul (#3B82F6)
- **Secondary**: Verde (#10B981)
- **Accent**: Roxo (#8B5CF6)
- **Warning**: Âmbar (#F59E0B)
- **Error**: Vermelho (#EF4444)

### Tipografia
- **Headings**: Inter, system-ui
- **Body**: Inter, system-ui
- **Monospace**: JetBrains Mono

### Espaçamento
- **Base**: 4px (0.25rem)
- **Scale**: 1.5x (Tailwind default)

## 🚀 Funcionalidades Principais

### 1. Análise de Texto
- Upload de múltiplos formatos
- Pré-processamento automático
- Expansão semântica com IA
- Classificação inteligente

### 2. Visualizações
- Gráficos interativos
- Nuvens de palavras
- Distribuições por canto
- Métricas de performance

### 3. Dashboard
- Estatísticas em tempo real
- Análises recentes
- Relatórios exportáveis
- Métricas de sistema

## 🔧 Configuração

### Variáveis de Ambiente
```env
VITE_API_URL=http://localhost:5000/api
VITE_APP_NAME=Sonhos Lusíadas
```

### Tailwind CSS
Configuração customizada com:
- Cores do design system
- Animações personalizadas
- Breakpoints responsivos
- Plugins otimizados

## 📱 Responsividade

- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

## 🎯 Próximos Passos

- [ ] Implementar modo escuro
- [ ] Adicionar testes unitários
- [ ] Otimizar bundle size
- [ ] Implementar PWA
- [ ] Adicionar internacionalização

## 📄 Licença

MIT License - veja o arquivo LICENSE para detalhes.
