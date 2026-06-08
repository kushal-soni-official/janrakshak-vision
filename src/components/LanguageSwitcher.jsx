import { useTranslation } from 'react-i18next'

const LANGS = [
  { code: 'en', label: 'English' },
  { code: 'hi', label: 'हिंदी' },
  { code: 'bn', label: 'বাংলা' },
]

export default function LanguageSwitcher() {
  const { i18n, t } = useTranslation()
  const current = i18n.language

  const change = (code) => {
    i18n.changeLanguage(code)
    localStorage.setItem('jr_lang', code)
  }

  return (
    <div>
      <p className="text-xs font-medium mb-2" style={{ color: 'var(--color-text-muted)' }}>
        {t('navbar.language')}
      </p>
      <div className="flex gap-2">
        {LANGS.map(lang => (
          <button
            key={lang.code}
            onClick={() => change(lang.code)}
            className="px-3 py-1.5 rounded-lg text-sm font-medium transition-all"
            style={{
              backgroundColor: current === lang.code ? 'var(--color-primary)' : 'var(--color-surface2)',
              color: current === lang.code ? 'white' : 'var(--color-text)',
              border: '1px solid var(--color-border)',
            }}
          >
            {lang.label}
          </button>
        ))}
      </div>
    </div>
  )
}
