const BACKEND = import.meta.env.VITE_BACKEND_URL || 'https://ofc01-janrakshak-api.hf.space'

export async function analyzeFile(file) {
  const isVideo = file.type.startsWith('video/')
  const endpoint = isVideo ? '/analyze/video' : '/analyze/image'
  const formData = new FormData()
  formData.append('file', file)

  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), 120000)

  try {
    const res = await fetch(`${BACKEND}${endpoint}`, {
      method: 'POST',
      body: formData,
      signal: controller.signal,
    })
    clearTimeout(timeout)
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || `HTTP ${res.status}`)
    }
    return await res.json()
  } catch (err) {
    clearTimeout(timeout)
    if (err.name === 'AbortError') throw new Error('Request timed out')
    throw err
  }
}
