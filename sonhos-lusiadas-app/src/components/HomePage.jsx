import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { 
  Brain, 
  FileText, 
  BarChart3, 
  Sparkles, 
  BookOpen,
  Upload,
  Search,
  TrendingUp,
  ArrowRight,
  CheckCircle
} from 'lucide-react'

const HomePage = () => {
  const features = [
    {
      icon: Brain,
      title: 'Análise com IA',
      description: 'Processamento de linguagem natural avançado com Claude Sonnet 4 para análise literária profunda.',
      color: 'text-blue-600'
    },
    {
      icon: FileText,
      title: 'Múltiplos Formatos',
      description: 'Suporte para arquivos .txt, .docx e .pdf. Analise qualquer texto literário.',
      color: 'text-green-600'
    },
    {
      icon: BarChart3,
      title: 'Visualizações Interativas',
      description: 'Gráficos, nuvens de palavras e dashboards para explorar os dados de forma visual.',
      color: 'text-purple-600'
    },
    {
      icon: Search,
      title: 'Busca Semântica',
      description: 'Expansão semântica inteligente para encontrar padrões e conexões ocultas no texto.',
      color: 'text-amber-600'
    }
  ]

  const steps = [
    {
      icon: Upload,
      title: 'Envie seu Texto',
      description: 'Faça upload do arquivo ou cole o texto diretamente'
    },
    {
      icon: Brain,
      title: 'Processamento IA',
      description: 'Nossa IA analisa o conteúdo usando técnicas avançadas de NLP'
    },
    {
      icon: TrendingUp,
      title: 'Visualize Resultados',
      description: 'Explore insights através de gráficos e relatórios detalhados'
    }
  ]

  const benefits = [
    'Análise quantitativa e qualitativa combinadas',
    'Identificação de padrões temáticos',
    'Classificação automática de contextos',
    'Relatórios detalhados em múltiplos formatos',
    'Interface intuitiva e moderna',
    'Processamento rápido e eficiente'
  ]

  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="text-center space-y-8 py-12">
        <div className="space-y-4">
          <div className="flex justify-center">
            <div className="relative animate-bounce">
              <BookOpen className="h-16 w-16 text-blue-600" />
              <Sparkles className="h-8 w-8 text-amber-500 absolute -top-2 -right-2 animate-pulse" />
            </div>
          </div>
          <h1 className="text-3xl sm:text-4xl md:text-6xl font-bold text-slate-800 leading-tight">
            Sonhos em <span className="text-blue-600 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">Os Lusíadas</span>
          </h1>
          <p className="text-lg sm:text-xl text-slate-600 max-w-3xl mx-auto leading-relaxed px-4">
            Uma ferramenta revolucionária para análise literária que combina inteligência artificial 
            avançada com técnicas de processamento de linguagem natural para explorar temas e 
            padrões em textos clássicos.
          </p>
        </div>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Link to="/analysis">
            <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 text-lg">
              Começar Análise
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </Link>
          <Link to="/about">
            <Button variant="outline" size="lg" className="px-8 py-3 text-lg">
              Saiba Mais
            </Button>
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section className="space-y-8">
        <div className="text-center space-y-4">
          <h2 className="text-3xl font-bold text-slate-800">Recursos Principais</h2>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Tecnologia de ponta para análise literária profunda e insights únicos
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon
            return (
              <Card 
                key={index} 
                className="group hover:shadow-lg transition-all duration-300 border-0 bg-white/60 backdrop-blur-sm animate-fade-in-up"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <CardHeader className="text-center">
                  <div className="mx-auto mb-4 p-3 rounded-full bg-slate-50 group-hover:bg-slate-100 transition-colors">
                    <Icon className={`h-8 w-8 ${feature.color}`} />
                  </div>
                  <CardTitle className="text-lg">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-center text-slate-600">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            )
          })}
        </div>
      </section>

      {/* How it Works Section */}
      <section className="space-y-8">
        <div className="text-center space-y-4">
          <h2 className="text-3xl font-bold text-slate-800">Como Funciona</h2>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Processo simples e intuitivo para análise literária avançada
          </p>
        </div>
        
        <div className="grid md:grid-cols-3 gap-8">
          {steps.map((step, index) => {
            const Icon = step.icon
            return (
              <div key={index} className="text-center space-y-4">
                <div className="relative">
                  <div className="mx-auto w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center">
                    <Icon className="h-8 w-8 text-blue-600" />
                  </div>
                  <div className="absolute -top-2 -right-2 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                    {index + 1}
                  </div>
                </div>
                <h3 className="text-xl font-semibold text-slate-800">{step.title}</h3>
                <p className="text-slate-600">{step.description}</p>
              </div>
            )
          })}
        </div>
      </section>

      {/* Benefits Section */}
      <section className="bg-white/60 backdrop-blur-sm rounded-2xl p-8 space-y-8">
        <div className="text-center space-y-4">
          <h2 className="text-3xl font-bold text-slate-800">Por que Escolher Nossa Ferramenta?</h2>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Benefícios únicos para pesquisadores, estudantes e entusiastas da literatura
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 gap-6">
          {benefits.map((benefit, index) => (
            <div key={index} className="flex items-center space-x-3">
              <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0" />
              <span className="text-slate-700">{benefit}</span>
            </div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="text-center space-y-8 py-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl text-white">
        <div className="space-y-4">
          <h2 className="text-3xl font-bold">Pronto para Começar?</h2>
          <p className="text-xl opacity-90 max-w-2xl mx-auto">
            Descubra insights únicos em textos literários com nossa ferramenta de análise avançada
          </p>
        </div>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Link to="/analysis">
            <Button size="lg" variant="secondary" className="px-8 py-3 text-lg">
              Iniciar Análise Gratuita
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </Link>
          <Link to="/dashboard">
            <Button size="lg" variant="outline" className="px-8 py-3 text-lg border-white text-white hover:bg-white hover:text-blue-600">
              Ver Dashboard
            </Button>
          </Link>
        </div>
      </section>
    </div>
  )
}

export default HomePage
