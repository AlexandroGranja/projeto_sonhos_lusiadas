# 🌙 Visões Oníricas da Epopeia Lusitana: Análise Literária com IA

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://reactjs.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange.svg)]()

> [!NOTE]
> Este é um projeto de demonstração que utiliza modelos de linguagem para análise literária. A precisão e a qualidade da análise dependem da configuração e do treinamento dos modelos utilizados.

## 📖 Sobre o Projeto

O **Visões Oníricas da Epopeia Lusitana** é uma ferramenta de software completa para análise literária do tema "sonho" na obra *Os Lusíadas*, de Luís de Camões. A aplicação combina técnicas avançadas de **Processamento de Linguagem Natural (NLP)** com modelos de linguagem de última geração para oferecer uma plataforma robusta de pesquisa literária.

### 🎯 Funcionalidades Principais

- 🔍 **Análise Quantitativa**: Frequência de palavras, identificação de padrões e distribuição de termos relacionados a "sonho"
- 🧠 **Análise Qualitativa**: Classificação de contextos (onírico, profético, alegórico) e análise de função narrativa
- 🤖 **Expansão Semântica**: IA para identificar conceitos semanticamente relacionados ao tema central
- 📊 **Interface Interativa**: Upload de arquivos (.txt, .docx, .pdf) e visualização de dados em tempo real
- 📈 **Dashboard Administrativo**: Métricas detalhadas e visualizações interativas
- 🏗️ **Arquitetura Flexível**: Execução local ou em servidor de produção (VPS)

## 🔬 Como o App Funciona

### 📝 **Fluxo de Análise Completo**

1. **📁 Upload de Texto**
   - Usuário faz upload de arquivo (.txt, .docx, .pdf) ou cola texto diretamente
   - Sistema valida formato e tamanho do arquivo
   - Texto é extraído e preparado para processamento

2. **🔧 Pré-processamento**
   - Limpeza e normalização do texto
   - Tokenização e lematização com spaCy
   - Extração de sentenças e identificação de cantos (para Os Lusíadas)
   - Remoção de stopwords e caracteres especiais

3. **🧠 Expansão Semântica**
   - **Claude Sonnet 4**: Análise literária qualitativa para identificar palavras relacionadas
   - **NLP Tradicional**: Técnicas focadas especificamente no termo "sono" e termos relacionados
   - **Gemini Validator**: Validação e refinamento automático dos resultados
   - **Análise de Coocorrência**: Identificação de termos que aparecem juntos
   - Combinação de todos os métodos para vocabulário expandido

4. **🔍 Análise de Contexto**
   - Busca por ocorrências das palavras expandidas no texto
   - Extração de contextos com janela configurável
   - Identificação do canto onde cada ocorrência aparece
   - Classificação automática usando IA

5. **📊 Geração de Visualizações**
   - Gráficos de frequência de palavras
   - Distribuição por canto
   - Classificação de tipos de sonho
   - Word clouds interativos
   - Dashboard com métricas em tempo real

### 🎨 **Tipos de Sonho Identificados**

- **🌙 Onírico**: Sonhos, pesadelos, devaneios
- **🔮 Profético**: Visões, presságios, augúrios
- **🎭 Alegórico**: Símbolos, metáforas, alegorias
- **✨ Divino**: Revelações, aparições divinas
- **👁️ Ilusão**: Quimeras, miragens, falsas aparências

### 🛠️ **Tecnologias de IA Utilizadas**

- **Claude Sonnet 4**: Análise literária qualitativa e classificação de contextos
- **NLP Tradicional**: Técnicas focadas especificamente no termo "sono" e termos relacionados
- **spaCy**: Processamento de linguagem natural em português
- **NLTK**: Análise de texto e recursos linguísticos
- **Pandas**: Manipulação e análise de dados
- **Matplotlib/Plotly**: Geração de visualizações interativas
- **Gemini Validator**: Validação e refinamento dos resultados

## 🏗️ Arquitetura do Sistema

O projeto é dividido em dois componentes principais que se comunicam através de uma API RESTful:

### 🔧 Backend (Flask + Python)
- **API RESTful**: Endpoints para upload, processamento e análise de textos
- **Processamento NLP**: spaCy e NLTK para tokenização, lematização e análise
- **Análise Semântica**: Integração com Claude Sonnet 4 para expansão semântica
- **Gerenciamento de Dados**: Pandas para manipulação e armazenamento de resultados

### 🎨 Frontend (React + Vite)
- **Interface Moderna**: Componentes responsivos para upload e visualização
- **Dashboard Interativo**: Gráficos e métricas em tempo real
- **Comunicação API**: Integração completa com o backend

## 🚀 Como Ativar o Projeto

### 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.11+** ([Download](https://python.org/downloads/))
- **Node.js 18+** e **npm** ([Download](https://nodejs.org/))
- **Git** ([Download](https://git-scm.com/downloads))
- **Chave da API Anthropic** ([Obter aqui](https://console.anthropic.com/))

> ⚠️ **Importante**: O projeto foi testado e está funcionando corretamente. Certifique-se de seguir todos os passos para evitar problemas de configuração.

### 🔧 Passo 1: Clonar o Repositório

   ```bash
# Clone o repositório
git clone https://github.com/AlexandroGranja/projeto_sonhos_lusiadas.git

# Navegue para o diretório do projeto
cd projeto_sonhos_lusiadas
```

### 🐍 Passo 2: Configurar o Backend (Python)

   ```bash
# 1. Navegue para o diretório do backend
cd sonhos-lusiadas-backend

# 2. Crie um ambiente virtual
python -m venv venv

# 3. Ative o ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
   source venv/bin/activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Configure as variáveis de ambiente
# Crie o arquivo .env
echo "ANTHROPIC_API_KEY=sua_chave_de_api_aqui" > .env
echo "SECRET_KEY=sonhos-lusiadas-secret-key-2024" >> .env
echo "CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://192.168.1.14:5173" >> .env

# 6. Execute o servidor Flask
python src/main.py
```

✅ **Backend rodando em:** `http://localhost:5000` ou `http://192.168.1.14:5000`

### ⚛️ Passo 3: Configurar o Frontend (React)

   ```bash
# 1. Abra um NOVO terminal e navegue para o frontend
cd sonhos-lusiadas-app

# 2. Instale as dependências
npm install

# 3. Execute a aplicação React
npm run dev
```

✅ **Frontend rodando em:** `http://localhost:5173` ou `http://192.168.1.14:5173`

> 🔧 **Nota**: O frontend está configurado para se conectar automaticamente ao backend. Se você estiver usando um IP diferente, edite o arquivo `src/services/api.js` e altere a URL do backend.

### 🔑 Passo 4: Configurar a API Key

1. Acesse [console.anthropic.com](https://console.anthropic.com/)
2. Crie uma conta ou faça login
3. Gere uma nova API key
4. Edite o arquivo `.env` no backend e substitua `sua_chave_de_api_aqui` pela sua chave:
   ```
   ANTHROPIC_API_KEY=sk-proj-sua_chave_real_aqui
   ```

### ✅ Passo 5: Verificar a Instalação

1. **Backend**: Verifique se está rodando em `http://localhost:5000` ou `http://192.168.1.14:5000`
2. **Frontend**: Acesse `http://localhost:5173` ou `http://192.168.1.14:5173` no seu navegador
3. **Teste**: Faça upload de um arquivo de texto ou cole texto diretamente
4. **Análise**: Clique em "Iniciar Análise" e aguarde o processamento

> ✅ **Status**: O projeto foi testado e está funcionando corretamente. Todos os problemas de configuração foram resolvidos.

## 🎮 Como Usar o App

### 📁 **Upload de Arquivos**

1. **Arraste e solte** um arquivo (.txt, .docx, .pdf) na área de upload
2. **Ou clique** para selecionar um arquivo do seu computador
3. **Ou cole** o texto diretamente na área de texto

### 🔍 **Processo de Análise**

1. **Pré-processamento**: O texto é limpo e preparado
2. **Expansão Semântica**: IA identifica palavras relacionadas a "sonho"
3. **Busca de Contextos**: Sistema encontra ocorrências no texto
4. **Classificação**: Cada contexto é classificado automaticamente
5. **Visualização**: Gráficos e métricas são gerados

### 📊 **Interpretando os Resultados**

- **Frequência de Palavras**: Quais termos aparecem mais
- **Distribuição por Canto**: Onde os sonhos aparecem na obra
- **Classificação**: Tipo de sonho (onírico, profético, etc.)
- **Contextos**: Frases onde as palavras aparecem
- **Métricas**: Estatísticas gerais da análise

### 🎯 **Dicas de Uso**

- **Para Os Lusíadas**: Use o texto completo para melhor análise
- **Para outros textos**: Funciona com qualquer obra literária
- **Tamanho ideal**: Textos entre 1.000 e 50.000 palavras
- **Formatos suportados**: .txt, .docx, .pdf

## ⚡ Ativação Rápida

### 🚀 **Scripts de Inicialização Automática**

**Windows:**
```bash
# Execute o script de inicialização
scripts\start_project.bat
```

**Linux/Mac:**
```bash
# Torne o script executável e execute
chmod +x scripts/start_project.sh
./scripts/start_project.sh
```

### 🚀 **Comandos Manuais**

**Terminal 1 - Backend:**
   ```bash
cd sonhos-lusiadas-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=sua_chave_aqui" > .env
echo "CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://192.168.1.14:5173" >> .env
python src/main.py
   ```

**Terminal 2 - Frontend:**
   ```bash
   cd sonhos-lusiadas-app
npm install
npm run dev
```

### 🌐 **Acessar a Aplicação**

- **Frontend**: http://localhost:5173 ou http://192.168.1.14:5173
- **Backend API**: http://localhost:5000 ou http://192.168.1.14:5000
- **Health Check**: http://localhost:5000/api/analysis/health

### 📱 **Interface do Usuário**

1. **Página Inicial**: Visão geral do projeto
2. **Análise**: Upload e processamento de textos
3. **Dashboard**: Visualizações e métricas
4. **Sobre**: Informações do projeto

### 🔧 **Endpoints da API**

- `POST /api/analysis/upload` - Upload de arquivos
- `POST /api/analysis/preprocess` - Pré-processamento
- `POST /api/analysis/expand-semantic` - Expansão semântica
- `POST /api/analysis/analyze-contexts` - Análise de contextos
- `POST /api/analysis/complete-analysis` - Análise completa
- `GET /api/analysis/health` - Status da API

### 🐛 Solução de Problemas

> ✅ **Problemas Resolvidos**: Os seguintes problemas foram identificados e corrigidos automaticamente:
> - Configuração de URL do backend (localhost vs IP)
> - Endpoint de visualização incorreto
> - Configuração de CORS para aceitar requisições do frontend
> - Componente Toaster faltante
> - Arquivo CSS vazio (configurações do Tailwind)
> - Configuração do Tailwind CSS faltante

**Erro de dependências Python:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Erro de dependências Node.js:**
   ```bash
npm cache clean --force
rm -rf node_modules package-lock.json
   npm install
   ```

**Erro de API Key:**
- Verifique se a chave está correta no arquivo `.env`
- Certifique-se de que o arquivo `.env` está na pasta `sonhos-lusiadas-backend`
- Teste a chave em: https://console.anthropic.com/

**Backend não inicia:**
```bash
# Verifique se está no diretório correto
cd sonhos-lusiadas-backend
# Verifique se o arquivo main.py existe
ls src/main.py
# Execute com debug
python -c "import sys; print(sys.path)"
```

**Frontend não carrega:**
   ```bash
# Verifique se está no diretório correto
cd sonhos-lusiadas-app
# Verifique se package.json existe
ls package.json
# Reinstale dependências
npm install --force
```

**Erro de CORS (Cross-Origin):**
- O backend está configurado para aceitar requisições de `localhost:5173` e `192.168.1.14:5173`
- Se você estiver usando um IP diferente, edite o arquivo `.env` no backend e adicione seu IP

**Erro de conexão entre frontend e backend:**
- Verifique se ambos estão rodando simultaneamente
- Confirme se as URLs estão corretas no arquivo `src/services/api.js`
- Teste a conexão acessando `http://localhost:5000` no navegador

## 📚 Manual do Usuário

### 🔍 Como Usar a Análise

1. **📁 Upload de Arquivo**
   - Arraste e solte arquivos `.txt`, `.docx` ou `.pdf`
   - Ou clique para selecionar arquivos do seu computador

2. **✍️ Entrada de Texto**
   - Cole texto diretamente na área de texto
   - Ideal para trechos específicos ou textos pequenos

3. **🚀 Iniciar Análise**
   - Clique em "Iniciar Análise" após fornecer o texto
   - O sistema processará automaticamente

4. **📊 Acompanhar Progresso**
   - Visualize cada etapa do processamento em tempo real
   - Aguarde a conclusão da análise

5. **📈 Visualizar Resultados**
   - Métricas quantitativas (frequência, distribuição)
   - Análises qualitativas (contextos, simbolismos)
   - Gráficos interativos e visualizações

### 📊 Dashboard Administrativo

- **📈 Métricas Gerais**: Total de análises, palavras processadas, tempo médio
- **📊 Gráficos Interativos**: Frequência de palavras, distribuição por canto
- **🏷️ Classificação de Sonhos**: Tipos identificados (onírico, profético, alegórico)
- **📄 Relatórios**: Exportação de dados para pesquisas acadêmicas

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.11+** - Linguagem principal
- **Flask** - Framework web
- **spaCy** - Processamento de linguagem natural
- **NLTK** - Análise de texto
- **Pandas** - Manipulação de dados
- **Anthropic API** - Claude Sonnet 4
- **NLP Tradicional** - Técnicas focadas no termo "sono"
- **Gemini API** - Validação e refinamento de resultados

### Frontend
- **React 18+** - Biblioteca de interface
- **Vite** - Build tool e dev server
- **Tailwind CSS** - Estilização
- **Chart.js** - Visualizações de dados
- **Axios** - Comunicação com API

## 📁 Estrutura do Projeto

```
projeto_sonhos_lusiadas/
├── 📁 sonhos-lusiadas-backend/     # Backend Flask
│   ├── 📁 src/
│   │   ├── main.py                 # Servidor principal
│   │   ├── 📁 routes/              # Endpoints da API
│   │   ├── 📁 models/              # Modelos de dados
│   │   └── 📁 database/            # Banco de dados
│   └── requirements.txt            # Dependências Python
├── 📁 sonhos-lusiadas-app/         # Frontend React
│   ├── 📁 src/
│   │   ├── 📁 components/          # Componentes React
│   │   ├── 📁 hooks/               # Custom hooks
│   │   └── 📁 services/            # Serviços de API
│   └── package.json                # Dependências Node.js
├── 📁 data/                        # Dados do projeto
│   └── 📁 raw/
│       └── os_lusiadas.txt         # Texto original
├── 📁 docs/                        # Documentação
│   ├── MANUAL_USUARIO.md           # Manual do usuário
│   ├── MELHORIAS_IMPLEMENTADAS.md  # Melhorias implementadas
│   └── 📁 relatorios/              # Relatórios de análise
├── 📁 scripts/                     # Scripts de inicialização
│   ├── start_project.bat           # Script Windows
│   └── start_project.sh            # Script Linux/Mac
├── 📁 analysis_results/            # Resultados de análises
├── project_config.json             # Configuração do projeto
├── env.example                     # Exemplo de variáveis de ambiente
└── README.md                       # Este arquivo
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Alexandro Granja**
- GitHub: [@AlexandroGranja](https://github.com/AlexandroGranja)
- LinkedIn: [Alexandro Granja](https://linkedin.com/in/alexandro-granja)

## 🙏 Agradecimentos

- Luís de Camões pela obra *Os Lusíadas*
- Anthropic pelo modelo Claude Sonnet 4
- Comunidade open source pelas bibliotecas utilizadas

## 📝 Exemplos Práticos

### 🌟 **Exemplo 1: Análise de Os Lusíadas**

1. **Upload**: Faça upload do arquivo `os_lusiadas.txt`
2. **Processamento**: Aguarde a análise automática com NLP tradicional
3. **Resultados**: Visualize:
   - Análise focada no termo "sono" e termos relacionados
   - Contextos classificados (onírico, profético, alegórico, divino, ilusório)
   - Validação automática com Gemini
   - Distribuição por cantos
   - Download com nome criativo: "visoes_oniricas_epopeia_YYYYMMDD_HHMMSS.pdf"

### 📊 **Exemplo 2: Análise de Texto Personalizado**

1. **Texto**: Cole um trecho de qualquer obra literária
2. **Análise**: Sistema identifica automaticamente palavras relacionadas
3. **Classificação**: Contextos são categorizados por tipo de sonho
4. **Visualização**: Gráficos mostram padrões encontrados

### 🎯 **Exemplo 3: Dashboard Interativo**

1. **Acesse**: http://localhost:5173/dashboard
2. **Explore**: Gráficos de frequência e distribuição
3. **Interaja**: Clique nos elementos para detalhes
4. **Exporte**: Baixe visualizações em PNG/HTML

## 🔬 Casos de Uso

### 👨‍🎓 **Para Pesquisadores**
- Análise quantitativa de temas literários
- Identificação de padrões em obras clássicas
- Geração de dados para publicações acadêmicas

### 👩‍🏫 **Para Professores**
- Material didático interativo
- Demonstração de análise literária
- Exercícios práticos com estudantes

### 📚 **Para Estudantes**
- Compreensão de análise textual
- Visualização de conceitos literários
- Ferramenta de estudo e pesquisa

## 📊 Status Atual do Projeto

### ✅ **Funcionalidades Implementadas e Testadas**
- [x] Backend Flask com API RESTful completa
- [x] Frontend React com interface moderna e responsiva
- [x] Upload de arquivos (.txt, .docx, .pdf)
- [x] Pré-processamento de texto com spaCy
- [x] Expansão semântica com Claude Sonnet 4
- [x] **Sistema NLP Tradicional** focado no termo "sono"
- [x] **Validação com Gemini** para refinamento de resultados
- [x] Análise de contextos e classificação automática
- [x] **Categorização expandida** (onírico, profético, alegórico, divino, ilusório)
- [x] Geração de visualizações interativas
- [x] Dashboard administrativo
- [x] **Nomes de arquivo criativos** para downloads
- [x] **Relatórios limpos** sem data de geração
- [x] Configuração de CORS para desenvolvimento
- [x] Componentes UI completos (Tailwind CSS)
- [x] Sistema de notificações (Toaster)

### 🔧 **Problemas Resolvidos Recentemente**
- ✅ Configuração de URL do backend (localhost vs IP)
- ✅ Endpoint de visualização incorreto
- ✅ Configuração de CORS para aceitar requisições do frontend
- ✅ Componente Toaster faltante
- ✅ Arquivo CSS vazio (configurações do Tailwind)
- ✅ Configuração do Tailwind CSS faltante

### 🆕 **Melhorias Implementadas (Dezembro 2024)**
- ✅ **Novo Título Criativo**: "Visões Oníricas da Epopeia Lusitana"
- ✅ **Sistema NLP Tradicional**: Foco específico no termo "sono" e termos relacionados
- ✅ **Validação com Gemini**: Refinamento automático dos resultados
- ✅ **Nomes de Arquivo Criativos**: Downloads com nomes mais elegantes
- ✅ **Remoção de Data**: Relatórios mais limpos sem data de geração
- ✅ **Categorização Expandida**: Nova categoria "ilusório" para análise mais precisa
- ✅ **Técnicas Avançadas**: Tokenização, lematização, coocorrência e similaridade

## 🚀 Próximos Passos

### 🔮 **Funcionalidades Futuras**
- [ ] Análise de outras obras literárias
- [ ] Comparação entre textos
- [ ] Exportação de relatórios em PDF
- [ ] API para integração com outros sistemas
- [ ] Análise de sentimento
- [ ] Detecção de temas automática
- [ ] Sistema de autenticação de usuários
- [ ] Banco de dados para persistência de análises

### 🤝 **Contribuindo**
1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Abra um Pull Request

---

*Desenvolvido com ❤️ para a análise literária e pesquisa acadêmica*

**🎉 O projeto está 100% funcional e pronto para uso!**

> 📝 **Última atualização**: Dezembro 2024 - Sistema atualizado com novo título criativo, NLP tradicional focado no sono, validação com Gemini e nomes de arquivo elegantes.