export function formatPrice(copper) {
    const amount = Math.round(Number(copper))
    if (!Number.isFinite(amount) || amount < 0) return '—'
    const gold = Math.floor(amount / 10000)
    const silver = Math.floor((amount % 10000) / 100)
    const bronze = amount % 100
    return `${gold.toLocaleString('es-MX')} oro · ${String(silver).padStart(2, '0')} plata · ${String(bronze).padStart(2, '0')} cobre`
}
