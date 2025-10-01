import { useState } from 'react'
import api from '@/services/api'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

const SimpleAnalysis = () => {
  const [text, setText] = useState('')
  const [mode, setMode] = useState('estrito')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [data, setData] = useState(null)

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

  const aggregate = data?.aggregate
  const byCanto = data?.by_canto || {}

  // Ordenar cantos I-X
  const cantoOrder = ['CANTO I', 'CANTO II', 'CANTO III', 'CANTO IV', 'CANTO V', 'CANTO VI', 'CANTO VII', 'CANTO VIII', 'CANTO IX', 'CANTO X']
  const sortedCantos = cantoOrder.filter(canto => byCanto[canto])

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
                            <div className="flex items-center gap-2 mb-2">
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
                            </div>
                            <p className="text-slate-700 italic mb-2">"{ctx.sentence}"</p>
                            {ctx.terms && ctx.terms.length > 0 && (
                              <div className="flex flex-wrap gap-1">
                                {ctx.terms.map((term, termIdx) => (
                                  <Badge key={termIdx} variant="outline" className="text-xs">
                                    {term.term}
                                  </Badge>
                                ))}
                              </div>
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