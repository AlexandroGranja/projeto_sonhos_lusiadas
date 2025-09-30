/**
 * Serviço para comunicação com a API do backend
 * Projeto: Sonho em Os Lusíadas - Uma Análise Quantitativa e Qualitativa
 */

const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? '/api' 
  : 'http://192.168.1.14:5000/api'

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL
  }

  /**
   * Método genérico para fazer requisições HTTP
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  /**
   * Verifica a saúde da API
   */
  async healthCheck() {
    return this.request('/analysis/health')
  }

  /**
   * Faz upload de arquivo
   */
  async uploadFile(file, onProgress = null) {
    const formData = new FormData()
    formData.append('file', file)

    const config = {
      method: 'POST',
      body: formData,
      headers: {}, // Deixa o browser definir o Content-Type para FormData
    }

    // Se callback de progresso for fornecido, adiciona listener
    if (onProgress && typeof onProgress === 'function') {
      // Simula progresso para demonstração
      const simulateProgress = () => {
        let progress = 0
        const interval = setInterval(() => {
          progress += Math.random() * 30
          if (progress >= 100) {
            progress = 100
            clearInterval(interval)
          }
          onProgress(progress)
        }, 200)
      }
      simulateProgress()
    }

    return this.request('/analysis/upload', config)
  }

  /**
   * Pré-processa texto
   */
  async preprocessText(data) {
    return this.request('/analysis/preprocess', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  /**
   * Expande semanticamente o vocabulário
   */
  async expandSemantic(data) {
    return this.request('/analysis/expand-semantic', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  /**
   * Analisa contextos
   */
  async analyzeContexts(data) {
    return this.request('/analysis/analyze-contexts', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  /**
   * Gera visualizações
   */
  async generateVisualizations(data) {
    return this.request('/analysis/visualize', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  /**
   * Executa análise completa (pipeline completo)
   */
  async completeAnalysis(data, onProgress = null) {
    // Simula progresso para demonstração
    if (onProgress && typeof onProgress === 'function') {
      const steps = [
        { name: 'Pré-processamento', progress: 25 },
        { name: 'Expansão Semântica', progress: 50 },
        { name: 'Análise de Contexto', progress: 75 },
        { name: 'Geração de Visualizações', progress: 100 }
      ]

      let currentStep = 0
      const interval = setInterval(() => {
        if (currentStep < steps.length) {
          onProgress(steps[currentStep])
          currentStep++
        } else {
          clearInterval(interval)
        }
      }, 1000)
    }

    return this.request('/analysis/complete-analysis', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  /**
   * Baixa arquivo gerado
   */
  async downloadFile(filename) {
    const url = `${this.baseURL}/analysis/download/${filename}`
    
    try {
      const response = await fetch(url)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      return response.blob()
    } catch (error) {
      console.error('Download failed:', error)
      throw error
    }
  }

  /**
   * Obtém estatísticas do dashboard
   */
  async getDashboardStats() {
    // Simula dados para demonstração
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          totalAnalyses: 1247,
          totalTexts: 342,
          totalWords: 2100000,
          averageTime: 2.3,
          successRate: 96.2,
          averageConfidence: 94.1
        })
      }, 500)
    })
  }

  /**
   * Obtém dados de frequência de palavras
   */
  async getWordFrequencyData() {
    // Simula dados para demonstração
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve([
          { word: 'sonho', frequency: 45, category: 'onírico' },
          { word: 'visão', frequency: 32, category: 'profético' },
          { word: 'sombra', frequency: 28, category: 'alegórico' },
          { word: 'glória', frequency: 24, category: 'divino' },
          { word: 'pesadelo', frequency: 18, category: 'onírico' },
          { word: 'fantasia', frequency: 15, category: 'ilusão' },
          { word: 'profecia', frequency: 12, category: 'profético' },
          { word: 'miragem', frequency: 10, category: 'ilusão' }
        ])
      }, 300)
    })
  }

  /**
   * Obtém dados de distribuição por canto
   */
  async getCantoDistributionData() {
    // Simula dados para demonstração
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve([
          { canto: 'I', occurrences: 12, percentage: 15 },
          { canto: 'II', occurrences: 8, percentage: 10 },
          { canto: 'III', occurrences: 15, percentage: 19 },
          { canto: 'IV', occurrences: 6, percentage: 8 },
          { canto: 'V', occurrences: 11, percentage: 14 },
          { canto: 'VI', occurrences: 9, percentage: 11 },
          { canto: 'VII', occurrences: 7, percentage: 9 },
          { canto: 'VIII', occurrences: 5, percentage: 6 },
          { canto: 'IX', occurrences: 4, percentage: 5 },
          { canto: 'X', occurrences: 3, percentage: 4 }
        ])
      }, 300)
    })
  }

  /**
   * Obtém dados de tipos de sonho
   */
  async getDreamTypesData() {
    // Simula dados para demonstração
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve([
          { name: 'Onírico', value: 35, color: '#3B82F6' },
          { name: 'Profético', value: 28, color: '#10B981' },
          { name: 'Alegórico', value: 20, color: '#8B5CF6' },
          { name: 'Divino', value: 12, color: '#F59E0B' },
          { name: 'Ilusão', value: 5, color: '#EF4444' }
        ])
      }, 300)
    })
  }

  /**
   * Obtém análises recentes
   */
  async getRecentAnalyses() {
    // Simula dados para demonstração
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve([
          { 
            id: 1, 
            title: 'Os Lusíadas - Canto I', 
            type: 'Épico', 
            status: 'Concluído', 
            confidence: 94, 
            date: '2024-06-15',
            duration: '2.3s'
          },
          { 
            id: 2, 
            title: 'Sonetos de Camões', 
            type: 'Lírico', 
            status: 'Processando', 
            confidence: null, 
            date: '2024-06-15',
            duration: null
          },
          { 
            id: 3, 
            title: 'Auto da Barca do Inferno', 
            type: 'Teatro', 
            status: 'Concluído', 
            confidence: 87, 
            date: '2024-06-14',
            duration: '1.8s'
          },
          { 
            id: 4, 
            title: 'Mensagem - Fernando Pessoa', 
            type: 'Épico', 
            status: 'Concluído', 
            confidence: 92, 
            date: '2024-06-14',
            duration: '3.1s'
          },
          { 
            id: 5, 
            title: 'Rimas de Camões', 
            type: 'Lírico', 
            status: 'Erro', 
            confidence: null, 
            date: '2024-06-13',
            duration: null
          }
        ])
      }, 400)
    })
  }

  /**
   * Valida arquivo antes do upload
   */
  validateFile(file) {
    const allowedTypes = [
      'text/plain',
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ]
    
    const allowedExtensions = ['.txt', '.pdf', '.docx']
    const maxSize = 16 * 1024 * 1024 // 16MB

    // Verifica tipo MIME
    if (!allowedTypes.includes(file.type)) {
      // Verifica extensão como fallback
      const hasValidExtension = allowedExtensions.some(ext => 
        file.name.toLowerCase().endsWith(ext)
      )
      
      if (!hasValidExtension) {
        throw new Error('Tipo de arquivo não suportado. Use arquivos .txt, .pdf ou .docx')
      }
    }

    // Verifica tamanho
    if (file.size > maxSize) {
      throw new Error('Arquivo muito grande. O tamanho máximo é 16MB')
    }

    // Verifica se o arquivo não está vazio
    if (file.size === 0) {
      throw new Error('O arquivo está vazio')
    }

    return true
  }

  /**
   * Extrai texto de diferentes tipos de arquivo (client-side)
   */
  async extractTextFromFile(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      
      reader.onload = (event) => {
        const text = event.target.result
        resolve(text)
      }
      
      reader.onerror = () => {
        reject(new Error('Erro ao ler o arquivo'))
      }

      // Para arquivos de texto simples
      if (file.type === 'text/plain' || file.name.endsWith('.txt')) {
        reader.readAsText(file, 'utf-8')
      } else {
        // Para PDF e DOCX, o processamento será feito no backend
        reject(new Error('Processamento de PDF e DOCX deve ser feito no backend'))
      }
    })
  }

  /**
   * Formata bytes para exibição
   */
  formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes'
    
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  /**
   * Obtém ícone baseado no tipo de arquivo
   */
  getFileIcon(filename) {
    const extension = filename.toLowerCase().split('.').pop()
    
    const icons = {
      'txt': '📄',
      'pdf': '📕',
      'docx': '📘',
      'doc': '📘'
    }
    
    return icons[extension] || '📄'
  }
}

// Exporta instância singleton
export default new ApiService()
