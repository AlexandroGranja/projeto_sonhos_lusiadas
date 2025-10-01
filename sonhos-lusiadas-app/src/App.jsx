import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from '@/components/ui/toaster'
import SimpleAnalysis from '@/components/SimpleAnalysis'
import './App.css'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<SimpleAnalysis />} />
            <Route path="*" element={<SimpleAnalysis />} />
          </Routes>
        </main>
        <Toaster />
      </div>
    </Router>
  )
}

export default App
