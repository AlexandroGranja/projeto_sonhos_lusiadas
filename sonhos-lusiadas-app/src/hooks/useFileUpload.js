/**
 * Hook personalizado para gerenciar uploads de arquivo
 * Projeto: Sonho em Os Lusíadas - Uma Análise Quantitativa e Qualitativa
 */

import { useState, useCallback } from 'react'
import { useToast } from '@/hooks/use-toast'
import apiService from '@/services/api'

export const useFileUpload = () => {
  const [uploadState, setUploadState] = useState({
    isUploading: false,
    progress: 0,
    uploadedFile: null,
    error: null
  })
  
  const { toast } = useToast()

  /**
   * Reseta o estado do upload
   */
  const resetUpload = useCallback(() => {
    setUploadState({
      isUploading: false,
      progress: 0,
      uploadedFile: null,
      error: null
    })
  }, [])

  /**
   * Valida arquivo antes do upload
   */
  const validateFile = useCallback((file) => {
    try {
      apiService.validateFile(file)
      return true
    } catch (error) {
      setUploadState(prev => ({ ...prev, error: error.message }))
      toast({
        title: "Arquivo inválido",
        description: error.message,
        variant: "destructive"
      })
      return false
    }
  }, [toast])

  /**
   * Faz upload do arquivo
   */
  const uploadFile = useCallback(async (file) => {
    // Valida arquivo primeiro
    if (!validateFile(file)) {
      return null
    }

    setUploadState(prev => ({
      ...prev,
      isUploading: true,
      progress: 0,
      error: null
    }))

    try {
      // Callback para atualizar progresso
      const onProgress = (progress) => {
        setUploadState(prev => ({
          ...prev,
          progress: Math.min(progress, 100)
        }))
      }

      // Faz upload
      const result = await apiService.uploadFile(file, onProgress)

      // Atualiza estado com sucesso
      setUploadState(prev => ({
        ...prev,
        isUploading: false,
        progress: 100,
        uploadedFile: {
          id: result.file_id,
          name: file.name,
          size: file.size,
          type: file.type,
          stats: result.stats
        }
      }))

      toast({
        title: "Upload concluído",
        description: `${file.name} foi enviado com sucesso`
      })

      return result
    } catch (error) {
      setUploadState(prev => ({
        ...prev,
        isUploading: false,
        error: error.message
      }))

      toast({
        title: "Erro no upload",
        description: error.message,
        variant: "destructive"
      })

      return null
    }
  }, [validateFile, toast])

  /**
   * Processa múltiplos arquivos
   */
  const uploadMultipleFiles = useCallback(async (files) => {
    const results = []
    
    for (const file of files) {
      const result = await uploadFile(file)
      if (result) {
        results.push(result)
      }
    }
    
    return results
  }, [uploadFile])

  /**
   * Extrai texto de arquivo (para arquivos .txt)
   */
  const extractTextFromFile = useCallback(async (file) => {
    try {
      const text = await apiService.extractTextFromFile(file)
      return text
    } catch (error) {
      toast({
        title: "Erro ao extrair texto",
        description: "Não foi possível extrair o texto do arquivo",
        variant: "destructive"
      })
      return null
    }
  }, [toast])

  /**
   * Obtém informações do arquivo
   */
  const getFileInfo = useCallback((file) => {
    return {
      name: file.name,
      size: apiService.formatFileSize(file.size),
      type: file.type,
      icon: apiService.getFileIcon(file.name),
      lastModified: new Date(file.lastModified).toLocaleDateString('pt-BR')
    }
  }, [])

  /**
   * Verifica se o tipo de arquivo é suportado
   */
  const isFileTypeSupported = useCallback((file) => {
    const supportedTypes = [
      'text/plain',
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ]
    
    const supportedExtensions = ['.txt', '.pdf', '.docx']
    
    return supportedTypes.includes(file.type) || 
           supportedExtensions.some(ext => file.name.toLowerCase().endsWith(ext))
  }, [])

  /**
   * Obtém preview do arquivo (para arquivos de texto)
   */
  const getFilePreview = useCallback(async (file, maxLength = 500) => {
    if (file.type === 'text/plain' || file.name.endsWith('.txt')) {
      try {
        const text = await extractTextFromFile(file)
        if (text) {
          return text.length > maxLength 
            ? text.substring(0, maxLength) + '...'
            : text
        }
      } catch (error) {
        console.error('Erro ao gerar preview:', error)
      }
    }
    return null
  }, [extractTextFromFile])

  /**
   * Calcula estatísticas básicas do arquivo de texto
   */
  const calculateTextStats = useCallback(async (file) => {
    if (file.type === 'text/plain' || file.name.endsWith('.txt')) {
      try {
        const text = await extractTextFromFile(file)
        if (text) {
          const words = text.split(/\s+/).filter(word => word.length > 0)
          const sentences = text.split(/[.!?]+/).filter(sentence => sentence.trim().length > 0)
          const paragraphs = text.split(/\n\s*\n/).filter(paragraph => paragraph.trim().length > 0)
          
          return {
            characters: text.length,
            charactersNoSpaces: text.replace(/\s/g, '').length,
            words: words.length,
            sentences: sentences.length,
            paragraphs: paragraphs.length,
            averageWordsPerSentence: Math.round(words.length / sentences.length) || 0
          }
        }
      } catch (error) {
        console.error('Erro ao calcular estatísticas:', error)
      }
    }
    return null
  }, [extractTextFromFile])

  return {
    // Estado
    isUploading: uploadState.isUploading,
    progress: uploadState.progress,
    uploadedFile: uploadState.uploadedFile,
    error: uploadState.error,
    
    // Ações
    uploadFile,
    uploadMultipleFiles,
    resetUpload,
    validateFile,
    extractTextFromFile,
    
    // Utilitários
    getFileInfo,
    isFileTypeSupported,
    getFilePreview,
    calculateTextStats
  }
}
