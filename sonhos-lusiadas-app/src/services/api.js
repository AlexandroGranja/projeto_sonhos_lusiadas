const API_BASE_URL = 'http://localhost:5000/api/analysis'

class ApiService {
  async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`)
      return await response.json()
    } catch (error) {
      console.error('Erro ao verificar saúde da API:', error)
      throw error
    }
  }

  async uploadFile(file) {
    try {
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await fetch(`${API_BASE_URL}/upload`, {
        method: 'POST',
        body: formData
      })
      
      if (!response.ok) {
        throw new Error(`Erro no upload: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Erro no upload do arquivo:', error)
      throw error
    }
  }

  async completeAnalysis(text, mode = 'estrito') {
    try {
      const response = await fetch(`${API_BASE_URL}/complete-analysis`, {
      method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text, mode })
      })
      
      if (!response.ok) {
        throw new Error(`Erro na análise: ${response.statusText}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('Erro na análise completa:', error)
      throw error
    }
  }

  async preprocessText(text) {
    try {
      const response = await fetch(`${API_BASE_URL}/preprocess`, {
      method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text })
      })
      
      if (!response.ok) {
        throw new Error(`Erro no pré-processamento: ${response.statusText}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('Erro no pré-processamento:', error)
      throw error
    }
  }

  async expandSemantic(text) {
    try {
      const response = await fetch(`${API_BASE_URL}/expand-semantic`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text })
      })
      
      if (!response.ok) {
        throw new Error(`Erro na expansão semântica: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Erro na expansão semântica:', error)
      throw error
    }
  }

  async analyzeContexts(text, words = []) {
    try {
      const response = await fetch(`${API_BASE_URL}/analyze-contexts`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text, words })
      })
      
      if (!response.ok) {
        throw new Error(`Erro na análise de contextos: ${response.statusText}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('Erro na análise de contextos:', error)
      throw error
    }
  }

  async generateVisualizations(data) {
    try {
      const response = await fetch(`${API_BASE_URL}/visualize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
      
      if (!response.ok) {
        throw new Error(`Erro na geração de visualizações: ${response.statusText}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('Erro na geração de visualizações:', error)
      throw error
    }
  }
}

export default new ApiService()