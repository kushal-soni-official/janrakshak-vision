import { createContext, useContext, useState, useEffect } from 'react'

const ThemeContext = createContext()

function hexToRgbAdj(hex, amt) {
  const n = parseInt(hex.replace('#', ''), 16)
  const r = Math.min(255, Math.max(0, (n >> 16) + amt))
  const g = Math.min(255, Math.max(0, ((n >> 8) & 0xff) + amt))
  const b = Math.min(255, Math.max(0, (n & 0xff) + amt))
  return '#' + [r, g, b].map(x => x.toString(16).padStart(2, '0')).join('')
}

export function ThemeProvider({ children }) {
  const [theme, setThemeState] = useState(() => localStorage.getItem('jr_theme') || 'default')
  const [mode, setModeState] = useState(() => localStorage.getItem('jr_mode') || 'light')
  const [customColor, setCustomColorState] = useState(() => localStorage.getItem('jr_custom') || '#2563EB')

  const applyAll = (t, m, color) => {
    const root = document.documentElement
    root.setAttribute('data-theme', t === 'default' ? '' : t)
    root.setAttribute('data-mode', m)
    if (t === 'custom') {
      root.style.setProperty('--color-primary', color)
      root.style.setProperty('--color-primary-dark', hexToRgbAdj(color, -30))
      root.style.setProperty('--color-primary-light', hexToRgbAdj(color, 80))
    } else {
      root.style.removeProperty('--color-primary')
      root.style.removeProperty('--color-primary-dark')
      root.style.removeProperty('--color-primary-light')
    }
  }

  useEffect(() => { applyAll(theme, mode, customColor) }, [theme, mode])

  const setTheme = (t) => { setThemeState(t); localStorage.setItem('jr_theme', t) }
  const toggleMode = () => {
    const next = mode === 'light' ? 'dark' : 'light'
    setModeState(next)
    localStorage.setItem('jr_mode', next)
    applyAll(theme, next, customColor)
  }
  const setCustomColor = (color) => {
    setCustomColorState(color)
    localStorage.setItem('jr_custom', color)
    setThemeState('custom')
    applyAll('custom', mode, color)
  }

  return (
    <ThemeContext.Provider value={{ theme, setTheme, mode, toggleMode, customColor, setCustomColor }}>
      {children}
    </ThemeContext.Provider>
  )
}

export const useTheme = () => useContext(ThemeContext)
