import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { useTranslation } from 'react-i18next'
import { UploadCloud, Image, Video, Lock, Zap } from 'lucide-react'
import { validateFile } from '../utils/fileValidator'
import toast from 'react-hot-toast'

export default function UploadZone({ onFileSelected }) {
  const { t } = useTranslation()
  const [dragging, setDragging] = useState(false)

  const STATS = [
    { val: t('upload.stat1_val'), desc: t('upload.stat1_desc') },
    { val: t('upload.stat2_val'), desc: t('upload.stat2_desc') },
    { val: t('upload.stat3_val'), desc: t('upload.stat3_desc') },
  ]

  const onDrop = useCallback((accepted, rejected) => {
    setDragging(false)
    if (rejected.length > 0) { toast.error(t('errors.wrong_type')); return }
    const file = accepted[0]
    if (!file) return
    const v = validateFile(file)
    if (!v.valid) { toast.error(t(v.error)); return }
    onFileSelected(file)
  }, [onFileSelected, t])

  const { getRootProps, getInputProps, open } = useDropzone({
    onDrop,
    onDragEnter: () => setDragging(true),
    onDragLeave: () => setDragging(false),
    accept: {
      'image/*': ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp'],
      'video/*': ['.mp4', '.avi', '.mov', '.mkv'],
    },
    maxSize: 100 * 1024 * 1024,
    multiple: false,
    noClick: true,
  })

  return (
    <div className="space-y-5 fade-in-up">
      {/* Header */}
      <div className="text-center pt-2">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full mb-4 text-xs font-semibold"
          style={{ backgroundColor: 'var(--color-primary)', color: 'white' }}>
          <Zap size={11} /> {t('upload.badge')}
        </div>
        <h1 className="text-3xl font-extrabold mb-2 gradient-text">{t('app.title')}</h1>
        <p className="text-sm leading-relaxed max-w-sm mx-auto" style={{ color: 'var(--color-text-muted)' }}>
          {t('app.subtitle')}
        </p>
      </div>

      {/* Drop Zone */}
      <div
        {...getRootProps()}
        className="rounded-2xl p-8 text-center transition-all duration-200 card"
        style={{
          border: `2px dashed ${dragging ? 'var(--color-primary)' : 'var(--color-border)'}`,
          backgroundColor: dragging ? 'rgba(37,99,235,0.04)' : 'var(--color-surface)',
          transform: dragging ? 'scale(1.01)' : 'scale(1)',
          boxShadow: dragging ? 'var(--shadow-md)' : 'var(--shadow-sm)',
        }}
      >
        <input {...getInputProps()} />
        <div className="flex flex-col items-center gap-4">
          <div className={`w-16 h-16 rounded-2xl flex items-center justify-center ${dragging ? 'pulse-ring' : ''}`}
            style={{ background: 'linear-gradient(135deg, rgba(37,99,235,0.14), rgba(37,99,235,0.06))' }}>
            <UploadCloud size={30} style={{ color: 'var(--color-primary)' }} />
          </div>

          <div>
            <p className="text-lg font-bold" style={{ color: 'var(--color-text)' }}>
              {t('upload.drag_drop')}
            </p>
            <p className="text-sm mt-1" style={{ color: 'var(--color-text-muted)' }}>
              {t('upload.or_click')}
            </p>
          </div>

          <div className="flex gap-3 text-xs flex-wrap justify-center">
            <span className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg font-medium"
              style={{ backgroundColor: 'var(--color-surface2)', border: '1px solid var(--color-border)', color: 'var(--color-text)' }}>
              <Image size={12} style={{ color: 'var(--color-primary)' }} /> {t('upload.images')}
            </span>
            <span className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg font-medium"
              style={{ backgroundColor: 'var(--color-surface2)', border: '1px solid var(--color-border)', color: 'var(--color-text)' }}>
              <Video size={12} style={{ color: 'var(--color-primary)' }} /> {t('upload.videos')}
            </span>
          </div>

          <p className="text-xs font-medium" style={{ color: 'var(--color-text-muted)' }}>
            {t('upload.max_size')}
          </p>

          <button type="button" onClick={open} className="btn-primary">
            {t('upload.cta')}
          </button>
        </div>
      </div>

      {/* Privacy note */}
      <p className="text-xs text-center flex items-center justify-center gap-1.5"
        style={{ color: 'var(--color-text-muted)' }}>
        <Lock size={11} />
        {t('upload.privacy')}
      </p>

      {/* Stats row */}
      <div className="grid grid-cols-3 gap-3">
        {STATS.map((s, i) => (
          <div key={i} className="text-center p-3 rounded-xl card card-hover">
            <p className="font-extrabold text-base gradient-text">{s.val}</p>
            <p className="text-xs mt-0.5 leading-tight" style={{ color: 'var(--color-text-muted)' }}>{s.desc}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
