import { useState, useMemo } from 'react'
import api from '@/services/api'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import { Progress } from '@/components/ui/progress'
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line
} from 'recharts'
import { 
  Search, Filter, Download, ChevronDown, ChevronUp, 
  Eye, EyeOff, ThumbsUp, ThumbsDown, FileText, BarChart3
} from 'lucide-react'

const SimpleAnalysis = () => {
  const [text, setText] = useState('')
  const [mode, setMode] = useState('estrito')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [data, setData] = useState(null)
  
  // Filtros e busca
  const [searchTerm, setSearchTerm] = useState('')
  const [contextTypeFilter, setContextTypeFilter] = useState('todos')
  const [confidenceFilter, setConfidenceFilter] = useState(0)
  const [showReasoning, setShowReasoning] = useState(true)
  
  // Feedback do usuário
  const [userFeedback, setUserFeedback] = useState({})
  
  // Análise por canto
  const [selectedCanto, setSelectedCanto] = useState(null)

  const handleAnalyze = async () => {
    setError('')
    setData(null)
    if (!text || text.trim().length < 5) {
      setError('Cole o texto de Os Lusíadas para analisar.')
      return
    }
    setLoading(true)
    try {
      const res = await api.completeAnalysis(text, mode)
      setData(res?.results || null)
    } catch (e) {
      setError('Falha na análise. Verifique o backend e tente novamente.')
    } finally {
      setLoading(false)
    }
  }

  const handleFeedback = (contextId, isCorrect, suggestedType = null) => {
    setUserFeedback(prev => ({
      ...prev,
      [contextId]: { isCorrect, suggestedType, timestamp: new Date().toISOString() }
    }))
  }

  const highlightTerms = (sentence, terms) => {
    if (!terms || terms.length === 0) return sentence
    
    let highlighted = sentence
    terms.forEach(term => {
      const regex = new RegExp(`\\b${term.term}\\b`, 'gi')
      highlighted = highlighted.replace(regex, `<span class="bg-yellow-200 px-1 rounded font-semibold">${term.term}</span>`)
    })
    return highlighted
  }

  // Normaliza campos vindos do backend para evitar "undefined"
  const normalizeContext = (ctx) => {
    if (!ctx) return ctx
    const context_type = ctx.context_type || ctx.classification || 'onírico'
    let confidence = ctx.confidence_score
    if (confidence === undefined || confidence === null) confidence = ctx.confidence
    if (typeof confidence === 'number' && confidence > 1) confidence = Math.round((confidence / 100) * 100) / 100
    if (typeof confidence !== 'number') confidence = 0
    const sentence = ctx.sentence || ctx.text || ctx.excerpt || ''
    return { ...ctx, context_type, confidence_score: confidence, sentence }
  }

  const exportToCSV = () => {
    if (!data) {
      alert('❌ Nenhuma análise disponível para exportar.\n\nPor favor, execute uma análise primeiro.')
      return
    }
    
    // Coletar todos os contextos de todos os cantos
    let allContexts = []
    
    // Usar Object.keys(byCanto) em vez de sortedCantos se sortedCantos estiver vazio
    const cantosToProcess = sortedCantos.length > 0 ? sortedCantos : Object.keys(byCanto)
    
    cantosToProcess.forEach(canto => {
      const info = byCanto[canto]
      if (info && info.dream_contexts) {
        const cantoContexts = info.dream_contexts.map(ctx => ({
          ...ctx,
          canto,
          id: `${canto}-${ctx.position}`
        }))
        allContexts = allContexts.concat(cantoContexts)
      }
    })
    
    console.log('Contextos encontrados:', allContexts.length)
    console.log('Cantos processados:', cantosToProcess)
    console.log('Dados da análise:', data)
    
    if (allContexts.length === 0) {
      alert(`❌ Nenhum contexto encontrado para exportar.\n\n📊 Estatísticas da análise:\n• Palavras processadas: ${aggregate?.preprocessing?.words || 0}\n• Ocorrências encontradas: ${aggregate?.semantic_expansion?.terms_found || 0}\n• Cantos analisados: ${aggregate?.cantos_identified || 0}\n\n💡 Dica: Tente usar o "Modo Completo" para encontrar mais termos relacionados.`)
      return
    }
    
    const headers = ['Canto', 'Estrofe', 'Tipo', 'Confiança', 'Raciocínio', 'Trecho', 'Termos']
    const csvContent = [
      headers.join(','),
      ...allContexts.map(ctx => [
        ctx.canto,
        ctx.stanza || '',
        ctx.context_type,
        ctx.confidence_score || 0,
        `"${(ctx.reasoning || '').replace(/"/g, '""')}"`,
        `"${ctx.sentence.replace(/"/g, '""')}"`,
        ctx.terms?.map(t => t.term).join(';') || ''
      ].join(','))
    ].join('\n')
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'analise_sonhos_lusiadas.csv'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const exportToPDF = () => {
    if (!data) {
      alert('❌ Nenhuma análise disponível para exportar.\n\nPor favor, execute uma análise primeiro.')
      return
    }
    
    // Coletar todos os contextos de todos os cantos
    let allContexts = []
    
    // Usar Object.keys(byCanto) em vez de sortedCantos se sortedCantos estiver vazio
    const cantosToProcess = sortedCantos.length > 0 ? sortedCantos : Object.keys(byCanto)
    
    cantosToProcess.forEach(canto => {
      const info = byCanto[canto]
      if (info && info.dream_contexts) {
        const cantoContexts = info.dream_contexts.map(ctx => ({
          ...ctx,
          canto,
          id: `${canto}-${ctx.position}`
        }))
        allContexts = allContexts.concat(cantoContexts)
      }
    })
    
    if (allContexts.length === 0) {
      alert(`❌ Nenhum contexto encontrado para exportar.\n\n📊 Estatísticas da análise:\n• Palavras processadas: ${aggregate?.preprocessing?.words || 0}\n• Ocorrências encontradas: ${aggregate?.semantic_expansion?.terms_found || 0}\n• Cantos analisados: ${aggregate?.cantos_identified || 0}\n\n💡 Dica: Tente usar o "Modo Completo" para encontrar mais termos relacionados.`)
      return
    }
    
    const printWindow = window.open('', '_blank')
    const content = `
      <html>
        <head>
          <title>Análise de Sonhos em Os Lusíadas</title>
          <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .header { text-align: center; margin-bottom: 30px; }
            .context { margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; }
            .confidence { color: #666; font-size: 0.9em; }
            .reasoning { background: #f5f5f5; padding: 10px; margin-top: 10px; }
            .stats { background: #f0f8ff; padding: 15px; margin-bottom: 20px; border-radius: 5px; }
          </style>
        </head>
        <body>
          <div class="header">
            <h1>Análise de Sonhos em Os Lusíadas</h1>
            <p>Relatório gerado em ${new Date().toLocaleDateString('pt-BR')}</p>
          </div>
          
          <div class="stats">
            <h2>Estatísticas Gerais</h2>
            <p><strong>Total de palavras:</strong> ${aggregate?.preprocessing?.words || 0}</p>
            <p><strong>Ocorrências encontradas:</strong> ${aggregate?.semantic_expansion?.terms_found || 0}</p>
            <p><strong>Cantos analisados:</strong> ${aggregate?.cantos_identified || 0}</p>
            <p><strong>Total de contextos:</strong> ${allContexts.length}</p>
          </div>
          
          ${allContexts.map(ctx => `
            <div class="context">
              <h3>${ctx.canto} - Estrofe ${ctx.stanza || 'N/A'}</h3>
              <p><strong>Tipo:</strong> ${ctx.context_type}</p>
              <p class="confidence"><strong>Confiança:</strong> ${Math.round((ctx.confidence_score || 0) * 100)}%</p>
              <p><strong>Trecho:</strong> ${ctx.sentence}</p>
              <div class="reasoning">
                <strong>Raciocínio:</strong> ${ctx.reasoning || 'N/A'}
              </div>
            </div>
          `).join('')}
        </body>
      </html>
    `
    printWindow.document.write(content)
    printWindow.document.close()
    printWindow.print()
  }

  

  const exportToDOCX = async () => {
    if (!data) {
      alert('❌ Nenhuma análise disponível para exportar.\n\nPor favor, execute uma análise primeiro.')
      return
    }
    try {
      const resp = await api.exportDetailedReport(data, 'docx')
      const base64 = resp?.content
      const filename = resp?.filename || 'relatorio_analise_sonhos.docx'
      if (!base64) {
        alert('Não foi possível gerar o DOCX. Tente novamente.')
        return
      }
      const byteCharacters = atob(base64)
      const byteNumbers = new Array(byteCharacters.length)
      for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i)
      }
      const byteArray = new Uint8Array(byteNumbers)
      const blob = new Blob([byteArray], { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = filename
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } catch (e) {
      console.error('Erro ao exportar DOCX:', e)
      alert('Falha ao exportar DOCX. Verifique o backend e tente novamente.')
    }
  }

  const downloadCompleteAnalysis = () => {
    if (!data) {
      alert('❌ Nenhuma análise disponível para exportar.\n\nPor favor, execute uma análise primeiro.')
      return
    }

    // Coletar todos os contextos de todos os cantos
    let allContexts = []
    
    // Usar Object.keys(byCanto) em vez de sortedCantos se sortedCantos estiver vazio
    const cantosToProcess = sortedCantos.length > 0 ? sortedCantos : Object.keys(byCanto)
    
    cantosToProcess.forEach(canto => {
      const info = byCanto[canto]
      if (info && info.dream_contexts) {
        const cantoContexts = info.dream_contexts.map(ctx => ({
          ...ctx,
          canto,
          id: `${canto}-${ctx.position}`
        }))
        allContexts = allContexts.concat(cantoContexts)
      }
    })

    console.log('Contextos encontrados para JSON:', allContexts.length)
    console.log('Cantos processados:', cantosToProcess)
    console.log('Dados da análise:', data)

    const analysisData = {
      metadata: {
        generated_at: new Date().toISOString(),
        total_words: aggregate?.preprocessing?.words || 0,
        total_occurrences: aggregate?.semantic_expansion?.terms_found || 0,
        cantos_analyzed: aggregate?.cantos_identified || 0,
        total_contexts: allContexts.length,
        debug_info: {
          sortedCantos: sortedCantos,
          byCantoKeys: Object.keys(byCanto),
          hasAggregate: !!aggregate,
          hasData: !!data
        }
      },
      summary: {
        context_classification: aggregate?.context_classification || {},
        cantos_identified: aggregate?.cantos_identified || 0
      },
      by_canto: byCanto,
      all_contexts: allContexts,
      filters_applied: {
        search_term: searchTerm,
        context_type: contextTypeFilter,
        confidence_min: confidenceFilter
      }
    }

    const blob = new Blob([JSON.stringify(analysisData, null, 2)], { type: 'application/json;charset=utf-8;' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `analise_completa_sonhos_lusiadas_${new Date().toISOString().split('T')[0]}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const aggregate = data?.aggregate
  const byCanto = data?.by_canto || {}

  // Ordenar cantos I-X
  const cantoOrder = ['CANTO I', 'CANTO II', 'CANTO III', 'CANTO IV', 'CANTO V', 'CANTO VI', 'CANTO VII', 'CANTO VIII', 'CANTO IX', 'CANTO X']
  const sortedCantos = cantoOrder.filter(canto => byCanto[canto])

  const getContextTypeColor = (type) => {
    const colors = {
      'onírico': '#3b82f6',
      'profético': '#10b981',
      'alegórico': '#f59e0b',
      'divino': '#ef4444'
    }
    return colors[type] || '#6b7280'
  }

  // Filtrar contextos
  const filteredContexts = useMemo(() => {
    if (!data) return []
    
    let contexts = []
    sortedCantos.forEach(canto => {
      const info = byCanto[canto]
      const cantoContexts = (info.dream_contexts || []).map(ctx => ({
        ...normalizeContext(ctx),
        canto,
        id: `${canto}-${ctx.position}`
      }))
      contexts = contexts.concat(cantoContexts)
    })

    // Aplicar filtros
    if (searchTerm) {
      contexts = contexts.filter(ctx => 
        ctx.sentence.toLowerCase().includes(searchTerm.toLowerCase()) ||
        ctx.reasoning?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        ctx.terms?.some(term => term.term.toLowerCase().includes(searchTerm.toLowerCase()))
      )
    }

    if (contextTypeFilter !== 'todos') {
      contexts = contexts.filter(ctx => ctx.context_type === contextTypeFilter)
    }

    if (confidenceFilter > 0) {
      contexts = contexts.filter(ctx => (ctx.confidence_score || 0) >= confidenceFilter)
    }

    return contexts
  }, [data, searchTerm, contextTypeFilter, confidenceFilter, sortedCantos])

  // Dados para gráficos
  const chartData = useMemo(() => {
    if (!data || !aggregate) return { barData: [], pieData: [], lineData: [] }

    const barData = sortedCantos.map(canto => {
      const info = byCanto[canto]
      const contexts = info.dream_contexts || []
      return {
        canto: canto.replace('CANTO ', ''),
        onírico: contexts.filter(c => c.context_type === 'onírico').length,
        profético: contexts.filter(c => c.context_type === 'profético').length,
        alegórico: contexts.filter(c => c.context_type === 'alegórico').length,
        divino: contexts.filter(c => c.context_type === 'divino').length
      }
    })

    const pieData = Object.entries(aggregate.context_classification || {}).map(([type, count]) => ({
      name: type,
      value: count,
      color: getContextTypeColor(type)
    }))

    const lineData = sortedCantos.map((canto, index) => {
      const info = byCanto[canto]
      const contexts = info.dream_contexts || []
      const avgConfidence = contexts.length > 0 
        ? contexts.reduce((sum, c) => sum + (c.confidence_score || 0), 0) / contexts.length
        : 0
      return {
        canto: index + 1,
        confidence: avgConfidence * 100
      }
    })

    return { barData, pieData, lineData }
  }, [data, sortedCantos, aggregate])

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-slate-800 mb-2">Análise de Sonhos em Os Lusíadas</h1>
        <p className="text-slate-600">Cole o texto e veja onde aparecem referências a sonhos por Canto e Estrofe</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Texto para Análise</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Cole aqui o texto completo de Os Lusíadas..."
            rows={8}
            className="text-sm"
          />
          <div className="space-y-4">
            {/* Explicação dos Modos */}
            <div className="bg-blue-50 p-4 rounded-lg">
              <h3 className="font-semibold text-blue-800 mb-2">Escolha o Modo de Análise:</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex items-start gap-3">
                  <div className="w-48">
                    <Select value={mode} onValueChange={setMode}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="estrito">Modo Estrito</SelectItem>
                        <SelectItem value="default">Modo Completo</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="text-sm text-blue-700">
                    {mode === 'estrito' ? (
                      <div>
                        <strong>Modo Estrito:</strong> Busca apenas palavras diretamente relacionadas a "sonho" (sonho, sonhar, sonhador, etc.)
                      </div>
                    ) : (
                      <div>
                        <strong>Modo Completo:</strong> Busca termos relacionados semanticamente (visão, devaneio, ilusão, profecia, etc.)
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
            
            <div className="flex gap-4 items-center">
              <Button onClick={handleAnalyze} disabled={loading} className="px-8">
                {loading ? 'Analisando...' : 'Iniciar Análise'}
              </Button>
              {error && <span className="text-red-600 text-sm">{error}</span>}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Filtros e Busca removidos por solicitação do usuário */}

      {aggregate && (
        <div className="space-y-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Card>
              <CardContent className="p-4 text-center">
                <div className="text-2xl font-bold text-blue-600">{aggregate.preprocessing?.words || 0}</div>
                <div className="text-sm text-slate-600">Palavras</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4 text-center">
                <div className="text-2xl font-bold text-green-600">{aggregate.semantic_expansion?.terms_found || 0}</div>
                <div className="text-sm text-slate-600">Ocorrências</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4 text-center">
                <div className="text-2xl font-bold text-purple-600">{aggregate.cantos_identified || 0}</div>
                <div className="text-sm text-slate-600">Cantos</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4 text-center">
                <div className="text-2xl font-bold text-orange-600">
                  {Object.values(aggregate.context_classification || {}).reduce((a, b) => a + b, 0)}
                </div>
                <div className="text-sm text-slate-600">Contextos</div>
              </CardContent>
            </Card>
          </div>
          
          {/* Botões de Download */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Download className="h-5 w-5" />
                Download da Análise
              </CardTitle>
              <p className="text-sm text-gray-600">
                Baixe a análise completa em diferentes formatos
              </p>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex flex-wrap gap-3">
                  <Button onClick={downloadCompleteAnalysis} className="flex items-center gap-2">
                    <Download className="h-4 w-4" />
                    Análise Completa (JSON)
                  </Button>
                  <Button variant="outline" onClick={exportToCSV} className="flex items-center gap-2">
                    <FileText className="h-4 w-4" />
                    Contextos (CSV)
                  </Button>
                  <Button variant="outline" onClick={exportToPDF} className="flex items-center gap-2">
                    <FileText className="h-4 w-4" />
                    Relatório (PDF)
                  </Button>
                  <Button variant="outline" onClick={exportToDOCX} className="flex items-center gap-2">
                    <FileText className="h-4 w-4" />
                    Word (DOCX)
                  </Button>
                </div>
                
                {/* Debug Info */}
                <div className="bg-gray-50 p-3 rounded-lg text-xs">
                  <details>
                    <summary className="cursor-pointer font-medium text-gray-700">
                      🔍 Informações de Debug (clique para expandir)
                    </summary>
                    <div className="mt-2 space-y-1 text-gray-600">
                      <div>• Cantos encontrados: {sortedCantos.length}</div>
                      <div>• Chaves byCanto: {Object.keys(byCanto).length}</div>
                      <div>• Tem aggregate: {aggregate ? 'Sim' : 'Não'}</div>
                      <div>• Tem data: {data ? 'Sim' : 'Não'}</div>
                      <div>• Contextos filtrados: {filteredContexts.length}</div>
                      <div>• Cantos para processar: {sortedCantos.length > 0 ? sortedCantos.length : Object.keys(byCanto).length}</div>
                      {Object.keys(byCanto).length > 0 && (
                        <div className="mt-2">
                          <div className="font-medium">Contextos por canto:</div>
                          {Object.keys(byCanto).map(canto => {
                            const info = byCanto[canto]
                            const contexts = info.dream_contexts || []
                            return (
                              <div key={canto} className="ml-2">
                                {canto}: {contexts.length} contextos
                              </div>
                            )
                          })}
                        </div>
                      )}
                    </div>
                  </details>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Visualizações Interativas */}
      {data && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="h-5 w-5" />
              Visualizações Interativas
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="distribution" className="w-full">
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="distribution">Distribuição por Canto</TabsTrigger>
                <TabsTrigger value="types">Tipos de Contexto</TabsTrigger>
                <TabsTrigger value="confidence">Evolução da Confiança</TabsTrigger>
              </TabsList>
              
              <TabsContent value="distribution" className="mt-6">
                <div className="h-80">
                  {chartData.barData.length > 0 ? (
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={chartData.barData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="canto" />
                        <YAxis />
                        <RechartsTooltip />
                        <Bar dataKey="onírico" stackId="a" fill="#3b82f6" name="Onírico" />
                        <Bar dataKey="profético" stackId="a" fill="#10b981" name="Profético" />
                        <Bar dataKey="alegórico" stackId="a" fill="#f59e0b" name="Alegórico" />
                        <Bar dataKey="divino" stackId="a" fill="#ef4444" name="Divino" />
                      </BarChart>
                    </ResponsiveContainer>
                  ) : (
                    <div className="flex items-center justify-center h-full text-gray-500">
                      Nenhum dado disponível para exibir
                    </div>
                  )}
                </div>
              </TabsContent>
              
              <TabsContent value="types" className="mt-6">
                <div className="h-80">
                  {chartData.pieData.length > 0 ? (
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={chartData.pieData}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                          outerRadius={80}
                          fill="#8884d8"
                          dataKey="value"
                        >
                          {chartData.pieData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                        <RechartsTooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  ) : (
                    <div className="flex items-center justify-center h-full text-gray-500">
                      Nenhum dado disponível para exibir
                    </div>
                  )}
                </div>
              </TabsContent>
              
              <TabsContent value="confidence" className="mt-6">
                <div className="h-80">
                  {chartData.lineData.length > 0 ? (
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={chartData.lineData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="canto" />
                        <YAxis domain={[0, 100]} />
                        <RechartsTooltip formatter={(value) => [`${value.toFixed(1)}%`, 'Confiança']} />
                        <Line type="monotone" dataKey="confidence" stroke="#8884d8" strokeWidth={2} />
                      </LineChart>
                    </ResponsiveContainer>
                  ) : (
                    <div className="flex items-center justify-center h-full text-gray-500">
                      Nenhum dado disponível para exibir
                    </div>
                  )}
                </div>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      )}

      {/* Análise Detalhada por Canto */}
      {sortedCantos.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="h-5 w-5" />
              Análise Detalhada por Canto
            </CardTitle>
            <p className="text-sm text-gray-600">
              Clique em um canto para ver a análise detalhada com estatísticas específicas
            </p>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              {sortedCantos.map(canto => {
                const info = byCanto[canto]
                const totalOccurrences = info.semantic_expansion?.terms_found || 0
                const stanzas = info.stanzas || []
                const contexts = info.dream_contexts || []
                const words = info.preprocessing?.words || 0
                
                return (
                  <div 
                    key={canto} 
                    className={`text-center p-4 rounded-lg border-2 cursor-pointer transition-all hover:shadow-md ${
                      selectedCanto === canto 
                        ? 'border-blue-500 bg-blue-50' 
                        : 'border-gray-200 bg-white hover:border-gray-300'
                    }`}
                    onClick={() => setSelectedCanto(selectedCanto === canto ? null : canto)}
                  >
                    <div className="font-semibold text-slate-700 mb-2">{canto.replace('CANTO ', '')}</div>
                    <div className="text-2xl font-bold text-blue-600 mb-1">{totalOccurrences}</div>
                    <div className="text-xs text-slate-500 mb-1">ocorrências</div>
                    <div className="text-xs text-slate-500 mb-1">{stanzas.length} estrofes</div>
                    <div className="text-xs text-slate-500">{words.toLocaleString()} palavras</div>
                    <div className="text-xs text-slate-500">{contexts.length} contextos</div>
                  </div>
                )
              })}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Análise Detalhada do Canto Selecionado */}
      {selectedCanto && byCanto[selectedCanto] && (
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-xl text-slate-800">{selectedCanto}</CardTitle>
              <Button 
                variant="outline" 
                size="sm" 
                onClick={() => setSelectedCanto(null)}
              >
                Fechar
              </Button>
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            {(() => {
              const info = byCanto[selectedCanto]
              const stanzas = info.stanzas || []
              const contexts = info.dream_contexts || []
              const terms = info.expanded_terms || {}
              const classification = info.context_classification || {}
              const totalOccurrences = info.semantic_expansion?.terms_found || 0
              const words = info.preprocessing?.words || 0
              const sentences = info.preprocessing?.sentences || 0
              
              return (
                <>
                  {/* Estatísticas do Canto */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="text-center p-3 bg-slate-50 rounded">
                      <div className="text-lg font-bold text-slate-700">{words.toLocaleString()}</div>
                      <div className="text-xs text-slate-500">Palavras</div>
                    </div>
                    <div className="text-center p-3 bg-slate-50 rounded">
                      <div className="text-lg font-bold text-slate-700">{sentences}</div>
                      <div className="text-xs text-slate-500">Sentenças</div>
                    </div>
                    <div className="text-center p-3 bg-slate-50 rounded">
                      <div className="text-lg font-bold text-slate-700">{stanzas.length}</div>
                      <div className="text-xs text-slate-500">Estrofes com sonhos</div>
                    </div>
                    <div className="text-center p-3 bg-slate-50 rounded">
                      <div className="text-lg font-bold text-slate-700">
                        {Math.round((totalOccurrences / (words || 1)) * 10000) / 100}%
                      </div>
                      <div className="text-xs text-slate-500">Densidade</div>
                    </div>
                  </div>

                  {/* Classificação por Tipo */}
                  <div>
                    <h4 className="font-semibold text-slate-700 mb-3">Classificação por Tipo de Sonho</h4>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                      {Object.entries(classification).map(([type, count]) => (
                        <div key={type} className="flex items-center justify-between p-2 bg-slate-50 rounded">
                          <span className="text-sm font-medium capitalize text-slate-600">{type}</span>
                          <Badge variant={count > 0 ? "default" : "outline"} className="text-xs">
                            {count}
                          </Badge>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Estrofes com Ocorrências */}
                  {stanzas.length > 0 && (
                    <div>
                      <h4 className="font-semibold text-slate-700 mb-3">Estrofes com Referências a Sonhos</h4>
                      <div className="flex flex-wrap gap-2">
                        {stanzas.map(stanza => (
                          <Badge key={stanza} variant="default" className="text-sm px-3 py-1">
                            Estrofe {stanza}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Termos Encontrados */}
                  {Object.keys(terms).length > 0 && (
                    <div>
                      <h4 className="font-semibold text-slate-700 mb-3">Termos Encontrados por Categoria</h4>
                      <div className="space-y-3">
                        {Object.entries(terms).map(([category, termData]) => {
                          const categoryTotal = termData.total || 0
                          if (categoryTotal === 0) return null
                          
                          return (
                            <div key={category} className="border rounded-lg p-3">
                              <div className="flex items-center justify-between mb-2">
                                <span className="font-medium capitalize text-slate-700">{category}</span>
                                <Badge variant="secondary">{categoryTotal} total</Badge>
                              </div>
                              <div className="flex flex-wrap gap-1">
                                {Object.entries(termData).map(([term, count]) => {
                                  if (term === 'total') return null
                                  return (
                                    <Badge key={term} variant="outline" className="text-xs">
                                      {term} ({count})
                                    </Badge>
                                  )
                                })}
                              </div>
                            </div>
                          )
                        })}
                      </div>
                    </div>
                  )}

                  {/* Trechos Detalhados */}
                  {contexts.length > 0 && (
                    <div>
                      <h4 className="font-semibold text-slate-700 mb-3">Trechos Encontrados ({contexts.length} total)</h4>
                      <div className="space-y-3 max-h-96 overflow-y-auto">
                        {contexts.map((ctx, idx) => (
                          <div key={idx} className="bg-slate-50 p-4 rounded-lg border-l-4 border-blue-300">
                            <div className="flex items-center justify-between mb-2">
                              <div className="flex items-center gap-2">
                                <Badge variant="outline" className="text-xs">
                                  {ctx.context_type}
                                </Badge>
                                {ctx.stanza && (
                                  <Badge variant="secondary" className="text-xs">
                                    Estrofe {ctx.stanza}
                                  </Badge>
                                )}
                                <span className="text-xs text-slate-500">
                                  {ctx.terms?.length || 0} termo(s)
                                </span>
                                {ctx.confidence_score && (
                                  <div className="flex items-center gap-1">
                                    <span className="text-xs text-slate-500">Confiança:</span>
                                    <Progress 
                                      value={(ctx.confidence_score || 0) * 100} 
                                      className="w-16 h-2"
                                    />
                                    <span className="text-xs text-slate-500">
                                      {Math.round((ctx.confidence_score || 0) * 100)}%
                                    </span>
                                  </div>
                                )}
                              </div>
                              <div className="flex gap-1">
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  onClick={() => handleFeedback(`${selectedCanto}-${ctx.position}`, true)}
                                  className="h-6 w-6 p-0"
                                >
                                  <ThumbsUp className="h-3 w-3" />
                                </Button>
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  onClick={() => handleFeedback(`${selectedCanto}-${ctx.position}`, false)}
                                  className="h-6 w-6 p-0"
                                >
                                  <ThumbsDown className="h-3 w-3" />
                                </Button>
                              </div>
                            </div>
                            <div 
                              className="text-slate-700 italic mb-2"
                              dangerouslySetInnerHTML={{ 
                                __html: highlightTerms(ctx.sentence, ctx.terms || []) 
                              }}
                            />
                            {ctx.terms && ctx.terms.length > 0 && (
                              <div className="flex flex-wrap gap-1 mb-2">
                                {ctx.terms.map((term, termIdx) => (
                                  <Badge key={termIdx} variant="outline" className="text-xs">
                                    {term.term}
                                  </Badge>
                                ))}
                              </div>
                            )}
                            {showReasoning && ctx.reasoning && (
                              <Collapsible>
                                <CollapsibleTrigger className="flex items-center gap-1 text-sm text-slate-600 hover:text-slate-800">
                                  <ChevronDown className="h-4 w-4" />
                                  Ver raciocínio
                                </CollapsibleTrigger>
                                <CollapsibleContent className="mt-2 p-3 bg-slate-100 rounded text-sm text-slate-700">
                                  {ctx.reasoning}
                                </CollapsibleContent>
                              </Collapsible>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Resumo do Canto */}
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <h5 className="font-semibold text-slate-700 mb-2">Resumo do {selectedCanto}</h5>
                    <p className="text-sm text-slate-600">
                      Este canto contém <strong>{totalOccurrences} ocorrências</strong> de termos relacionados a sonhos, 
                      distribuídas em <strong>{stanzas.length} estrofes</strong>. 
                      A densidade de referências oníricas é de <strong>
                        {Math.round((totalOccurrences / (words || 1)) * 10000) / 100}%
                      </strong> do total de palavras.
                    </p>
                  </div>
                </>
              )
            })()}
          </CardContent>
        </Card>
      )}

      {sortedCantos.length > 0 && (
        <div className="space-y-6">
          <h2 className="text-2xl font-bold text-slate-800">Análise Completa por Canto</h2>
          
          {/* Resumo Geral dos Cantos */}
          <Card className="bg-gradient-to-r from-blue-50 to-purple-50">
            <CardHeader>
              <CardTitle className="text-lg">Resumo Geral dos Cantos</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                {sortedCantos.map(canto => {
                  const info = byCanto[canto]
                  const totalOccurrences = info.semantic_expansion?.terms_found || 0
                  const stanzas = info.stanzas || []
                  return (
                    <div key={canto} className="text-center p-3 bg-white rounded-lg border">
                      <div className="font-semibold text-slate-700">{canto.replace('CANTO ', '')}</div>
                      <div className="text-2xl font-bold text-blue-600">{totalOccurrences}</div>
                      <div className="text-xs text-slate-500">ocorrências</div>
                      <div className="text-xs text-slate-500">{stanzas.length} estrofes</div>
                    </div>
                  )
                })}
              </div>
            </CardContent>
          </Card>

          {/* Análise Detalhada de Cada Canto */}
          {sortedCantos.map(canto => {
            const info = byCanto[canto]
            const stanzas = info.stanzas || []
            const contexts = info.dream_contexts || []
            const terms = info.expanded_terms || {}
            const classification = info.context_classification || {}
            const totalOccurrences = info.semantic_expansion?.terms_found || 0
            
            return (
              <Card key={canto} className="border-2">
                <CardHeader className="bg-gradient-to-r from-slate-50 to-blue-50">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-xl text-slate-800">{canto}</CardTitle>
                    <div className="flex gap-2">
                      <Badge variant="default" className="bg-blue-600">
                        {totalOccurrences} ocorrências
                      </Badge>
                      <Badge variant="outline">
                        {stanzas.length} estrofes
                      </Badge>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-6">
                  
                  {/* Estatísticas do Canto */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="text-center p-3 bg-slate-50 rounded">
                      <div className="text-lg font-bold text-slate-700">{info.preprocessing?.words || 0}</div>
                      <div className="text-xs text-slate-500">Palavras</div>
                    </div>
                    <div className="text-center p-3 bg-slate-50 rounded">
                      <div className="text-lg font-bold text-slate-700">{info.preprocessing?.sentences || 0}</div>
                      <div className="text-xs text-slate-500">Sentenças</div>
                    </div>
                    <div className="text-center p-3 bg-slate-50 rounded">
                      <div className="text-lg font-bold text-slate-700">{stanzas.length}</div>
                      <div className="text-xs text-slate-500">Estrofes com sonhos</div>
                    </div>
                    <div className="text-center p-3 bg-slate-50 rounded">
                      <div className="text-lg font-bold text-slate-700">
                        {Math.round((totalOccurrences / (info.preprocessing?.words || 1)) * 10000) / 100}%
                      </div>
                      <div className="text-xs text-slate-500">Densidade</div>
                    </div>
                  </div>

                  {/* Classificação por Tipo */}
                  <div>
                    <h4 className="font-semibold text-slate-700 mb-3">Classificação por Tipo de Sonho</h4>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                      {Object.entries(classification).map(([type, count]) => (
                        <div key={type} className="flex items-center justify-between p-2 bg-slate-50 rounded">
                          <span className="text-sm font-medium capitalize text-slate-600">{type}</span>
                          <Badge variant={count > 0 ? "default" : "outline"} className="text-xs">
                            {count}
                          </Badge>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Estrofes com Ocorrências */}
                  {stanzas.length > 0 && (
                    <div>
                      <h4 className="font-semibold text-slate-700 mb-3">Estrofes com Referências a Sonhos</h4>
                      <div className="flex flex-wrap gap-2">
                        {stanzas.map(stanza => (
                          <Badge key={stanza} variant="default" className="text-sm px-3 py-1">
                            Estrofe {stanza}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Termos Encontrados */}
                  {Object.keys(terms).length > 0 && (
                    <div>
                      <h4 className="font-semibold text-slate-700 mb-3">Termos Encontrados por Categoria</h4>
                      <div className="space-y-3">
                        {Object.entries(terms).map(([category, termData]) => {
                          const categoryTotal = termData.total || 0
                          if (categoryTotal === 0) return null
                          
                          return (
                            <div key={category} className="border rounded-lg p-3">
                              <div className="flex items-center justify-between mb-2">
                                <span className="font-medium capitalize text-slate-700">{category}</span>
                                <Badge variant="secondary">{categoryTotal} total</Badge>
                              </div>
                              <div className="flex flex-wrap gap-1">
                                {Object.entries(termData).map(([term, count]) => {
                                  if (term === 'total') return null
                                  return (
                                    <Badge key={term} variant="outline" className="text-xs">
                                      {term} ({count})
                                    </Badge>
                                  )
                                })}
                              </div>
                            </div>
                          )
                        })}
                      </div>
                    </div>
                  )}

                  {/* Trechos Detalhados */}
                  {contexts.length > 0 && (
                    <div>
                      <h4 className="font-semibold text-slate-700 mb-3">Trechos Encontrados ({contexts.length} total)</h4>
                      <div className="space-y-3 max-h-96 overflow-y-auto">
                        {contexts.map((ctx, idx) => (
                          <div key={idx} className="bg-slate-50 p-4 rounded-lg border-l-4 border-blue-300">
                            <div className="flex items-center justify-between mb-2">
                              <div className="flex items-center gap-2">
                                <Badge variant="outline" className="text-xs">
                                  {ctx.context_type}
                                </Badge>
                                {ctx.stanza && (
                                  <Badge variant="secondary" className="text-xs">
                                    Estrofe {ctx.stanza}
                                  </Badge>
                                )}
                                <span className="text-xs text-slate-500">
                                  {ctx.terms?.length || 0} termo(s)
                                </span>
                                {ctx.confidence_score && (
                                  <div className="flex items-center gap-1">
                                    <span className="text-xs text-slate-500">Confiança:</span>
                                    <Progress 
                                      value={(ctx.confidence_score || 0) * 100} 
                                      className="w-16 h-2"
                                    />
                                    <span className="text-xs text-slate-500">
                                      {Math.round((ctx.confidence_score || 0) * 100)}%
                                    </span>
                                  </div>
                                )}
                              </div>
                              <div className="flex gap-1">
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  onClick={() => handleFeedback(`${canto}-${ctx.position}`, true)}
                                  className="h-6 w-6 p-0"
                                >
                                  <ThumbsUp className="h-3 w-3" />
                                </Button>
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  onClick={() => handleFeedback(`${canto}-${ctx.position}`, false)}
                                  className="h-6 w-6 p-0"
                                >
                                  <ThumbsDown className="h-3 w-3" />
                                </Button>
                              </div>
                            </div>
                            <div 
                              className="text-slate-700 italic mb-2"
                              dangerouslySetInnerHTML={{ 
                                __html: highlightTerms(ctx.sentence, ctx.terms || []) 
                              }}
                            />
                            {ctx.terms && ctx.terms.length > 0 && (
                              <div className="flex flex-wrap gap-1 mb-2">
                                {ctx.terms.map((term, termIdx) => (
                                  <Badge key={termIdx} variant="outline" className="text-xs">
                                    {term.term}
                                  </Badge>
                                ))}
                              </div>
                            )}
                            {showReasoning && ctx.reasoning && (
                              <Collapsible>
                                <CollapsibleTrigger className="flex items-center gap-1 text-sm text-slate-600 hover:text-slate-800">
                                  <ChevronDown className="h-4 w-4" />
                                  Ver raciocínio
                                </CollapsibleTrigger>
                                <CollapsibleContent className="mt-2 p-3 bg-slate-100 rounded text-sm text-slate-700">
                                  {ctx.reasoning}
                                </CollapsibleContent>
                              </Collapsible>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Resumo do Canto */}
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <h5 className="font-semibold text-slate-700 mb-2">Resumo do {canto}</h5>
                    <p className="text-sm text-slate-600">
                      Este canto contém <strong>{totalOccurrences} ocorrências</strong> de termos relacionados a sonhos, 
                      distribuídas em <strong>{stanzas.length} estrofes</strong>. 
                      A densidade de referências oníricas é de <strong>
                        {Math.round((totalOccurrences / (info.preprocessing?.words || 1)) * 10000) / 100}%
                      </strong> do total de palavras.
                    </p>
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>
      )}

      {/* Trechos Filtrados */}
      {filteredContexts.length > 0 && (
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>
                Trechos Filtrados ({filteredContexts.length} total)
              </CardTitle>
              <div className="flex gap-2">
                <Button variant="outline" onClick={exportToCSV} size="sm">
                  <Download className="h-4 w-4 mr-2" />
                  CSV
                </Button>
                <Button variant="outline" onClick={exportToPDF} size="sm">
                  <FileText className="h-4 w-4 mr-2" />
                  PDF
                </Button>
                <Button variant="outline" onClick={exportToDOCX} size="sm">
                  <FileText className="h-4 w-4 mr-2" />
                  Word (DOCX)
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {filteredContexts.map((ctx) => (
                <div key={ctx.id} className="bg-slate-50 p-4 rounded-lg border-l-4 border-blue-300">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <Badge variant="outline" className="text-xs">
                        {ctx.context_type}
                      </Badge>
                      {ctx.stanza && (
                        <Badge variant="secondary" className="text-xs">
                          Estrofe {ctx.stanza}
                        </Badge>
                      )}
                      <Badge variant="outline" className="text-xs">
                        {ctx.canto}
                      </Badge>
                      <div className="flex items-center gap-1">
                        <span className="text-xs text-slate-500">Confiança:</span>
                        <Progress 
                          value={(ctx.confidence_score || 0) * 100} 
                          className="w-16 h-2"
                        />
                        <span className="text-xs text-slate-500">
                          {Math.round((ctx.confidence_score || 0) * 100)}%
                        </span>
                      </div>
                    </div>
                    <div className="flex gap-1">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleFeedback(ctx.id, true)}
                        className="h-6 w-6 p-0"
                      >
                        <ThumbsUp className="h-3 w-3" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleFeedback(ctx.id, false)}
                        className="h-6 w-6 p-0"
                      >
                        <ThumbsDown className="h-3 w-3" />
                      </Button>
                    </div>
                  </div>
                  
                  <div 
                    className="text-slate-700 italic mb-2"
                    dangerouslySetInnerHTML={{ 
                      __html: highlightTerms(ctx.sentence, ctx.terms || []) 
                    }}
                  />
                  
                  {ctx.terms && ctx.terms.length > 0 && (
                    <div className="flex flex-wrap gap-1 mb-2">
                      {ctx.terms.map((term, termIdx) => (
                        <Badge key={termIdx} variant="outline" className="text-xs">
                          {term.term}
                        </Badge>
                      ))}
                    </div>
                  )}
                  
                  {showReasoning && ctx.reasoning && (
                    <Collapsible>
                      <CollapsibleTrigger className="flex items-center gap-1 text-sm text-slate-600 hover:text-slate-800">
                        <ChevronDown className="h-4 w-4" />
                        Ver raciocínio
                      </CollapsibleTrigger>
                      <CollapsibleContent className="mt-2 p-3 bg-slate-100 rounded text-sm text-slate-700">
                        {ctx.reasoning}
                      </CollapsibleContent>
                    </Collapsible>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {data && (
        <Card>
          <CardHeader>
            <CardTitle>Resumo da Análise</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <span className="font-medium">Onírico:</span> {aggregate.context_classification?.['onírico'] || 0}
              </div>
              <div>
                <span className="font-medium">Profético:</span> {aggregate.context_classification?.['profético'] || 0}
              </div>
              <div>
                <span className="font-medium">Alegórico:</span> {aggregate.context_classification?.['alegórico'] || 0}
              </div>
              <div>
                <span className="font-medium">Divino:</span> {aggregate.context_classification?.['divino'] || 0}
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

export default SimpleAnalysis