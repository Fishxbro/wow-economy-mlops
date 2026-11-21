export function parse_date(value) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(value || '')) return null
    const date = new Date(`${value}T00:00:00Z`)
    return Number.isNaN(date.getTime()) || date.toISOString().slice(0, 10) !== value ? null : date
}

export function date_range_error(start, end) {
    const first = parse_date(start)
    const last = parse_date(end)
    if (!first || !last) return 'Selecciona fechas válidas.'
    const days = (last - first) / 86400000 + 1
    if (days < 1) return 'La fecha final debe ser igual o posterior a la inicial.'
    if (days > 366) return 'El rango no puede superar 366 días.'
    return ''
}

export function format_date(value) {
    const date = parse_date(value)
    return date
        ? new Intl.DateTimeFormat('es-MX', {
              timeZone: 'UTC',
              day: '2-digit',
              month: '2-digit',
              year: 'numeric',
          }).format(date)
        : value
}

export function weekday(value) {
    const date = parse_date(value)
    return date
        ? new Intl.DateTimeFormat('es-MX', { timeZone: 'UTC', weekday: 'long' }).format(date)
        : ''
}

export function number(value, decimals = 0) {
    return new Intl.NumberFormat('es-MX', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals,
    }).format(Number(value) || 0)
}

export function money(value) {
    return new Intl.NumberFormat('es-MX', { style: 'currency', currency: 'USD' }).format(
        Number(value) || 0,
    )
}
