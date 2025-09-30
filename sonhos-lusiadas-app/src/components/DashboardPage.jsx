import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { 
  BarChart3, 
  TrendingUp, 
  FileText, 
  Brain,
  Clock,
  Users,
  Download,
  RefreshCw,
  Eye,
  BookOpen,
  Sparkles,
  PieChart,
  Activity
} from 'lucide-react'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart as RechartsPieChart,
  Cell,
  LineChart,
  Line,
  Area,
  AreaChart
} from 'recharts'

const DashboardPage = () => {
  const [activeTab, setActiveTab] = useState('overview')
  const [isLoading, setIsLoading] = useState(false)

  // Dados simulados para demonstração
  const overviewStats = [
    { title: 'Análises Realizadas', value: '1,247', change: '+12%', icon: FileText, color: 'text-blue-600' },
    { title: 'Textos Processados', value: '342', change: '+8%', icon: BookOpen, color: 'text-green-600' },
    { title: 'Palavras Analisadas', value: '2.1M', change: '+15%', icon: Brain, color: 'text-purple-600' },
    { title: 'Tempo Médio', value: '2.3s', change: '-5%', icon: Clock, color: 'text-amber-600' }
  ]

  const wordFrequencyData = [
    { word: 'sonho', frequency: 45, category: 'onírico' },
    { word: 'visão', frequency: 32, category: 'profético' },
    { word: 'sombra', frequency: 28, category: 'alegórico' },
    { word: 'glória', frequency: 24, category: 'divino' },
    { word: 'pesadelo', frequency: 18, category: 'onírico' },
    { word: 'fantasia', frequency: 15, category: 'ilusão' },
    { word: 'profecia', frequency: 12, category: 'profético' },
    { word: 'miragem', frequency: 10, category: 'ilusão' }
  ]

  const cantoDistributionData = [
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
  ]

  const dreamTypesData = [
    { name: 'Onírico', value: 35, color: '#3B82F6' },
    { name: 'Profético', value: 28, color: '#10B981' },
    { name: 'Alegórico', value: 20, color: '#8B5CF6' },
    { name: 'Divino', value: 12, color: '#F59E0B' },
    { name: 'Ilusão', value: 5, color: '#EF4444' }
  ]

  const analysisTimelineData = [
    { date: '2024-01', analyses: 45, accuracy: 89 },
    { date: '2024-02', analyses: 52, accuracy: 91 },
    { date: '2024-03', analyses: 48, accuracy: 93 },
    { date: '2024-04', analyses: 61, accuracy: 94 },
    { date: '2024-05', analyses: 58, accuracy: 95 },
    { date: '2024-06', analyses: 67, accuracy: 96 }
  ]

  const recentAnalyses = [
    { id: 1, title: 'Os Lusíadas - Canto I', type: 'Épico', status: 'Concluído', confidence: 94, date: '2024-06-15' },
    { id: 2, title: 'Sonetos de Camões', type: 'Lírico', status: 'Processando', confidence: null, date: '2024-06-15' },
    { id: 3, title: 'Auto da Barca do Inferno', type: 'Teatro', status: 'Concluído', confidence: 87, date: '2024-06-14' },
    { id: 4, title: 'Mensagem - Fernando Pessoa', type: 'Épico', status: 'Concluído', confidence: 92, date: '2024-06-14' },
    { id: 5, title: 'Rimas de Camões', type: 'Lírico', status: 'Erro', confidence: null, date: '2024-06-13' }
  ]

  const refreshData = () => {
    setIsLoading(true)
    setTimeout(() => {
      setIsLoading(false)
    }, 1000)
  }

  const getStatusBadge = (status) => {
    const variants = {
      'Concluído': 'default',
      'Processando': 'secondary',
      'Erro': 'destructive'
    }
    return <Badge variant={variants[status] || 'outline'}>{status}</Badge>
  }

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-slate-800 flex items-center gap-2">
            <BarChart3 className="h-8 w-8 text-blue-600" />
            Dashboard Administrativo
          </h1>
          <p className="text-lg text-slate-600 mt-2">
            Visão geral das análises e métricas do sistema
          </p>
        </div>
        <Button onClick={refreshData} disabled={isLoading}>
          <RefreshCw className={`mr-2 h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
          Atualizar
        </Button>
      </div>

      {/* Main Content */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="overview">Visão Geral</TabsTrigger>
          <TabsTrigger value="analytics">Análises</TabsTrigger>
          <TabsTrigger value="performance">Performance</TabsTrigger>
          <TabsTrigger value="reports">Relatórios</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {overviewStats.map((stat, index) => {
              const Icon = stat.icon
              return (
                <Card key={index} className="hover:shadow-lg transition-shadow">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-slate-600">{stat.title}</p>
                        <p className="text-2xl font-bold text-slate-900">{stat.value}</p>
                        <p className={`text-sm ${stat.change.startsWith('+') ? 'text-green-600' : 'text-red-600'}`}>
                          {stat.change} vs mês anterior
                        </p>
                      </div>
                      <Icon className={`h-8 w-8 ${stat.color}`} />
                    </div>
                  </CardContent>
                </Card>
              )
            })}
          </div>

          {/* Recent Analyses */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Activity className="h-5 w-5" />
                Análises Recentes
              </CardTitle>
              <CardDescription>
                Últimas análises realizadas no sistema
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentAnalyses.map((analysis) => (
                  <div key={analysis.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-slate-50 transition-colors">
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                        <FileText className="h-5 w-5 text-blue-600" />
                      </div>
                      <div>
                        <h4 className="font-medium">{analysis.title}</h4>
                        <p className="text-sm text-slate-600">{analysis.type} • {analysis.date}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      {analysis.confidence && (
                        <Badge variant="outline">{analysis.confidence}% confiança</Badge>
                      )}
                      {getStatusBadge(analysis.status)}
                      <Button variant="ghost" size="sm">
                        <Eye className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Analytics Tab */}
        <TabsContent value="analytics" className="space-y-6">
          <div className="grid lg:grid-cols-2 gap-6">
            {/* Word Frequency Chart */}
            <Card>
              <CardHeader>
                <CardTitle>Frequência de Palavras</CardTitle>
                <CardDescription>
                  Palavras mais comuns relacionadas a "sonho"
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={wordFrequencyData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="word" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="frequency" fill="#3B82F6" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Dream Types Pie Chart */}
            <Card>
              <CardHeader>
                <CardTitle>Tipos de Sonho</CardTitle>
                <CardDescription>
                  Distribuição por categoria
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <RechartsPieChart>
                    <Pie
                      data={dreamTypesData}
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      dataKey="value"
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    >
                      {dreamTypesData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </RechartsPieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* Canto Distribution */}
          <Card>
            <CardHeader>
              <CardTitle>Distribuição por Canto</CardTitle>
              <CardDescription>
                Ocorrências de referências a sonhos em cada canto de Os Lusíadas
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={cantoDistributionData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="canto" />
                  <YAxis />
                  <Tooltip />
                  <Area type="monotone" dataKey="occurrences" stroke="#8B5CF6" fill="#8B5CF6" fillOpacity={0.3} />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Performance Tab */}
        <TabsContent value="performance" className="space-y-6">
          {/* Timeline Chart */}
          <Card>
            <CardHeader>
              <CardTitle>Performance ao Longo do Tempo</CardTitle>
              <CardDescription>
                Número de análises e precisão média por mês
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={analysisTimelineData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis yAxisId="left" />
                  <YAxis yAxisId="right" orientation="right" />
                  <Tooltip />
                  <Bar yAxisId="left" dataKey="analyses" fill="#3B82F6" />
                  <Line yAxisId="right" type="monotone" dataKey="accuracy" stroke="#10B981" strokeWidth={3} />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Performance Metrics */}
          <div className="grid md:grid-cols-3 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Tempo Médio de Processamento</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-blue-600">2.3s</div>
                <p className="text-sm text-slate-600 mt-2">
                  <span className="text-green-600">↓ 15%</span> vs mês anterior
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Taxa de Sucesso</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-green-600">96.2%</div>
                <p className="text-sm text-slate-600 mt-2">
                  <span className="text-green-600">↑ 2.1%</span> vs mês anterior
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Confiança Média</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-purple-600">94.1%</div>
                <p className="text-sm text-slate-600 mt-2">
                  <span className="text-green-600">↑ 1.8%</span> vs mês anterior
                </p>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Reports Tab */}
        <TabsContent value="reports" className="space-y-6">
          <div className="grid md:grid-cols-2 gap-6">
            {/* Export Options */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Download className="h-5 w-5" />
                  Exportar Relatórios
                </CardTitle>
                <CardDescription>
                  Baixe relatórios detalhados em diferentes formatos
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <Button className="w-full justify-start" variant="outline">
                  <FileText className="mr-2 h-4 w-4" />
                  Relatório Completo (PDF)
                </Button>
                <Button className="w-full justify-start" variant="outline">
                  <BarChart3 className="mr-2 h-4 w-4" />
                  Dados de Análise (CSV)
                </Button>
                <Button className="w-full justify-start" variant="outline">
                  <PieChart className="mr-2 h-4 w-4" />
                  Visualizações (PNG)
                </Button>
                <Button className="w-full justify-start" variant="outline">
                  <Sparkles className="mr-2 h-4 w-4" />
                  Dashboard Interativo (HTML)
                </Button>
              </CardContent>
            </Card>

            {/* Report Summary */}
            <Card>
              <CardHeader>
                <CardTitle>Resumo do Último Relatório</CardTitle>
                <CardDescription>
                  Gerado em 15 de junho de 2024
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm text-slate-600">Total de Análises</span>
                    <span className="font-medium">1,247</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-slate-600">Textos Únicos</span>
                    <span className="font-medium">342</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-slate-600">Palavras Processadas</span>
                    <span className="font-medium">2.1M</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-slate-600">Precisão Média</span>
                    <span className="font-medium">94.1%</span>
                  </div>
                </div>
                
                <Button className="w-full">
                  <Eye className="mr-2 h-4 w-4" />
                  Visualizar Relatório
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Scheduled Reports */}
          <Card>
            <CardHeader>
              <CardTitle>Relatórios Agendados</CardTitle>
              <CardDescription>
                Configure relatórios automáticos
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8">
                <Clock className="h-16 w-16 text-slate-400 mx-auto mb-4" />
                <p className="text-slate-600 mb-4">
                  Nenhum relatório agendado configurado
                </p>
                <Button>
                  Configurar Relatório Automático
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default DashboardPage
