import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Shield, Settings, X, Sun, Moon } from 'lucide-react'
import { useTheme } from '../contexts/ThemeContext'
import LanguageSwitcher from './LanguageSwitcher'
import ThemePicker from './ThemePicker'
import AdvancedPanel from './AdvancedPanel'

export default function Navbar({ analysisHistory = [] }) {
  const { t } = useTranslation()
  const { mode, toggleMode } = useTheme()
  const [open, setOpen] = useState(false)

  return (
    <nav className="sticky top-0 z-50 border-b"
      style={{ backgroundColor: 'var(--color-surface)', borderColor: 'var(--color-border)', boxShadow: 'var(--shadow-sm)' }}>
      <div className="max-w-xl mx-auto px-4 h-14 flex items-center justify-between">

        {/* Brand */}
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg flex items-center justify-center"
            style={{ background: 'linear-gradient(135deg, var(--color-primary), var(--color-primary-dark))' }}>
            <Shield size={17} color="white" />
          </div>
          <div>
            <span className="font-bold text-sm leading-none" style={{ color: 'var(--color-text)' }}>
              JanRakshak Vision
            </span>
            <p className="text-xs leading-none mt-0.5" style={{ color: 'var(--color-text-muted)' }}>
              by Anonymous Group
            </p>
          </div>
        </div>

        {/* Right actions */}
        <div className="flex items-center gap-1">
          {/* Dark/Light toggle — always visible */}
          <button
            onClick={toggleMode}
            title={mode === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
            className="p-2 rounded-lg transition-colors"
            style={{ color: 'var(--color-text-muted)', backgroundColor: 'transparent' }}
            aria-label="Toggle dark/light mode"
          >
            {mode === 'dark' ? <Sun size={19} /> : <Moon size={19} />}
          </button>

          {/* Settings toggle */}
          <button
            onClick={() => setOpen(!open)}
            className="p-2 rounded-lg transition-colors"
            style={{
              backgroundColor: open ? 'var(--color-primary)' : 'transparent',
              color: open ? 'white' : 'var(--color-text-muted)',
            }}
            aria-label={t('navbar.settings')}
          >
            {open ? <X size={19} /> : <Settings size={19} />}
          </button>
        </div>
      </div>

      {/* Settings Panel */}
      {open && (
        <div className="border-t max-w-xl mx-auto px-4 py-4 space-y-5 fade-in-up"
          style={{ borderColor: 'var(--color-border)' }}>
          <LanguageSwitcher />
          <ThemePicker />
          <AdvancedPanel history={analysisHistory} />
        </div>
      )}
    </nav>
  )
}
