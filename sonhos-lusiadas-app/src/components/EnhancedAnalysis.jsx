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

const EnhancedAnalysis = () => {
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

  const aggregate = data?.aggregate
  const byCanto = data?.by_canto || {}

  // Ordenar cantos I-X
  const cantoOrder = ['CANTO I', 'CANTO II', 'CANTO III', 'CANTO IV', 'CANTO V', 'CANTO VI', 'CANTO VII', 'CANTO VIII', 'CANTO IX', 'CANTO X']
  const sortedCantos = cantoOrder.filter(canto => byCanto[canto])

  // Filtrar contextos
  const filteredContexts = useMemo(() => {
    if (!data) return []
    
    let contexts = []
    sortedCantos.forEach(canto => {
      const info = byCanto[canto]
      const cantoContexts = (info.dream_contexts || []).map(ctx => ({
        ...ctx,
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
    if (!data) return { barData: [], pieData: [], lineData: [] }

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

  const getContextTypeColor = (type) => {
    const colors = {
      'onírico': '#3b82f6',
      'profético': '#10b981',
      'alegórico': '#f59e0b',
      'divino': '#ef4444'
    }
    return colors[type] || '#6b7280'
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

  const exportToCSV = () => {
    if (!filteredContexts.length) return
    
    const headers = ['Canto', 'Estrofe', 'Tipo', 'Confiança', 'Raciocínio', 'Trecho', 'Termos']
    const csvContent = [
      headers.join(','),
      ...filteredContexts.map(ctx => [
        ctx.canto,
        ctx.stanza || '',
        ctx.context_type,
        ctx.confidence_score || 0,
        `"${(ctx.reasoning || '').replace(/"/g, '""')}"`,
        `"${ctx.sentence.replace(/"/g, '""')}"`,
        ctx.terms?.map(t => t.term).join(';') || ''
      ].join(','))
    ].join('\n')
    
    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'analise_sonhos_lusiadas.csv'
    a.click()
    URL.revokeObjectURL(url)
  }

  const exportToPDF = () => {
    // Implementação básica - em produção seria melhor usar uma biblioteca como jsPDF
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
          </style>
        </head>
        <body>
          <div class="header">
            <h1>Análise de Sonhos em Os Lusíadas</h1>
            <p>Relatório gerado em ${new Date().toLocaleDateString('pt-BR')}</p>
          </div>
          ${filteredContexts.map(ctx => `
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

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-slate-800 mb-2">Análise Avançada de Sonhos em Os Lusíadas</h1>
        <p className="text-slate-600">Análise completa com visualizações interativas, filtros e feedback</p>
      </div>

      {/* Entrada de Texto */}
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
          <div className="flex gap-4 items-center">
            <div className="w-48">
              <Select value={mode} onValueChange={setMode}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="estrito">Modo Estrito (apenas sonhos)</SelectItem>
                  <SelectItem value="default">Modo Completo</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Button onClick={handleAnalyze} disabled={loading} className="px-8">
              {loading ? 'Analisando...' : 'Analisar'}
            </Button>
            {error && <span className="text-red-600 text-sm">{error}</span>}
          </div>
        </CardContent>
      </Card>

      {/* Filtros e Busca */}
      {data && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Filter className="h-5 w-5" />
              Filtros e Busca
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div>
                <label className="text-sm font-medium mb-2 block">Buscar por texto</label>
                <div className="relative">
                  <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                  <Input
                    placeholder="Digite para buscar..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10"
                  />
                </div>
              </div>
              <div>
                <label className="text-sm font-medium mb-2 block">Tipo de contexto</label>
                <Select value={contextTypeFilter} onValueChange={setContextTypeFilter}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="todos">Todos os tipos</SelectItem>
                    <SelectItem value="onírico">Onírico</SelectItem>
                    <SelectItem value="profético">Profético</SelectItem>
                    <SelectItem value="alegórico">Alegórico</SelectItem>
                    <SelectItem value="divino">Divino</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <label className="text-sm font-medium mb-2 block">Confiança mínima</label>
                <div className="space-y-2">
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={confidenceFilter}
                    onChange={(e) => setConfidenceFilter(parseFloat(e.target.value))}
                    className="w-full"
                  />
                  <div className="text-sm text-gray-600">
                    {Math.round(confidenceFilter * 100)}%
                  </div>
                </div>
              </div>
              <div className="flex items-end">
                <Button
                  variant="outline"
                  onClick={() => setShowReasoning(!showReasoning)}
                  className="w-full"
                >
                  {showReasoning ? <EyeOff className="h-4 w-4 mr-2" /> : <Eye className="h-4 w-4 mr-2" />}
                  {showReasoning ? 'Ocultar' : 'Mostrar'} Raciocínio
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Estatísticas Gerais */}
      {aggregate && (
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
                </div>
              </TabsContent>
              
              <TabsContent value="types" className="mt-6">
                <div className="h-80">
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
                </div>
              </TabsContent>
              
              <TabsContent value="confidence" className="mt-6">
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={chartData.lineData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="canto" />
                      <YAxis domain={[0, 100]} />
                      <RechartsTooltip formatter={(value) => [`${value.toFixed(1)}%`, 'Confiança']} />
                      <Line type="monotone" dataKey="confidence" stroke="#8884d8" strokeWidth={2} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      )}

      {/* Trechos Filtrados */}
      {filteredContexts.length > 0 && (
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>
                Trechos Encontrados ({filteredContexts.length} total)
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

      {/* Resumo Final */}
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

export default EnhancedAnalysis
