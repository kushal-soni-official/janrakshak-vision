const MAX_IMAGE_BYTES = 50 * 1024 * 1024   // 50MB — must match backend MAX_IMAGE
const MAX_VIDEO_BYTES = 100 * 1024 * 1024  // 100MB — must match backend MAX_VIDEO
const ALLOWED_IMAGE = ['image/jpeg', 'image/png', 'image/webp', 'image/gif', 'image/bmp']
const ALLOWED_VIDEO = ['video/mp4', 'video/avi', 'video/quicktime', 'video/x-matroska', 'video/x-msvideo']
const ALLOWED = [...ALLOWED_IMAGE, ...ALLOWED_VIDEO]

export function validateFile(file) {
  if (!ALLOWED.includes(file.type)) return { valid: false, error: 'errors.wrong_type' }
  const isVid = ALLOWED_VIDEO.includes(file.type)
  const limit = isVid ? MAX_VIDEO_BYTES : MAX_IMAGE_BYTES
  if (file.size > limit) return { valid: false, error: isVid ? 'errors.too_large_video' : 'errors.too_large_image' }
  return { valid: true }
}

export function isVideo(file) {
  return ALLOWED_VIDEO.includes(file.type)
}
