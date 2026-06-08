import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { ChevronDown, ChevronUp, Clock, SlidersHorizontal, Info } from 'lucide-react'

export default function AdvancedPanel({ history = [] }) {
  const { t } = useTranslation()
  const [open, setOpen] = useState(false)
  const [sensitivity, setSensitivity] = useState('medium')

  const SENS = [
    { value: 'low',    label: t('advanced.sens_low'),  desc: t('advanced.sens_low_desc')  },
    { value: 'medium', label: t('advanced.sens_med'),  desc: t('advanced.sens_med_desc')  },
    { value: 'high',   label: t('advanced.sens_high'), desc: t('advanced.sens_high_desc') },
  ]

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

          {/* Sensitivity */}
          <div>
            <p className="text-xs font-bold mb-2 flex items-center gap-1.5" style={{ color: 'var(--color-text)' }}>
              <SlidersHorizontal size={12} style={{ color: 'var(--color-primary)' }} />
              {t('advanced.sensitivity')}
            </p>
            <div className="flex gap-2">
              {SENS.map(s => (
                <button key={s.value} onClick={() => setSensitivity(s.value)} title={s.desc}
                  className="flex-1 py-1.5 rounded-lg text-xs font-semibold transition-all"
                  style={{
                    backgroundColor: sensitivity === s.value ? 'var(--color-primary)' : 'var(--color-surface)',
                    color: sensitivity === s.value ? 'white' : 'var(--color-text)',
                    border: sensitivity === s.value ? '1.5px solid var(--color-primary)' : '1px solid var(--color-border)',
                  }}>
                  {s.label}
                </button>
              ))}
            </div>
            <p className="text-xs mt-1.5 font-medium" style={{ color: 'var(--color-text-muted)' }}>
              {SENS.find(s => s.value === sensitivity)?.desc}
            </p>
          </div>

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
              [t('advanced.about_model'),  'EfficientNet (dima806)'],
              [t('advanced.about_team'),   'Anonymous Group'],
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
