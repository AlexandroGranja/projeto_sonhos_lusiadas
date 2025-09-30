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
  Sparkles
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
      { id: 1, name: 'Pré-processamento', description: 'Limpeza e tokenização do texto', duration: 2000 },
      { id: 2, name: 'Expansão Semântica', description: 'Identificando palavras relacionadas com IA', duration: 3000 },
      { id: 3, name: 'Análise de Contexto', description: 'Buscando padrões e classificando trechos', duration: 4000 },
      { id: 4, name: 'Geração de Visualizações', description: 'Criando gráficos e relatórios', duration: 2000 }
    ]

    setAnalysisSteps(steps.map(step => ({ ...step, status: 'pending' })))
    
    let currentProgress = 0
    const totalDuration = steps.reduce((sum, step) => sum + step.duration, 0)
    
    steps.forEach((step, index) => {
      setTimeout(() => {
        setAnalysisSteps(prev => prev.map(s => 
          s.id === step.id ? { ...s, status: 'processing' } : s
        ))
        
        setTimeout(() => {
          currentProgress += (step.duration / totalDuration) * 100
          setProgress(currentProgress)
          
          setAnalysisSteps(prev => prev.map(s => 
            s.id === step.id ? { ...s, status: 'completed' } : s
          ))
          
          if (index === steps.length - 1) {
            // Simular resultados
            setTimeout(() => {
              setResults({
                totalWords: 1247,
                uniqueWords: 342,
                dreamReferences: 23,
                cantos: 10,
                analysisTime: '2.3s',
                confidence: 94
              })
              setIsProcessing(false)
              toast({
                title: "Análise concluída!",
                description: "Resultados disponíveis na aba de resultados"
              })
            }, 500)
          }
        }, step.duration)
      }, steps.slice(0, index).reduce((sum, s) => sum + s.duration, 0))
    })
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
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileUp className="h-5 w-5" />
                  Upload de Arquivo
                </CardTitle>
                <CardDescription>
                  Envie arquivos .txt, .pdf ou .docx (máximo 16MB)
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div 
                  className={`border-2 border-dashed rounded-lg p-8 text-center transition-all duration-200 cursor-pointer ${
                    isDragOver 
                      ? 'border-blue-400 bg-blue-50 scale-105' 
                      : 'border-slate-300 hover:border-blue-400 hover:bg-slate-50'
                  }`}
                  onClick={() => fileInputRef.current?.click()}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                >
                  <FileText className={`h-12 w-12 mx-auto mb-4 transition-colors ${
                    isDragOver ? 'text-blue-500' : 'text-slate-400'
                  }`} />
                  <p className={`mb-2 transition-colors ${
                    isDragOver ? 'text-blue-600 font-medium' : 'text-slate-600'
                  }`}>
                    {isDragOver ? 'Solte o arquivo aqui' : 'Clique para selecionar ou arraste um arquivo aqui'}
                  </p>
                  <p className="text-sm text-slate-500">
                    Formatos suportados: TXT, PDF, DOCX
                  </p>
                </div>
                
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".txt,.pdf,.docx"
                  onChange={handleFileUpload}
                  className="hidden"
                />
                
                {file && (
                  <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                    <div className="flex items-center gap-2">
                      <CheckCircle className="h-5 w-5 text-green-600" />
                      <span className="text-sm font-medium">{file.name}</span>
                    </div>
                    <Badge variant="secondary">
                      {(file.size / 1024 / 1024).toFixed(2)} MB
                    </Badge>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Text Input */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5" />
                  Entrada de Texto
                </CardTitle>
                <CardDescription>
                  Cole ou digite o texto diretamente
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Textarea
                  placeholder="Cole aqui o texto que deseja analisar..."
                  value={textInput}
                  onChange={(e) => setTextInput(e.target.value)}
                  className="min-h-[200px] resize-none"
                />
                <div className="mt-2 text-sm text-slate-500">
                  {textInput.length} caracteres
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
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <RefreshCw className="h-5 w-5 animate-spin" />
                Processamento em Andamento
              </CardTitle>
              <CardDescription>
                Acompanhe o progresso da análise em tempo real
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Progress Bar */}
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Progresso Geral</span>
                  <span>{Math.round(progress)}%</span>
                </div>
                <Progress value={progress} className="h-2" />
              </div>

              {/* Analysis Steps */}
              <div className="space-y-4">
                {analysisSteps.map((step) => (
                  <div key={step.id} className="flex items-center gap-4 p-4 rounded-lg bg-slate-50">
                    {getStepIcon(step.status)}
                    <div className="flex-1">
                      <h4 className="font-medium">{step.name}</h4>
                      <p className="text-sm text-slate-600">{step.description}</p>
                    </div>
                    <Badge variant={
                      step.status === 'completed' ? 'default' : 
                      step.status === 'processing' ? 'secondary' : 'outline'
                    }>
                      {step.status === 'completed' ? 'Concluído' : 
                       step.status === 'processing' ? 'Processando' : 'Aguardando'}
                    </Badge>
                  </div>
                ))}
              </div>

              {isProcessing && (
                <div className="text-center">
                  <Button variant="outline" onClick={resetAnalysis}>
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
              <Card>
                <CardHeader>
                  <CardTitle>Resultados Detalhados</CardTitle>
                  <CardDescription>
                    Análise completa do texto processado
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="text-center py-8">
                    <BarChart3 className="h-16 w-16 text-slate-400 mx-auto mb-4" />
                    <p className="text-slate-600">
                      Visualizações detalhadas serão exibidas aqui após a implementação completa
                    </p>
                  </div>
                </CardContent>
              </Card>
            </>
          )}
        </TabsContent>

        {/* Export Tab */}
        <TabsContent value="export" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Download className="h-5 w-5" />
                Exportar Resultados
              </CardTitle>
              <CardDescription>
                Baixe os resultados da análise em diferentes formatos
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid md:grid-cols-3 gap-4">
                <Button variant="outline" className="h-20 flex-col">
                  <FileText className="h-6 w-6 mb-2" />
                  Relatório PDF
                </Button>
                <Button variant="outline" className="h-20 flex-col">
                  <BarChart3 className="h-6 w-6 mb-2" />
                  Dados CSV
                </Button>
                <Button variant="outline" className="h-20 flex-col">
                  <Sparkles className="h-6 w-6 mb-2" />
                  Visualizações
                </Button>
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
