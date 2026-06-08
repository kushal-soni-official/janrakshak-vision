const MAX_BYTES = 100 * 1024 * 1024
const ALLOWED_IMAGE = ['image/jpeg', 'image/png', 'image/webp', 'image/gif', 'image/bmp']
const ALLOWED_VIDEO = ['video/mp4', 'video/avi', 'video/quicktime', 'video/x-matroska', 'video/x-msvideo']
const ALLOWED = [...ALLOWED_IMAGE, ...ALLOWED_VIDEO]

export function validateFile(file) {
  if (!ALLOWED.includes(file.type)) return { valid: false, error: 'errors.wrong_type' }
  if (file.size > MAX_BYTES) return { valid: false, error: 'errors.too_large' }
  return { valid: true }
}

export function isVideo(file) {
  return ALLOWED_VIDEO.includes(file.type)
}
