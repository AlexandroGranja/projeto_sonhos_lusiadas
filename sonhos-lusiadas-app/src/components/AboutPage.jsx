import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { 
  BookOpen, 
  Brain, 
  Code, 
  Users, 
  Target,
  Lightbulb,
  Cpu,
  Database,
  Globe,
  Github,
  Mail,
  ExternalLink,
  Sparkles,
  Award,
  Zap
} from 'lucide-react'

const AboutPage = () => {
  const technologies = [
    { name: 'Claude Sonnet 4', description: 'IA para análise literária avançada', icon: Brain },
    { name: 'React', description: 'Interface de usuário moderna', icon: Code },
    { name: 'Flask', description: 'Backend robusto e escalável', icon: Database },
    { name: 'spaCy', description: 'Processamento de linguagem natural', icon: Cpu },
    { name: 'BERTimbau', description: 'Modelo de linguagem em português', icon: Zap },
    { name: 'Plotly', description: 'Visualizações interativas', icon: Globe }
  ]

  const features = [
    {
      title: 'Análise Quantitativa',
      description: 'Frequência, contexto e distribuição de palavras relacionadas ao tema "sonho"',
      icon: Target
    },
    {
      title: 'Análise Qualitativa',
      description: 'Função narrativa, simbolismo e intertextualidade com a tradição clássica',
      icon: BookOpen
    },
    {
      title: 'Expansão Semântica',
      description: 'Identificação automática de palavras relacionadas usando IA',
      icon: Brain
    },
    {
      title: 'Classificação Inteligente',
      description: 'Categorização de contextos em onírico, profético, alegórico e outros',
      icon: Lightbulb
    }
  ]

  const methodology = [
    {
      step: '1',
      title: 'Pré-processamento',
      description: 'Limpeza, tokenização e lematização do texto usando spaCy e NLTK'
    },
    {
      step: '2',
      title: 'Expansão Semântica',
      description: 'Ampliação do vocabulário com FastText, BERTimbau e Claude Sonnet 4'
    },
    {
      step: '3',
      title: 'Busca e Análise',
      description: 'Localização de ocorrências e extração de contextos relevantes'
    },
    {
      step: '4',
      title: 'Visualização',
      description: 'Geração de gráficos, nuvens de palavras e dashboards interativos'
    }
  ]

  return (
    <div className="max-w-6xl mx-auto space-y-12">
      {/* Header */}
      <div className="text-center space-y-6">
        <div className="flex justify-center">
          <div className="relative">
            <BookOpen className="h-16 w-16 text-blue-600" />
            <Sparkles className="h-8 w-8 text-amber-500 absolute -top-2 -right-2 animate-pulse" />
          </div>
        </div>
        <h1 className="text-4xl font-bold text-slate-800">
          Sobre o Projeto Sonhos Lusíadas
        </h1>
        <p className="text-xl text-slate-600 max-w-3xl mx-auto leading-relaxed">
          Uma ferramenta inovadora que combina inteligência artificial e análise literária 
          para explorar o tema "sonho" em Os Lusíadas de Luís de Camões
        </p>
      </div>

      {/* Project Overview */}
      <Card className="bg-gradient-to-r from-blue-50 to-purple-50 border-0">
        <CardHeader>
          <CardTitle className="text-2xl flex items-center gap-2">
            <Target className="h-6 w-6 text-blue-600" />
            Objetivo do Projeto
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-lg text-slate-700 leading-relaxed">
            Este projeto busca analisar a presença e o significado do tema "sonho" em Os Lusíadas 
            de Luís de Camões, combinando análise quantitativa através de técnicas de Processamento 
            de Linguagem Natural (NLP) com análise qualitativa literária.
          </p>
          <p className="text-slate-600">
            O sonho em Os Lusíadas funciona como dispositivo poético, profético e psicológico, 
            conectando o épico camoniano à tradição clássica e à cultura renascentista. 
            Nossa ferramenta mapeia e interpreta essas ocorrências de forma sistemática e inovadora.
          </p>
        </CardContent>
      </Card>

      {/* Features */}
      <section className="space-y-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-slate-800 mb-4">Funcionalidades Principais</h2>
          <p className="text-lg text-slate-600">
            Recursos avançados para análise literária profunda
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon
            return (
              <Card key={index} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <CardTitle className="flex items-center gap-3">
                    <div className="p-2 bg-blue-100 rounded-lg">
                      <Icon className="h-5 w-5 text-blue-600" />
                    </div>
                    {feature.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-slate-600">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            )
          })}
        </div>
      </section>

      {/* Methodology */}
      <section className="space-y-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-slate-800 mb-4">Metodologia</h2>
          <p className="text-lg text-slate-600">
            Processo estruturado em quatro etapas principais
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {methodology.map((item, index) => (
            <Card key={index} className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="mx-auto w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center text-xl font-bold mb-4">
                  {item.step}
                </div>
                <CardTitle className="text-lg">{item.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-slate-600">
                  {item.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* Technologies */}
      <section className="space-y-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-slate-800 mb-4">Tecnologias Utilizadas</h2>
          <p className="text-lg text-slate-600">
            Stack moderno e ferramentas de ponta para análise literária
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {technologies.map((tech, index) => {
            const Icon = tech.icon
            return (
              <Card key={index} className="hover:shadow-lg transition-shadow">
                <CardContent className="p-6 text-center">
                  <Icon className="h-12 w-12 text-blue-600 mx-auto mb-4" />
                  <h3 className="font-semibold text-lg mb-2">{tech.name}</h3>
                  <p className="text-sm text-slate-600">{tech.description}</p>
                </CardContent>
              </Card>
            )
          })}
        </div>
      </section>

      {/* Research Questions */}
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl flex items-center gap-2">
            <Lightbulb className="h-6 w-6 text-amber-600" />
            Perguntas de Pesquisa
          </CardTitle>
          <CardDescription>
            Questões centrais que orientam nossa análise
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-3">
              <h4 className="font-semibold text-slate-800">Análise Quantitativa</h4>
              <ul className="space-y-2 text-slate-600">
                <li>• Quais personagens estão mais associados a sonhos?</li>
                <li>• Há padrões de sonho por canto?</li>
                <li>• Qual a frequência de diferentes tipos de sonho?</li>
              </ul>
            </div>
            <div className="space-y-3">
              <h4 className="font-semibold text-slate-800">Análise Qualitativa</h4>
              <ul className="space-y-2 text-slate-600">
                <li>• Como o sonho funciona como recurso narrativo?</li>
                <li>• Como Camões dialoga com a tradição clássica?</li>
                <li>• Qual o simbolismo dos diferentes tipos de sonho?</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Results Expected */}
      <Card className="bg-gradient-to-r from-green-50 to-blue-50 border-0">
        <CardHeader>
          <CardTitle className="text-2xl flex items-center gap-2">
            <Award className="h-6 w-6 text-green-600" />
            Resultados Esperados
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-3">
              <h4 className="font-semibold text-slate-800">Outputs Quantitativos</h4>
              <ul className="space-y-2 text-slate-600">
                <li>• Tabela de frequências por canto e tipo de sonho</li>
                <li>• Nuvem de palavras com termos mais recorrentes</li>
                <li>• Gráficos de distribuição por canto</li>
                <li>• Lista de trechos classificados</li>
              </ul>
            </div>
            <div className="space-y-3">
              <h4 className="font-semibold text-slate-800">Outputs Qualitativos</h4>
              <ul className="space-y-2 text-slate-600">
                <li>• Relatório literário com interpretações</li>
                <li>• Análise de intertextualidade</li>
                <li>• Mapeamento de funções narrativas</li>
                <li>• Insights sobre simbolismo</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Technical Specifications */}
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl flex items-center gap-2">
            <Code className="h-6 w-6 text-purple-600" />
            Especificações Técnicas
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="space-y-3">
              <h4 className="font-semibold text-slate-800">Frontend</h4>
              <div className="space-y-2">
                <Badge variant="outline">React 18</Badge>
                <Badge variant="outline">Tailwind CSS</Badge>
                <Badge variant="outline">Shadcn/ui</Badge>
                <Badge variant="outline">Recharts</Badge>
              </div>
            </div>
            <div className="space-y-3">
              <h4 className="font-semibold text-slate-800">Backend</h4>
              <div className="space-y-2">
                <Badge variant="outline">Flask</Badge>
                <Badge variant="outline">Python 3.11</Badge>
                <Badge variant="outline">SQLite</Badge>
                <Badge variant="outline">Flask-CORS</Badge>
              </div>
            </div>
            <div className="space-y-3">
              <h4 className="font-semibold text-slate-800">IA & NLP</h4>
              <div className="space-y-2">
                <Badge variant="outline">Claude Sonnet 4</Badge>
                <Badge variant="outline">spaCy</Badge>
                <Badge variant="outline">BERTimbau</Badge>
                <Badge variant="outline">NLTK</Badge>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Contact & Links */}
      <Card className="bg-slate-50 border-0">
        <CardHeader>
          <CardTitle className="text-2xl flex items-center gap-2">
            <Users className="h-6 w-6 text-slate-600" />
            Contato e Recursos
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <h4 className="font-semibold text-slate-800">Desenvolvido por</h4>
              <p className="text-slate-600">
                Sistema de Análise Literária com IA<br />
                Baseado no projeto "Sonho em Os Lusíadas"
              </p>
              <div className="flex gap-3">
                <Button variant="outline" size="sm">
                  <Github className="mr-2 h-4 w-4" />
                  Código Fonte
                </Button>
                <Button variant="outline" size="sm">
                  <Mail className="mr-2 h-4 w-4" />
                  Contato
                </Button>
              </div>
            </div>
            <div className="space-y-4">
              <h4 className="font-semibold text-slate-800">Recursos Adicionais</h4>
              <div className="space-y-2">
                <Button variant="ghost" className="justify-start p-0 h-auto">
                  <ExternalLink className="mr-2 h-4 w-4" />
                  Documentação Técnica
                </Button>
                <Button variant="ghost" className="justify-start p-0 h-auto">
                  <ExternalLink className="mr-2 h-4 w-4" />
                  Manual do Usuário
                </Button>
                <Button variant="ghost" className="justify-start p-0 h-auto">
                  <ExternalLink className="mr-2 h-4 w-4" />
                  Projeto Gutenberg - Os Lusíadas
                </Button>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default AboutPage
