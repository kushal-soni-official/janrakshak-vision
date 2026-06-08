import { useTranslation } from 'react-i18next'
import { useTheme } from '../contexts/ThemeContext'
import { Sun, Moon } from 'lucide-react'

const SWATCHES = [
  { id: 'default', color: '#2563EB', label: 'Blue'   },
  { id: 'saffron', color: '#EA580C', label: 'Saffron'},
  { id: 'forest',  color: '#16A34A', label: 'Forest' },
  { id: 'ocean',   color: '#0891B2', label: 'Ocean'  },
  { id: 'rose',    color: '#E11D48', label: 'Rose'   },
  { id: 'violet',  color: '#7C3AED', label: 'Violet' },
  { id: 'amber',   color: '#D97706', label: 'Amber'  },
]

export default function ThemePicker() {
  const { t } = useTranslation()
  const { theme, setTheme, mode, toggleMode, customColor, setCustomColor } = useTheme()

  return (
    <div className="space-y-3">
      {/* Appearance — Dark / Light */}
      <div>
        <p className="text-xs font-bold mb-2 uppercase tracking-wide" style={{ color: 'var(--color-text-muted)' }}>
          {t('navbar.appearance')}
        </p>
        <div className="flex gap-2">
          <button
            onClick={() => mode === 'dark' && toggleMode()}
            className="flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-semibold transition-all"
            style={{
              backgroundColor: mode === 'light' ? 'var(--color-primary)' : 'var(--color-surface2)',
              color: mode === 'light' ? 'white' : 'var(--color-text)',
              border: mode === 'light' ? '1.5px solid var(--color-primary)' : '1px solid var(--color-border)',
            }}
          >
            <Sun size={13} /> {t('navbar.light')}
          </button>
          <button
            onClick={() => mode === 'light' && toggleMode()}
            className="flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-semibold transition-all"
            style={{
              backgroundColor: mode === 'dark' ? 'var(--color-primary)' : 'var(--color-surface2)',
              color: mode === 'dark' ? 'white' : 'var(--color-text)',
              border: mode === 'dark' ? '1.5px solid var(--color-primary)' : '1px solid var(--color-border)',
            }}
          >
            <Moon size={13} /> {t('navbar.dark')}
          </button>
        </div>
      </div>

      {/* Color Theme */}
      <div>
        <p className="text-xs font-bold mb-2 uppercase tracking-wide" style={{ color: 'var(--color-text-muted)' }}>
          {t('navbar.theme')}
        </p>
        <div className="flex items-center gap-2 flex-wrap">
          {SWATCHES.map(s => (
            <button key={s.id} onClick={() => setTheme(s.id)} title={s.label}
              className="w-7 h-7 rounded-full transition-transform hover:scale-110 active:scale-95"
              style={{
                backgroundColor: s.color,
                outline: theme === s.id ? `3px solid ${s.color}` : '3px solid transparent',
                outlineOffset: '2px',
                boxShadow: theme === s.id ? `0 0 8px ${s.color}70` : 'none',
              }}
            />
          ))}

          {/* Custom color */}
          <div className="flex items-center gap-1.5 ml-1">
            <span className="text-xs font-medium" style={{ color: 'var(--color-text-muted)' }}>
              {t('navbar.custom_color')}:
            </span>
            <div className="relative w-7 h-7">
              <input type="color" value={customColor}
                onChange={(e) => setCustomColor(e.target.value)}
                className="absolute inset-0 w-full h-full rounded-full cursor-pointer opacity-0" />
              <div className="w-7 h-7 rounded-full border-2 pointer-events-none flex items-center justify-center"
                style={{
                  backgroundColor: customColor,
                  borderColor: theme === 'custom' ? customColor : 'var(--color-border)',
                  outline: theme === 'custom' ? `3px solid ${customColor}` : '3px solid transparent',
                  outlineOffset: '2px',
                }}>
                <span className="text-white text-xs font-bold leading-none select-none">+</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
