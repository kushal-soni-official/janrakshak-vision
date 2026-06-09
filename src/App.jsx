import { useState } from 'react'
import { Toaster } from 'react-hot-toast'
import { ThemeProvider } from './contexts/ThemeContext'
import Navbar from './components/Navbar'
import UploadZone from './components/UploadZone'
import ResultCard from './components/ResultCard'
import LoadingState from './components/LoadingState'
import TeamModal from './components/TeamModal'
import { analyzeFile } from './utils/api'
import { useTranslation } from 'react-i18next'
import toast from 'react-hot-toast'

function AppContent() {
  const { t } = useTranslation()
  const [stage, setStage] = useState('upload')
  const [result, setResult] = useState(null)
  const [fileName, setFileName] = useState('')
  const [fileType, setFileType] = useState('image')
  const [history, setHistory] = useState([])
  const [showTeam, setShowTeam] = useState(false)

  const handleFileUpload = async (file) => {
    if (!file) return
    setFileName(file.name)
    setFileType(file.type.startsWith('video/') ? 'video' : 'image')
    setStage('loading')
    try {
      const data = await analyzeFile(file)
      setResult(data)
      setHistory(prev => [...prev, { name: file.name, verdict: data.verdict }])
      setStage('result')
    } catch (err) {
      console.error(err)
      if (err.message === 'Request timed out') {
        toast.error(t('errors.timeout'))
      } else if (err.message?.includes('fetch') || err.message?.includes('network')) {
        toast.error(t('errors.network'))
      } else {
        toast.error(err.message || t('errors.failed'))
      }
      setStage('upload')
    }
  }

  const handleReset = () => { setStage('upload'); setResult(null); setFileName('') }

  return (
    <div className="min-h-screen flex flex-col" style={{ backgroundColor: 'var(--color-bg)' }}>
      <Toaster
        position="top-center"
        toastOptions={{
          duration: 4000,
          style: {
            background: 'var(--color-surface)',
            color: 'var(--color-text)',
            border: '1px solid var(--color-border)',
            fontSize: '0.875rem',
          },
        }}
      />

      <Navbar analysisHistory={history} />

      <main className="flex-1 max-w-xl mx-auto w-full px-4 py-6 pb-4">
        {stage === 'upload'  && <UploadZone onFileSelected={handleFileUpload} />}
        {stage === 'loading' && <LoadingState fileName={fileName} fileType={fileType} />}
        {stage === 'result'  && result && (
          <ResultCard result={result} fileName={fileName} onReset={handleReset} />
        )}
      </main>

      {/* Footer */}
      <footer
        className="border-t text-center py-2.5 px-4"
        style={{ backgroundColor: 'var(--color-surface)', borderColor: 'var(--color-border)' }}
      >
        <p className="text-xs" style={{ color: 'var(--color-text-muted)' }}>
          🛡️{' '}
          <strong style={{ color: 'var(--color-text)' }}>JanRakshak Vision</strong>
          {' · '}
          {t('footer.tagline')}
          {' · Built by '}
          <button
            onClick={() => setShowTeam(true)}
            className="font-semibold underline-offset-2 hover:underline transition-colors"
            style={{ color: 'var(--color-primary)', background: 'none', border: 'none', cursor: 'pointer', padding: 0, fontSize: 'inherit' }}
          >
            {t('footer.team')}
          </button>
          {' · '}
          {t('footer.event')}
        </p>
      </footer>

      {/* Team Modal */}
      {showTeam && <TeamModal onClose={() => setShowTeam(false)} />}
    </div>
  )
}

export default function App() {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  )
}
