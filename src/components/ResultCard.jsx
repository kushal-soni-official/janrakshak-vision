import { useTranslation } from 'react-i18next'
import { CheckCircle, AlertTriangle, XCircle, RotateCcw, ExternalLink, Share2 } from 'lucide-react'
import toast from 'react-hot-toast'

const VERDICT_MAP = {
  REAL:       { Icon: CheckCircle,    colorVar: 'var(--color-success)', bgVar: 'var(--color-success-bg)' },
  SUSPICIOUS: { Icon: AlertTriangle,  colorVar: 'var(--color-warning)', bgVar: 'var(--color-warning-bg)' },
  FAKE:       { Icon: XCircle,        colorVar: 'var(--color-danger)',  bgVar: 'var(--color-danger-bg)'  },
}

export default function ResultCard({ result, fileName, onReset }) {
  const { t, i18n } = useTranslation()
  const cfg = VERDICT_MAP[result.verdict] || VERDICT_MAP.SUSPICIOUS
  const { Icon } = cfg
  const explanation = result.explanation?.[i18n.language.split('-')[0]] || result.explanation?.en || ''
  const nextKey = `result.next_${result.verdict.toLowerCase()}`

  const handleShare = () => {
    const text = `🛡️ JanRakshak Vision Result:\n${t(`verdict.${result.verdict}`)}\nConfidence: ${result.confidence}%\n\nCheck your media: https://janrakshak-frontend.vercel.app`
    const isMobile = /Android|iPhone|iPad/i.test(navigator.userAgent)
    if (isMobile && navigator.share) {
      navigator.share({ title: 'JanRakshak Vision', text }).catch(() => copyToClipboard(text))
    } else {
      copyToClipboard(text)
    }
  }

  const copyToClipboard = (text) => {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text)
        .then(() => toast.success(t('result.copied')))
        .catch(() => legacyCopy(text))
    } else {
      legacyCopy(text)
    }
  }

  const legacyCopy = (text) => {
    const ta = document.createElement('textarea')
    ta.value = text
    ta.style.position = 'fixed'; ta.style.opacity = '0'
    document.body.appendChild(ta); ta.focus(); ta.select()
    try { document.execCommand('copy'); toast.success(t('result.copied')) }
    catch { toast.error('Copy failed — please copy manually') }
    document.body.removeChild(ta)
  }

  return (
    <div className="space-y-4 fade-in-up">
      {/* Main Verdict Card */}
      <div className="rounded-2xl p-7 text-center"
        style={{ backgroundColor: cfg.bgVar, border: `2px solid ${cfg.colorVar}` }}>
        <Icon size={52} style={{ color: cfg.colorVar }} className="mx-auto mb-3" />
        <h2 className="text-2xl font-extrabold mb-4" style={{ color: cfg.colorVar }}>
          {t(`verdict.${result.verdict}`)}
        </h2>

        {/* Confidence Bar */}
        <div className="mb-4 text-left">
          <div className="flex justify-between text-xs mb-1.5 font-medium">
            <span style={{ color: 'var(--color-text)' }}>{t('result.confidence')}</span>
            <span className="font-bold" style={{ color: cfg.colorVar }}>{result.confidence}%</span>
          </div>
          <div className="h-3 rounded-full overflow-hidden" style={{ backgroundColor: 'var(--color-border)' }}>
            <div className="h-full rounded-full conf-bar"
              style={{ width: `${result.confidence}%`, backgroundColor: cfg.colorVar }} />
          </div>
        </div>

        <p className="text-sm leading-relaxed font-medium" style={{ color: 'var(--color-text)' }}>
          {explanation}
        </p>
      </div>

      {/* Frame info for video */}
      {result.frames_analyzed && (
        <p className="text-xs text-center font-medium" style={{ color: 'var(--color-text-muted)' }}>
          {result.frames_analyzed} {t('result.frames')}
        </p>
      )}

      {/* File name */}
      <p className="text-xs text-center" style={{ color: 'var(--color-text-muted)' }}>
        {t('result.file_checked')}:{' '}
        <span className="font-semibold" style={{ color: 'var(--color-text)' }}>{fileName}</span>
      </p>

      {/* What to do next */}
      <div className="rounded-xl p-4"
        style={{ backgroundColor: 'var(--color-surface)', border: '1px solid var(--color-border)' }}>
        <p className="text-sm font-bold mb-1" style={{ color: 'var(--color-text)' }}>
          {t('result.what_next')}
        </p>
        <p className="text-sm font-medium" style={{ color: 'var(--color-text-muted)' }}>
          {t(nextKey)}
        </p>
      </div>

      {/* Action Buttons */}
      <div className="grid grid-cols-2 gap-3">
        <button onClick={handleShare}
          className="flex items-center justify-center gap-2 py-3 px-4 rounded-xl font-semibold text-white text-sm"
          style={{ background: 'linear-gradient(135deg, var(--color-primary), var(--color-primary-dark))' }}>
          <Share2 size={15} />{t('actions.share')}
        </button>
        <a href="https://cybercrime.gov.in" target="_blank" rel="noreferrer"
          className="flex items-center justify-center gap-2 py-3 px-4 rounded-xl font-semibold text-sm"
          style={{ backgroundColor: 'var(--color-surface)', border: '1.5px solid var(--color-border)', color: 'var(--color-text)', textDecoration: 'none' }}>
          <ExternalLink size={15} />{t('actions.report_cyber')}
        </a>
      </div>

      <button onClick={onReset}
        className="w-full flex items-center justify-center gap-2 py-3 rounded-xl font-semibold text-sm transition-all hover:opacity-80"
        style={{ backgroundColor: 'transparent', border: '1.5px dashed var(--color-border)', color: 'var(--color-text-muted)' }}>
        <RotateCcw size={15} />{t('actions.check_another')}
      </button>
    </div>
  )
}
