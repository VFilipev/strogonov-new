export function toURLParams(filter = {}) {
  const params = new URLSearchParams()

  Object.entries(filter || {}).forEach(([key, value]) => {
    if (value === undefined || value === null || value === '') return

    if (Array.isArray(value)) {
      value.forEach((item) => {
        if (item !== undefined && item !== null && item !== '') {
          params.append(key, String(item))
        }
      })
      return
    }

    params.append(key, String(value))
  })

  return params.toString()
}

export function normalizeListResponse(value) {
  if (!value) return []
  if (Array.isArray(value)) return value
  if (typeof value === 'object' && Array.isArray(value.results)) return value.results
  return []
}
