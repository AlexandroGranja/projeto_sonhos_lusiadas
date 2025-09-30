/**
 * Hook personalizado para gerenciar análises de texto
 * Projeto: Sonho em Os Lusíadas - Uma Análise Quantitativa e Qualitativa
 */

import { useState, useCallback, useRef } from 'react'
import { useToast } from '@/hooks/use-toast'
import apiService from '@/services/api'

export const useAnalysis = () => {
  const [analysisState, setAnalysisState] = useState({
    isAnalyzing: false,
    currentStep: null,
    progress: 0,
    results: null,
    error: null,
    analysisId: null
  })
  
  const { toast } = useToast()
  const abortControllerRef = useRef(null)

  /**
   * Reseta o estado da análise
   */
  const resetAnalysis = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
      abortControllerRef.current = null
    }

    setAnalysisState({
      isAnalyzing: false,
      currentStep: null,
      progress: 0,
      results: null,
      error: null,
      analysisId: null
    })
  }, [])

  /**
   * Inicia análise completa
   */
  const startCompleteAnalysis = useCallback(async (data) => {
    resetAnalysis()

    abortControllerRef.current = new AbortController()

    setAnalysisState(prev => ({
      ...prev,
      isAnalyzing: true,
      progress: 0,
      error: null,
      analysisId: Date.now().toString()
    }))

    try {
      const onProgress = (step) => {
        setAnalysisState(prev => ({
          ...prev,
          currentStep: step,
          progress: step.progress || prev.progress
        }))
      }

      const result = await apiService.completeAnalysis(data, onProgress)

      if (abortControllerRef.current?.signal.aborted) {
        return null
      }

      setAnalysisState(prev => ({
        ...prev,
        isAnalyzing: false,
        progress: 100,
        results: result,
        currentStep: { name: 'Concluído', progress: 100 }
      }))

      toast({
        title: "Análise concluída",
        description: "A análise foi realizada com sucesso"
      })

      return result
    } catch (error) {
      if (error.name === 'AbortError') {
        toast({
          title: "Análise cancelada",
          description: "A análise foi cancelada pelo usuário"
        })
        return null
      }

      setAnalysisState(prev => ({
        ...prev,
        isAnalyzing: false,
        error: error.message
      }))

      toast({
        title: "Erro na análise",
        description: error.message,
        variant: "destructive"
      })

      return null
    }
  }, [resetAnalysis, toast])

  const cancelAnalysis = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
      abortControllerRef.current = null
    }

    setAnalysisState(prev => ({
      ...prev,
      isAnalyzing: false,
      currentStep: { name: 'Cancelado', progress: prev.progress }
    }))

    toast({
      title: "Análise cancelada",
      description: "A análise foi cancelada com sucesso"
    })
  }, [toast])

  return {
    isAnalyzing: analysisState.isAnalyzing,
    currentStep: analysisState.currentStep,
    progress: analysisState.progress,
    results: analysisState.results,
    error: analysisState.error,
    analysisId: analysisState.analysisId,
    startCompleteAnalysis,
    cancelAnalysis,
    resetAnalysis
  }
}
