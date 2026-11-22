const API_URL = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000').replace(/\/$/, '')

export default async function sendRequest(path, method = 'GET', body = null, query = null) {
    const url = new globalThis.URL(`${API_URL}/${path.replace(/^\//, '')}`)

    Object.entries(query || {}).forEach(([key, value]) => {
        if (value !== null && value !== undefined && value !== '') {
            url.searchParams.set(key, value)
        }
    })

    try {
        const response = await globalThis.fetch(url, {
            method,
            headers: body ? { 'Content-Type': 'application/json' } : undefined,
            body: body ? JSON.stringify(body) : undefined,
            signal: globalThis.AbortSignal.timeout(60000),
        })
        const data = await response.json().catch(() => null)

        if (!response.ok) {
            const detail =
                typeof data?.detail === 'string' ? data.detail : `Error HTTP ${response.status}`
            return { success: false, data: null, error: detail }
        }

        return { success: true, data, error: null, headers: response.headers }
    } catch (error) {
        return {
            success: false,
            data: null,
            error: error.message || 'No se pudo conectar con la API',
        }
    }
}
