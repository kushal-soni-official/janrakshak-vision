import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { ChevronDown, ChevronUp, Clock } from 'lucide-react'

export default function AdvancedPanel({ history = [] }) {
  const { t } = useTranslation()
  const [open, setOpen] = useState(false)
  return (
    <div>
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-1.5 text-xs font-medium transition-opacity hover:opacity-75"
        style={{ color: 'var(--color-text-muted)', background: 'none', border: 'none', cursor: 'pointer', padding: 0 }}
      >
        {open ? <ChevronUp size={13} /> : <ChevronDown size={13} />}
        {open ? t('advanced.hide') : t('advanced.show')}
        <span className="px-1.5 py-0.5 rounded text-xs font-medium"
          style={{ backgroundColor: 'var(--color-surface2)', border: '1px solid var(--color-border)', color: 'var(--color-text-muted)' }}>
          {t('navbar.advanced_hint')}
        </span>
      </button>

      {open && (
        <div className="mt-3 space-y-4 p-4 rounded-xl fade-in-up"
          style={{ backgroundColor: 'var(--color-surface2)', border: '1px solid var(--color-border)' }}>

          {/* Session History */}
          <div>
            <p className="text-xs font-bold mb-2 flex items-center gap-1.5" style={{ color: 'var(--color-text)' }}>
              <Clock size={12} style={{ color: 'var(--color-primary)' }} />
              {t('advanced.history')}
            </p>
            {history.length === 0 ? (
              <p className="text-xs italic font-medium" style={{ color: 'var(--color-text-muted)' }}>
                {t('advanced.no_history')}
              </p>
            ) : (
              <div className="space-y-1 max-h-32 overflow-y-auto">
                {[...history].reverse().slice(0, 8).map((item, i) => (
                  <div key={i} className="flex justify-between items-center text-xs py-1.5 px-2.5 rounded-lg"
                    style={{ backgroundColor: 'var(--color-surface)', border: '1px solid var(--color-border)' }}>
                    <span className="truncate max-w-[140px] font-medium" style={{ color: 'var(--color-text)' }} title={item.name}>
                      {item.name}
                    </span>
                    <span className="font-bold ml-2 shrink-0" style={{
                      color: item.verdict === 'FAKE' ? 'var(--color-danger)'
                           : item.verdict === 'SUSPICIOUS' ? 'var(--color-warning)'
                           : 'var(--color-success)'
                    }}>{item.verdict}</span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* About */}
          <div className="pt-2 border-t space-y-1" style={{ borderColor: 'var(--color-border)' }}>
            {[
              [t('advanced.about_model'),  '3-Brain Ensemble (v7)'],
              [t('advanced.about_team'),   'Anonymous Group'],
              [t('advanced.about_leader'), 'Kushal Soni'],
              [t('advanced.about_event'),  'Tradition Hacks 2026'],
            ].map(([label, value]) => (
              <div key={label} className="flex justify-between text-xs">
                <span style={{ color: 'var(--color-text-muted)' }}>{label}</span>
                <span className="font-semibold" style={{ color: 'var(--color-text)' }}>{value}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
