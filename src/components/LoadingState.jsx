import { useTranslation } from 'react-i18next'
import { Shield } from 'lucide-react'

export default function LoadingState({ fileName, fileType }) {
  const { t } = useTranslation()
  const steps = [t('loading.step1'), t('loading.step2'), t('loading.step3'), t('loading.step4')]

  return (
    <div className="text-center space-y-6 py-10 fade-in-up">
      <div className="flex justify-center">
        <div className="w-20 h-20 rounded-2xl flex items-center justify-center shield-anim"
          style={{ background: 'linear-gradient(135deg, rgba(37,99,235,0.12), rgba(37,99,235,0.06))', border: '2px solid var(--color-border)' }}>
          <Shield size={38} style={{ color: 'var(--color-primary)' }} />
        </div>
      </div>

      <div>
        <h2 className="text-xl font-bold mb-1" style={{ color: 'var(--color-text)' }}>
          {t('loading.title')}
        </h2>
        <p className="text-sm font-medium" style={{ color: 'var(--color-text-muted)' }}>{fileName}</p>
      </div>

      <div className="space-y-3 text-left max-w-xs mx-auto">
        {steps.map((step, i) => (
          <div key={i} className="flex items-center gap-3 text-sm">
            <div className="w-5 h-5 rounded-full border-2 flex-shrink-0 animate-spin"
              style={{ borderColor: 'var(--color-primary)', borderTopColor: 'transparent', animationDelay: `${i * 0.25}s` }} />
            <span className="font-medium" style={{ color: 'var(--color-text)' }}>{step}</span>
          </div>
        ))}
      </div>

      {fileType === 'video' && (
        <p className="text-xs font-medium px-4 py-2 rounded-lg inline-block"
          style={{ backgroundColor: 'var(--color-surface2)', color: 'var(--color-text-muted)', border: '1px solid var(--color-border)' }}>
          {t('loading.video_note')}
        </p>
      )}
    </div>
  )
}
