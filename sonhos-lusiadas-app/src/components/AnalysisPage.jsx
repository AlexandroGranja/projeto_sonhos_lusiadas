import { useState, useRef } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Textarea } from '@/components/ui/textarea'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { useToast } from '@/hooks/use-toast'
import { 
  Upload, 
  FileText, 
  Brain, 
  BarChart3, 
  Download,
  Play,
  Pause,
  RefreshCw,
  CheckCircle,
  AlertCircle,
  FileUp,
  Sparkles,
  Type
} from 'lucide-react'

const AnalysisPage = () => {
  const [activeTab, setActiveTab] = useState('upload')
  const [file, setFile] = useState(null)
  const [textInput, setTextInput] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  const [progress, setProgress] = useState(0)
  const [results, setResults] = useState(null)
  const [analysisSteps, setAnalysisSteps] = useState([])
  const [isDragOver, setIsDragOver] = useState(false)
  const fileInputRef = useRef(null)
  const { toast } = useToast()

  const handleFileUpload = (event) => {
    const selectedFile = event.target.files[0]
    if (selectedFile) {
      processFile(selectedFile)
    }
  }

  const processFile = (selectedFile) => {
    // Validar tipo de arquivo
    const allowedTypes = ['text/plain', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
    if (!allowedTypes.includes(selectedFile.type) && !selectedFile.name.match(/\.(txt|pdf|docx)$/i)) {
      toast({
        title: "Tipo de arquivo não suportado",
        description: "Por favor, envie arquivos .txt, .pdf ou .docx",
        variant: "destructive"
      })
      return
    }

    // Validar tamanho (16MB)
    if (selectedFile.size > 16 * 1024 * 1024) {
      toast({
        title: "Arquivo muito grande",
        description: "O arquivo deve ter no máximo 16MB",
        variant: "destructive"
      })
      return
    }

    setFile(selectedFile)
    toast({
      title: "Arquivo carregado",
      description: `${selectedFile.name} foi carregado com sucesso`
    })
  }

  const handleDragOver = (event) => {
    event.preventDefault()
    setIsDragOver(true)
  }

  const handleDragLeave = (event) => {
    event.preventDefault()
    setIsDragOver(false)
  }

  const handleDrop = (event) => {
    event.preventDefault()
    setIsDragOver(false)
    
    const droppedFile = event.dataTransfer.files[0]
    if (droppedFile) {
      processFile(droppedFile)
    }
  }

  const simulateAnalysisSteps = () => {
    const steps = [
      { id: 1, name: 'Pré-processamento', description: 'Limpeza e tokenização do texto', duration: 1000 },
      { id: 2, name: 'Análise Léxica', description: 'Identificação de palavras-chave e lematização', duration: 1200 },
      { id: 3, name: 'Expansão Semântica', description: 'Identificando palavras relacionadas com IA', duration: 1500 },
      { id: 4, name: 'Análise de Contexto', description: 'Buscando padrões e classificando trechos', duration: 1800 },
      { id: 5, name: 'Classificação de Sonhos', description: 'Categorizando tipos de sonho (onírico, profético, alegórico)', duration: 1600 },
      { id: 6, name: 'Análise Estatística', description: 'Calculando frequências e distribuições', duration: 1000 },
      { id: 7, name: 'Geração de Visualizações', description: 'Criando gráficos e relatórios', duration: 1200 },
      { id: 8, name: 'Relatório Final', description: 'Compilando resultados e insights', duration: 800 }
    ]

    setAnalysisSteps(steps.map(step => ({ ...step, status: 'pending' })))
    
    let currentProgress = 0
    const totalDuration = steps.reduce((sum, step) => sum + step.duration, 0)
    
    // Processar cada step sequencialmente
    const processStep = (stepIndex) => {
      if (stepIndex >= steps.length) {
        // Todos os steps concluídos
        setResults({
          totalWords: 1247,
          uniqueWords: 342,
          dreamReferences: 23,
          cantos: 10,
          analysisTime: '9.1s',
          confidence: 94,
          dreamTypes: {
            onirico: 12,
            profetico: 6,
            alegorico: 4,
            divino: 1
          },
          wordCloud: [
            { word: 'sonho', frequency: 45, category: 'onírico' },
            { word: 'visão', frequency: 32, category: 'profético' },
            { word: 'sombra', frequency: 28, category: 'alegórico' },
            { word: 'glória', frequency: 24, category: 'divino' },
            { word: 'pesadelo', frequency: 18, category: 'onírico' },
            { word: 'fantasia', frequency: 15, category: 'ilusão' }
          ],
          cantoDistribution: [
            { canto: 'I', occurrences: 12, percentage: 15 },
            { canto: 'II', occurrences: 8, percentage: 10 },
            { canto: 'III', occurrences: 15, percentage: 19 },
            { canto: 'IV', occurrences: 6, percentage: 8 },
            { canto: 'V', occurrences: 11, percentage: 14 }
          ],
          insights: [
            'O tema do sonho aparece principalmente no Canto III, representando 19% das ocorrências',
            'Sonhos proféticos são mais frequentes nos cantos iniciais da obra',
            'A palavra "sonho" aparece 45 vezes, sendo a mais recorrente',
            'Há uma progressão narrativa clara no uso do tema onírico'
          ]
        })
        setIsProcessing(false)
        setActiveTab('results')
        toast({
          title: "Análise concluída!",
          description: "Resultados detalhados disponíveis na aba de resultados"
        })
        return
      }

      const step = steps[stepIndex]
      
      // Marcar como processando
      setAnalysisSteps(prev => prev.map(s => 
        s.id === step.id ? { ...s, status: 'processing' } : s
      ))
      
      // Simular processamento
      setTimeout(() => {
        // Atualizar progresso
        currentProgress += (step.duration / totalDuration) * 100
        setProgress(Math.min(currentProgress, 100))
        
        // Marcar como concluído
        setAnalysisSteps(prev => prev.map(s => 
          s.id === step.id ? { ...s, status: 'completed' } : s
        ))
        
        // Processar próximo step
        processStep(stepIndex + 1)
      }, step.duration)
    }
    
    // Iniciar processamento
    processStep(0)
  }

  const startAnalysis = async () => {
    if (!file && !textInput.trim()) {
      toast({
        title: "Nenhum conteúdo para analisar",
        description: "Por favor, envie um arquivo ou digite um texto",
        variant: "destructive"
      })
      return
    }

    setIsProcessing(true)
    setProgress(0)
    setResults(null)
    setActiveTab('processing')
    
    // Simular análise (substituir por chamada real à API)
    simulateAnalysisSteps()
  }

  const resetAnalysis = () => {
    setFile(null)
    setTextInput('')
    setIsProcessing(false)
    setProgress(0)
    setResults(null)
    setAnalysisSteps([])
    setActiveTab('upload')
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  // Funções de exportação
  const exportToPDF = () => {
    if (!results) return
    
    // Criar conteúdo HTML para conversão em PDF
    const htmlContent = `
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Relatório de Análise - Sonhos dos Lusíadas</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
        h1 { color: #1e293b; border-bottom: 3px solid #3b82f6; padding-bottom: 10px; }
        h2 { color: #374151; margin-top: 30px; }
        .summary { background: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0; }
        .metric { display: flex; justify-content: space-between; margin: 8px 0; }
        .metric strong { color: #1e293b; }
        .dream-type { background: #f1f5f9; padding: 15px; margin: 10px 0; border-left: 4px solid #3b82f6; }
        .word-item { display: flex; justify-content: space-between; margin: 5px 0; }
        .canto-item { background: #fef3c7; padding: 10px; margin: 5px 0; border-radius: 4px; }
        .insight { background: #ecfdf5; padding: 15px; margin: 10px 0; border-left: 4px solid #10b981; }
        .footer { margin-top: 40px; text-align: center; color: #6b7280; font-style: italic; }
    </style>
</head>
<body>
    <h1>Relatório de Análise - Sonhos dos Lusíadas</h1>
    
    <div class="summary">
        <h2>Resumo Geral</h2>
        <div class="metric"><strong>Palavras Totais:</strong> ${results.totalWords}</div>
        <div class="metric"><strong>Palavras Únicas:</strong> ${results.uniqueWords}</div>
        <div class="metric"><strong>Referências a Sonhos:</strong> ${results.dreamReferences}</div>
        <div class="metric"><strong>Cantos Identificados:</strong> ${results.cantos}</div>
        <div class="metric"><strong>Tempo de Análise:</strong> ${results.analysisTime}</div>
        <div class="metric"><strong>Confiança:</strong> ${results.confidence}%</div>
    </div>

    <h2>Tipos de Sonho</h2>
    ${results.dreamTypes ? Object.entries(results.dreamTypes).map(([type, count]) => 
      `<div class="dream-type"><strong>${type.charAt(0).toUpperCase() + type.slice(1)}:</strong> ${count} ocorrências</div>`
    ).join('') : ''}

    <h2>Palavras Mais Frequentes</h2>
    ${results.wordCloud ? results.wordCloud.map(item => 
      `<div class="word-item"><strong>${item.word}:</strong> ${item.frequency}x (${item.category})</div>`
    ).join('') : ''}

    <h2>Distribuição por Canto</h2>
    ${results.cantoDistribution ? results.cantoDistribution.map(canto => 
      `<div class="canto-item"><strong>Canto ${canto.canto}:</strong> ${canto.occurrences} ocorrências (${canto.percentage}%)</div>`
    ).join('') : ''}

    <h2>Insights da Análise</h2>
    ${results.insights ? results.insights.map((insight, index) => 
      `<div class="insight"><strong>${index + 1}.</strong> ${insight}</div>`
    ).join('') : ''}

    <div class="footer">
        Relatório gerado automaticamente pelo sistema de análise de sonhos dos Lusíadas<br>
        Data: ${new Date().toLocaleDateString('pt-BR')}
    </div>
</body>
</html>
    `.trim()

    const blob = new Blob([htmlContent], { type: 'text/html' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'relatorio-sonhos-lusiadas.html'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    
    toast({
      title: "Download iniciado",
      description: "Relatório HTML gerado (abra no navegador e imprima como PDF)"
    })
  }

  const exportToCSV = () => {
    if (!results) return
    
    const csvData = [
      ['Métrica', 'Valor'],
      ['Palavras Totais', results.totalWords],
      ['Palavras Únicas', results.uniqueWords],
      ['Referências a Sonhos', results.dreamReferences],
      ['Cantos Identificados', results.cantos],
      ['Tempo de Análise', results.analysisTime],
      ['Confiança (%)', results.confidence],
      ['', ''],
      ['Tipo de Sonho', 'Ocorrências'],
      ...(results.dreamTypes ? Object.entries(results.dreamTypes).map(([type, count]) => [type, count]) : []),
      ['', ''],
      ['Palavra', 'Frequência', 'Categoria'],
      ...(results.wordCloud ? results.wordCloud.map(item => [item.word, item.frequency, item.category]) : [])
    ]
    
    const csvContent = csvData.map(row => row.join(',')).join('\n')
    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'dados-sonhos-lusiadas.csv'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    
    toast({
      title: "Download iniciado",
      description: "Dados CSV sendo gerado..."
    })
  }

  const exportToJSON = () => {
    if (!results) return
    
    const jsonData = {
      metadata: {
        totalWords: results.totalWords,
        uniqueWords: results.uniqueWords,
        dreamReferences: results.dreamReferences,
        cantos: results.cantos,
        analysisTime: results.analysisTime,
        confidence: results.confidence,
        generatedAt: new Date().toISOString()
      },
      dreamTypes: results.dreamTypes,
      wordCloud: results.wordCloud,
      cantoDistribution: results.cantoDistribution,
      insights: results.insights
    }
    
    const blob = new Blob([JSON.stringify(jsonData, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'dados-sonhos-lusiadas.json'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    
    toast({
      title: "Download iniciado",
      description: "Dados JSON sendo gerado..."
    })
  }

  const exportToWord = () => {
    if (!results) return
    
    // Criar conteúdo RTF (Rich Text Format) que pode ser aberto no Word
    const rtfContent = `{\\rtf1\\ansi\\deff0 {\\fonttbl {\\f0 Times New Roman;}}
{\\colortbl;\\red0\\green0\\blue0;\\red0\\green0\\blue255;\\red0\\green128\\blue0;\\red255\\green0\\blue0;}
\\f0\\fs24

{\\b\\fs32 Relatório de Análise - Sonhos dos Lusíadas}\\par\\par

{\\b\\fs28 RESUMO GERAL}\\par
{\\b Palavras Totais:} ${results.totalWords}\\par
{\\b Palavras Únicas:} ${results.uniqueWords}\\par
{\\b Referências a Sonhos:} ${results.dreamReferences}\\par
{\\b Cantos Identificados:} ${results.cantos}\\par
{\\b Tempo de Análise:} ${results.analysisTime}\\par
{\\b Confiança:} ${results.confidence}%\\par\\par

{\\b\\fs28 TIPOS DE SONHO}\\par
${results.dreamTypes ? Object.entries(results.dreamTypes).map(([type, count]) => 
  `{\\b ${type.charAt(0).toUpperCase() + type.slice(1)}:} ${count} ocorrências\\par`
).join('') : ''}\\par

{\\b\\fs28 PALAVRAS MAIS FREQUENTES}\\par
${results.wordCloud ? results.wordCloud.map(item => 
  `{\\b ${item.word}:} ${item.frequency}x (${item.category})\\par`
).join('') : ''}\\par

{\\b\\fs28 DISTRIBUIÇÃO POR CANTO}\\par
${results.cantoDistribution ? results.cantoDistribution.map(canto => 
  `{\\b Canto ${canto.canto}:} ${canto.occurrences} ocorrências (${canto.percentage}%)\\par`
).join('') : ''}\\par

{\\b\\fs28 INSIGHTS DA ANÁLISE}\\par
${results.insights ? results.insights.map((insight, index) => 
  `{\\b ${index + 1}.} ${insight}\\par`
).join('') : ''}\\par\\par

{\\i Relatório gerado automaticamente pelo sistema de análise de sonhos dos Lusíadas}\\par
{\\i Data: ${new Date().toLocaleDateString('pt-BR')}}
}`

    const blob = new Blob([rtfContent], { type: 'application/rtf' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'relatorio-sonhos-lusiadas.rtf'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    
    toast({
      title: "Download iniciado",
      description: "Relatório RTF gerado (abra no Word)"
    })
  }

  const exportToPowerPoint = () => {
    if (!results) return
    
    // Criar conteúdo HTML que pode ser convertido para PowerPoint
    const htmlContent = `
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Apresentação - Análise de Sonhos dos Lusíadas</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .slide { background: white; margin: 20px 0; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); page-break-after: always; }
        .slide h1 { color: #1e293b; font-size: 32px; margin-bottom: 20px; text-align: center; }
        .slide h2 { color: #374151; font-size: 24px; margin: 30px 0 15px 0; border-bottom: 2px solid #3b82f6; }
        .slide h3 { color: #4b5563; font-size: 20px; margin: 20px 0 10px 0; }
        .metric { background: #f8fafc; padding: 15px; margin: 10px 0; border-left: 4px solid #3b82f6; }
        .metric strong { color: #1e293b; }
        .dream-type { background: #f1f5f9; padding: 12px; margin: 8px 0; border-radius: 4px; }
        .word-item { background: #fef3c7; padding: 10px; margin: 5px 0; border-radius: 4px; }
        .canto-item { background: #ecfdf5; padding: 10px; margin: 5px 0; border-radius: 4px; }
        .insight { background: #fef2f2; padding: 12px; margin: 8px 0; border-left: 4px solid #ef4444; }
        .conclusion { background: #f0f9ff; padding: 20px; border-radius: 8px; margin: 20px 0; }
        .footer { text-align: center; color: #6b7280; font-style: italic; margin-top: 20px; }
        @media print { .slide { page-break-after: always; } }
    </style>
</head>
<body>
    <div class="slide">
        <h1>Análise de Sonhos dos Lusíadas</h1>
        <h2>Resumo Executivo</h2>
        <div class="metric"><strong>Palavras Totais:</strong> ${results.totalWords}</div>
        <div class="metric"><strong>Referências a Sonhos:</strong> ${results.dreamReferences}</div>
        <div class="metric"><strong>Cantos Analisados:</strong> ${results.cantos}</div>
        <div class="metric"><strong>Confiança da Análise:</strong> ${results.confidence}%</div>
        <div class="footer">Sistema de Análise Literária com IA</div>
    </div>

    <div class="slide">
        <h2>Tipos de Sonho Identificados</h2>
        ${results.dreamTypes ? Object.entries(results.dreamTypes).map(([type, count]) => 
          `<div class="dream-type"><strong>${type.charAt(0).toUpperCase() + type.slice(1)}:</strong> ${count} ocorrências</div>`
        ).join('') : ''}
        <div class="footer">Classificação automática por IA</div>
    </div>

    <div class="slide">
        <h2>Palavras-Chave Mais Frequentes</h2>
        ${results.wordCloud ? results.wordCloud.slice(0, 10).map(item => 
          `<div class="word-item"><strong>${item.word}</strong> (${item.frequency}x) - ${item.category}</div>`
        ).join('') : ''}
        <div class="footer">Análise de frequência lexical</div>
    </div>

    <div class="slide">
        <h2>Distribuição por Canto</h2>
        ${results.cantoDistribution ? results.cantoDistribution.map(canto => 
          `<div class="canto-item"><strong>Canto ${canto.canto}:</strong> ${canto.occurrences} ocorrências (${canto.percentage}%)</div>`
        ).join('') : ''}
        <div class="footer">Padrões de distribuição narrativa</div>
    </div>

    <div class="slide">
        <h2>Insights Principais</h2>
        ${results.insights ? results.insights.map((insight, index) => 
          `<div class="insight"><strong>${index + 1}.</strong> ${insight}</div>`
        ).join('') : ''}
        <div class="footer">Descobertas automáticas da análise</div>
    </div>

    <div class="slide">
        <h2>Conclusões</h2>
        <div class="conclusion">
            <h3>Principais Descobertas:</h3>
            <div class="metric">• Análise concluída com ${results.confidence}% de confiança</div>
            <div class="metric">• ${results.dreamReferences} referências a sonhos identificadas</div>
            <div class="metric">• Padrões claros identificados na distribuição por cantos</div>
            <div class="metric">• Insights valiosos para análise literária</div>
        </div>
        <div class="footer">Relatório gerado automaticamente - ${new Date().toLocaleDateString('pt-BR')}</div>
    </div>
</body>
</html>
    `.trim()

    const blob = new Blob([htmlContent], { type: 'text/html' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'apresentacao-sonhos-lusiadas.html'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    
    toast({
      title: "Download iniciado",
      description: "Apresentação HTML gerada (abra no navegador e salve como PowerPoint)"
    })
  }

  const exportVisualizations = () => {
    if (!results) return
    
    // Criar um canvas para gerar uma imagem
    const canvas = document.createElement('canvas')
    const ctx = canvas.getContext('2d')
    canvas.width = 800
    canvas.height = 600
    
    // Fundo branco
    ctx.fillStyle = '#ffffff'
    ctx.fillRect(0, 0, canvas.width, canvas.height)
    
    // Título
    ctx.fillStyle = '#1e293b'
    ctx.font = 'bold 24px Arial'
    ctx.textAlign = 'center'
    ctx.fillText('Análise de Sonhos dos Lusíadas', canvas.width / 2, 40)
    
    // Subtítulo
    ctx.fillStyle = '#64748b'
    ctx.font = '16px Arial'
    ctx.fillText('Visualização dos Resultados', canvas.width / 2, 70)
    
    // Estatísticas
    ctx.fillStyle = '#1e293b'
    ctx.font = 'bold 18px Arial'
    ctx.textAlign = 'left'
    ctx.fillText('Estatísticas Principais:', 50, 120)
    
    const stats = [
      `Palavras Totais: ${results.totalWords}`,
      `Referências a Sonhos: ${results.dreamReferences}`,
      `Cantos: ${results.cantos}`,
      `Confiança: ${results.confidence}%`
    ]
    
    stats.forEach((stat, index) => {
      ctx.fillStyle = '#475569'
      ctx.font = '14px Arial'
      ctx.fillText(stat, 50, 150 + (index * 25))
    })
    
    // Converter para blob e fazer download
    canvas.toBlob((blob) => {
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'visualizacao-sonhos-lusiadas.png'
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    })
    
    toast({
      title: "Download iniciado",
      description: "Visualizações sendo geradas..."
    })
  }

  const getStepIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-green-600 animate-pulse" />
      case 'processing':
        return <RefreshCw className="h-5 w-5 text-blue-600 animate-spin" />
      default:
        return <div className="h-5 w-5 rounded-full border-2 border-slate-300" />
    }
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center space-y-4">
        <h1 className="text-3xl font-bold text-slate-800 flex items-center justify-center gap-2">
          <Brain className="h-8 w-8 text-blue-600" />
          Análise Literária com IA
        </h1>
        <p className="text-lg text-slate-600 max-w-2xl mx-auto">
          Faça upload de um texto ou cole o conteúdo para análise avançada com processamento de linguagem natural
        </p>
      </div>

      {/* Main Content */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="upload" className="flex items-center gap-2">
            <Upload className="h-4 w-4" />
            Upload
          </TabsTrigger>
          <TabsTrigger value="processing" disabled={!isProcessing && !results}>
            <RefreshCw className="h-4 w-4" />
            Processamento
          </TabsTrigger>
          <TabsTrigger value="results" disabled={!results}>
            <BarChart3 className="h-4 w-4" />
            Resultados
          </TabsTrigger>
          <TabsTrigger value="export" disabled={!results}>
            <Download className="h-4 w-4" />
            Exportar
          </TabsTrigger>
        </TabsList>

        {/* Upload Tab */}
        <TabsContent value="upload" className="space-y-6">
          <div className="grid md:grid-cols-2 gap-6">
            {/* File Upload */}
            <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <CardHeader className="text-center">
                <div className="mx-auto w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
                  <FileUp className="h-8 w-8 text-blue-600" />
                </div>
                <CardTitle className="text-xl text-slate-800">
                  Upload de Arquivo
                </CardTitle>
                <CardDescription className="text-base">
                  Envie arquivos .txt, .pdf ou .docx (máximo 16MB)
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div 
                  className={`border-2 border-dashed rounded-xl p-8 text-center transition-all duration-300 cursor-pointer ${
                    isDragOver 
                      ? 'border-blue-400 bg-gradient-to-br from-blue-50 to-purple-50 scale-105 shadow-lg' 
                      : 'border-slate-300 hover:border-blue-400 hover:bg-gradient-to-br hover:from-slate-50 hover:to-blue-50 hover:shadow-md'
                  }`}
                  onClick={() => fileInputRef.current?.click()}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                >
                  <FileText className={`h-16 w-16 mx-auto mb-4 transition-all duration-300 ${
                    isDragOver ? 'text-blue-500 scale-110' : 'text-slate-400'
                  }`} />
                  <p className={`text-lg mb-2 transition-colors ${
                    isDragOver ? 'text-blue-600 font-semibold' : 'text-slate-600'
                  }`}>
                    {isDragOver ? 'Solte o arquivo aqui' : 'Clique para selecionar ou arraste um arquivo aqui'}
                  </p>
                  <p className="text-sm text-slate-500">
                    Formatos suportados: TXT, PDF, DOCX
                  </p>
                  <div className="mt-4 flex justify-center space-x-2">
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                  </div>
                </div>
                
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".txt,.pdf,.docx"
                  onChange={handleFileUpload}
                  className="hidden"
                />
                
                {file && (
                  <div className="flex items-center justify-between p-4 bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl border border-green-200">
                    <div className="flex items-center gap-3">
                      <CheckCircle className="h-6 w-6 text-green-600" />
                      <div>
                        <span className="text-sm font-semibold text-green-800">{file.name}</span>
                        <p className="text-xs text-green-600">Arquivo carregado com sucesso</p>
                      </div>
                    </div>
                    <Badge variant="secondary" className="bg-green-100 text-green-800">
                      {(file.size / 1024 / 1024).toFixed(2)} MB
                    </Badge>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Text Input */}
            <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <CardHeader className="text-center">
                <div className="mx-auto w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mb-4">
                  <Type className="h-8 w-8 text-purple-600" />
                </div>
                <CardTitle className="text-xl text-slate-800">
                  Entrada de Texto
                </CardTitle>
                <CardDescription className="text-base">
                  Cole ou digite o texto diretamente
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="relative">
                  <Textarea
                    placeholder="Cole aqui o texto que deseja analisar..."
                    value={textInput}
                    onChange={(e) => setTextInput(e.target.value)}
                    className="min-h-[200px] resize-none border-2 focus:border-purple-400 transition-colors duration-200"
                  />
                  <div className="absolute bottom-2 right-2 text-xs text-slate-400">
                    {textInput.length} caracteres
                  </div>
                </div>
                
                <div className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                  <div className="flex items-center gap-2">
                    <div className={`w-2 h-2 rounded-full ${
                      textInput.length >= 100 ? 'bg-green-500' : 'bg-yellow-500'
                    }`} />
                    <span className="text-sm text-slate-600">
                      {textInput.length >= 100 ? 'Texto válido' : 'Mínimo: 100 caracteres'}
                    </span>
                  </div>
                  <Badge variant={textInput.length >= 100 ? 'default' : 'secondary'}>
                    {textInput.length >= 100 ? '✓ Pronto' : '⚠️ Insuficiente'}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Analysis Options */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Sparkles className="h-5 w-5" />
                Opções de Análise
              </CardTitle>
              <CardDescription>
                Configure os parâmetros da análise
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid md:grid-cols-3 gap-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium">Expansão Semântica</label>
                  <div className="flex gap-2">
                    <Badge variant="outline">Claude Sonnet 4</Badge>
                    <Badge variant="outline">BERTimbau</Badge>
                  </div>
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Classificação</label>
                  <Badge variant="outline">Automática com IA</Badge>
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Visualizações</label>
                  <Badge variant="outline">Completas</Badge>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Start Analysis Button */}
          <div className="flex justify-center">
            <Button 
              size="lg" 
              onClick={startAnalysis}
              disabled={isProcessing || (!file && !textInput.trim())}
              className="px-8 py-3 text-lg"
            >
              {isProcessing ? (
                <>
                  <RefreshCw className="mr-2 h-5 w-5 animate-spin" />
                  Processando...
                </>
              ) : (
                <>
                  <Play className="mr-2 h-5 w-5" />
                  Iniciar Análise
                </>
              )}
            </Button>
          </div>
        </TabsContent>

        {/* Processing Tab */}
        <TabsContent value="processing" className="space-y-6">
          <Card className="border-0 shadow-lg bg-gradient-to-br from-blue-50 to-purple-50">
            <CardHeader className="text-center">
              <div className="mx-auto w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
                <RefreshCw className="h-8 w-8 text-blue-600 animate-spin" />
              </div>
              <CardTitle className="text-2xl text-slate-800">
                Processamento em Andamento
              </CardTitle>
              <CardDescription className="text-lg">
                Acompanhe o progresso da análise em tempo real
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-8">
              {/* Progress Bar */}
              <div className="space-y-4">
                <div className="flex justify-between text-lg font-medium">
                  <span className="text-slate-700">Progresso Geral</span>
                  <span className="text-blue-600">{Math.round(progress)}%</span>
                </div>
                <div className="relative">
                  <Progress value={progress} className="h-3 bg-slate-200" />
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full opacity-20" 
                       style={{ width: `${progress}%` }} />
                </div>
              </div>

              {/* Analysis Steps */}
              <div className="space-y-3">
                {analysisSteps.map((step, index) => (
                  <div key={step.id} className={`flex items-center gap-4 p-4 rounded-xl transition-all duration-300 ${
                    step.status === 'processing' ? 'bg-blue-100 border-2 border-blue-300 shadow-md scale-105' :
                    step.status === 'completed' ? 'bg-green-50 border border-green-200' :
                    'bg-white border border-slate-200'
                  }`}>
                    <div className="flex-shrink-0">
                      {getStepIcon(step.status)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <h4 className="font-semibold text-slate-800">{step.name}</h4>
                      <p className="text-sm text-slate-600 mt-1">{step.description}</p>
                    </div>
                    <div className="flex-shrink-0">
                      <Badge variant={
                        step.status === 'completed' ? 'default' : 
                        step.status === 'processing' ? 'secondary' : 'outline'
                      } className="text-xs">
                        {step.status === 'completed' ? '✓ Concluído' : 
                         step.status === 'processing' ? '⚡ Processando' : '⏳ Aguardando'}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>

              {/* Processing Animation */}
              {isProcessing && (
                <div className="text-center space-y-4">
                  <div className="flex justify-center space-x-2">
                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                  <p className="text-slate-600 text-sm">Processando dados com inteligência artificial...</p>
                  <Button variant="outline" onClick={resetAnalysis} className="mt-4">
                    <Pause className="mr-2 h-4 w-4" />
                    Cancelar Análise
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Results Tab */}
        <TabsContent value="results" className="space-y-6">
          {results && (
            <>
              {/* Summary Cards */}
              <div className="grid md:grid-cols-4 gap-4">
                <Card>
                  <CardContent className="p-6 text-center">
                    <div className="text-2xl font-bold text-blue-600">{results.totalWords}</div>
                    <div className="text-sm text-slate-600">Palavras Totais</div>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="p-6 text-center">
                    <div className="text-2xl font-bold text-green-600">{results.dreamReferences}</div>
                    <div className="text-sm text-slate-600">Referências a Sonhos</div>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="p-6 text-center">
                    <div className="text-2xl font-bold text-purple-600">{results.cantos}</div>
                    <div className="text-sm text-slate-600">Cantos Identificados</div>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="p-6 text-center">
                    <div className="text-2xl font-bold text-amber-600">{results.confidence}%</div>
                    <div className="text-sm text-slate-600">Confiança</div>
                  </CardContent>
                </Card>
              </div>

              {/* Detailed Results */}
              <div className="grid lg:grid-cols-2 gap-6">
                {/* Word Cloud Visualization */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <BarChart3 className="h-5 w-5" />
                      Nuvem de Palavras
                    </CardTitle>
                    <CardDescription>
                      Palavras mais frequentes relacionadas a sonhos
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {results.wordCloud?.slice(0, 8).map((item, index) => (
                        <div key={index} className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <div className={`w-3 h-3 rounded-full ${
                              item.category === 'onírico' ? 'bg-blue-500' :
                              item.category === 'profético' ? 'bg-green-500' :
                              item.category === 'alegórico' ? 'bg-purple-500' :
                              item.category === 'divino' ? 'bg-yellow-500' : 'bg-gray-500'
                            }`} />
                            <span className="font-medium">{item.word}</span>
                            <Badge variant="outline" className="text-xs">
                              {item.category}
                            </Badge>
                          </div>
                          <div className="text-sm text-slate-600">
                            {item.frequency}x
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* Dream Types Distribution */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <BarChart3 className="h-5 w-5" />
                      Tipos de Sonho
                    </CardTitle>
                    <CardDescription>
                      Distribuição por categoria
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {results.dreamTypes && Object.entries(results.dreamTypes).map(([type, count]) => (
                        <div key={type} className="space-y-2">
                          <div className="flex justify-between text-sm">
                            <span className="capitalize">{type}</span>
                            <span className="font-medium">{count}</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div 
                              className={`h-2 rounded-full ${
                                type === 'onirico' ? 'bg-blue-500' :
                                type === 'profetico' ? 'bg-green-500' :
                                type === 'alegorico' ? 'bg-purple-500' : 'bg-yellow-500'
                              }`}
                              style={{ 
                                width: `${(count / results.dreamReferences) * 100}%` 
                              }}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Canto Distribution */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <BarChart3 className="h-5 w-5" />
                    Distribuição por Canto
                  </CardTitle>
                  <CardDescription>
                    Ocorrências de referências a sonhos em cada canto
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                    {results.cantoDistribution?.map((canto, index) => (
                      <div key={index} className="text-center p-4 border rounded-lg">
                        <div className="text-2xl font-bold text-blue-600">{canto.occurrences}</div>
                        <div className="text-sm text-slate-600">Canto {canto.canto}</div>
                        <div className="text-xs text-slate-500">{canto.percentage}%</div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Insights */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Brain className="h-5 w-5" />
                    Insights da Análise
                  </CardTitle>
                  <CardDescription>
                    Descobertas importantes sobre o tema dos sonhos
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {results.insights?.map((insight, index) => (
                      <div key={index} className="flex items-start gap-3 p-4 bg-blue-50 rounded-lg">
                        <div className="w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0">
                          {index + 1}
                        </div>
                        <p className="text-slate-700">{insight}</p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </>
          )}
        </TabsContent>

        {/* Export Tab */}
        <TabsContent value="export" className="space-y-6">
          <Card className="border-0 shadow-lg">
            <CardHeader className="text-center">
              <div className="mx-auto w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-4">
                <Download className="h-8 w-8 text-green-600" />
              </div>
              <CardTitle className="text-2xl text-slate-800">
                Exportar Resultados
              </CardTitle>
              <CardDescription className="text-lg">
                Baixe os resultados da análise em diferentes formatos
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-8">
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                <Button 
                  variant="outline" 
                  className="h-24 flex-col hover:bg-blue-50 hover:border-blue-300 transition-all duration-200"
                  onClick={exportToPDF}
                >
                  <FileText className="h-8 w-8 mb-2 text-blue-600" />
                  <span className="font-semibold">Relatório PDF</span>
                  <span className="text-xs text-slate-500">Análise completa</span>
                </Button>
                
                <Button 
                  variant="outline" 
                  className="h-24 flex-col hover:bg-green-50 hover:border-green-300 transition-all duration-200"
                  onClick={exportToCSV}
                >
                  <BarChart3 className="h-8 w-8 mb-2 text-green-600" />
                  <span className="font-semibold">Dados CSV</span>
                  <span className="text-xs text-slate-500">Dados brutos</span>
                </Button>
                
                <Button 
                  variant="outline" 
                  className="h-24 flex-col hover:bg-purple-50 hover:border-purple-300 transition-all duration-200"
                  onClick={exportVisualizations}
                >
                  <Sparkles className="h-8 w-8 mb-2 text-purple-600" />
                  <span className="font-semibold">Visualizações</span>
                  <span className="text-xs text-slate-500">Gráficos PNG</span>
                </Button>
                
                <Button 
                  variant="outline" 
                  className="h-24 flex-col hover:bg-orange-50 hover:border-orange-300 transition-all duration-200"
                  onClick={exportToWord}
                >
                  <FileText className="h-8 w-8 mb-2 text-orange-600" />
                  <span className="font-semibold">Relatório Word</span>
                  <span className="text-xs text-slate-500">Documento editável</span>
                </Button>
                
                <Button 
                  variant="outline" 
                  className="h-24 flex-col hover:bg-red-50 hover:border-red-300 transition-all duration-200"
                  onClick={exportToPowerPoint}
                >
                  <BarChart3 className="h-8 w-8 mb-2 text-red-600" />
                  <span className="font-semibold">Apresentação</span>
                  <span className="text-xs text-slate-500">PowerPoint</span>
                </Button>
                
                <Button 
                  variant="outline" 
                  className="h-24 flex-col hover:bg-indigo-50 hover:border-indigo-300 transition-all duration-200"
                  onClick={exportToJSON}
                >
                  <Sparkles className="h-8 w-8 mb-2 text-indigo-600" />
                  <span className="font-semibold">Dados JSON</span>
                  <span className="text-xs text-slate-500">Estruturado</span>
                </Button>
              </div>
              
              {/* Export Summary */}
              <div className="bg-slate-50 rounded-lg p-6">
                <h3 className="font-semibold text-slate-800 mb-4">Resumo da Análise</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">{results?.totalWords || 0}</div>
                    <div className="text-slate-600">Palavras</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">{results?.dreamReferences || 0}</div>
                    <div className="text-slate-600">Referências</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-purple-600">{results?.cantos || 0}</div>
                    <div className="text-slate-600">Cantos</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-orange-600">{results?.confidence || 0}%</div>
                    <div className="text-slate-600">Confiança</div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Reset Button */}
      {(file || textInput || results) && (
        <div className="text-center">
          <Button variant="outline" onClick={resetAnalysis}>
            <RefreshCw className="mr-2 h-4 w-4" />
            Nova Análise
          </Button>
        </div>
      )}
    </div>
  )
}

export default AnalysisPage
