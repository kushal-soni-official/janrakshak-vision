import { useTranslation } from 'react-i18next'
import { X, ExternalLink, Star, Crown } from 'lucide-react'

const TEAM_MEMBERS = [
  {
    id: 1,
    name: 'Kushal Soni',
    role: 'Front end | Back end | AI/ML Integration',
    isLeader: true,
    github: 'https://github.com/kushal-soni-official',
    works: ['Front end', 'Back end', 'AI/ML Integration'],
    avatar: 'K',
  },
  {
    id: 2,
    name: 'Vinod Kumar Prajapat',
    role: 'Testing | Miro Architecture | Presentation',
    isLeader: false,
    github: '#',
    works: ['Miro architecture design', 'Testing and debugging', 'Presentation'],
    avatar: 'V',
  },
  {
    id: 3,
    name: 'Vishal Vishwakarma',
    role: 'Member',
    isLeader: false,
    github: '#',
    works: [],
    avatar: 'V',
  },
]

export default function TeamModal({ onClose }) {
  const { t } = useTranslation()

  // Close on backdrop click
  const handleBackdrop = (e) => {
    if (e.target === e.currentTarget) onClose()
  }

  return (
    <div
      className="fixed inset-0 z-[100] flex items-end sm:items-center justify-center p-0 sm:p-4"
      style={{ backgroundColor: 'rgba(0,0,0,0.55)', backdropFilter: 'blur(4px)' }}
      onClick={handleBackdrop}
    >
      <div
        className="w-full sm:max-w-md rounded-t-3xl sm:rounded-2xl overflow-hidden fade-in-up"
        style={{ backgroundColor: 'var(--color-surface)', border: '1px solid var(--color-border)', boxShadow: 'var(--shadow-lg)' }}
      >
        {/* Header */}
        <div className="px-5 pt-5 pb-4 border-b flex items-start justify-between"
          style={{ borderColor: 'var(--color-border)', background: 'linear-gradient(135deg, var(--color-primary)18, transparent)' }}>
          <div>
            <div className="flex items-center gap-2 mb-0.5">
              <div className="w-7 h-7 rounded-lg flex items-center justify-center"
                style={{ background: 'linear-gradient(135deg, var(--color-primary), var(--color-primary-dark))' }}>
                <Star size={13} color="white" />
              </div>
              <h2 className="text-lg font-bold" style={{ color: 'var(--color-text)' }}>
                {t('team.title')}
              </h2>
            </div>
            <p className="text-xs" style={{ color: 'var(--color-text-muted)' }}>
              {t('team.subtitle')}
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg transition-colors mt-0.5"
            style={{ color: 'var(--color-text-muted)', backgroundColor: 'var(--color-surface2)' }}
            aria-label={t('team.close')}
          >
            <X size={16} />
          </button>
        </div>

        {/* Members list */}
        <div className="px-5 py-4 space-y-3 max-h-[65vh] overflow-y-auto">
          {TEAM_MEMBERS.map((member) => (
            <div
              key={member.id}
              className="rounded-xl p-4 transition-all"
              style={{
                backgroundColor: 'var(--color-surface2)',
                border: member.isLeader
                  ? '1.5px solid var(--color-primary)'
                  : '1px solid var(--color-border)',
              }}
            >
              <div className="flex items-start gap-3">
                {/* Avatar circle */}
                <div
                  className="w-11 h-11 rounded-full flex items-center justify-center text-xl shrink-0"
                  style={{
                    background: member.isLeader
                      ? 'linear-gradient(135deg, var(--color-primary), var(--color-primary-dark))'
                      : 'var(--color-border)',
                  }}
                >
                  {member.isLeader ? <Crown size={18} color="white" /> : <span>{member.avatar}</span>}
                </div>

                {/* Info */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="font-semibold text-sm" style={{ color: 'var(--color-text)' }}>
                      {member.name}
                    </span>
                    <span
                      className="text-xs px-2 py-0.5 rounded-full font-medium"
                      style={{
                        backgroundColor: member.isLeader ? 'var(--color-primary)' : 'var(--color-border)',
                        color: member.isLeader ? 'white' : 'var(--color-text-muted)',
                      }}
                    >
                      {member.isLeader ? t('team.leader_badge') : t('team.member_badge')}
                    </span>
                  </div>
                  <p className="text-xs mt-0.5" style={{ color: 'var(--color-text-muted)' }}>
                    {member.role}
                  </p>

                  {/* Works */}
                  <ul className="mt-2 space-y-0.5">
                    {member.works.map((w, i) => (
                      <li key={i} className="text-xs flex items-start gap-1.5" style={{ color: 'var(--color-text-muted)' }}>
                        <span style={{ color: 'var(--color-primary)', marginTop: '1px' }}>▸</span>
                        {w}
                      </li>
                    ))}
                  </ul>

                  {/* GitHub link */}
                  <a
                    href={member.github}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1 mt-2 text-xs font-medium transition-opacity hover:opacity-75"
                    style={{ color: 'var(--color-primary)', textDecoration: 'none' }}
                  >
                    <ExternalLink size={11} /> GitHub
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="px-5 py-3 border-t flex items-center justify-between"
          style={{ borderColor: 'var(--color-border)' }}>
          <p className="text-xs" style={{ color: 'var(--color-text-muted)' }}>
            🏆 Tradition Hacks 2026
          </p>
          <button
            onClick={onClose}
            className="text-xs px-4 py-1.5 rounded-lg font-medium"
            style={{ backgroundColor: 'var(--color-primary)', color: 'white' }}
          >
            {t('team.close')}
          </button>
        </div>
      </div>
    </div>
  )
}
