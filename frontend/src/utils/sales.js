import { parse_date } from './dates.js'

export function sales_totals(rows) {
    return {
        pizzas: rows.reduce((sum, row) => sum + row.quantity, 0),
        orders: new Set(rows.map((row) => row.order_id)).size,
        revenue: rows.reduce((sum, row) => sum + row.amount, 0),
    }
}

export function group_quantities(rows, key) {
    const totals = new Map()
    rows.forEach((row) => totals.set(row[key], (totals.get(row[key]) || 0) + row.quantity))
    return [...totals].map(([label, value]) => ({ label, value })).sort((a, b) => b.value - a.value)
}

export function sales_chart(rows) {
    return group_quantities(rows, 'date').sort((a, b) => a.label.localeCompare(b.label))
}

export function add_missing_days(rows, start, end) {
    const values = new Map(rows.map((row) => [row.label, row.value]))
    const date = parse_date(start)
    const last = parse_date(end)
    if (!date || !last) return rows
    const result = []

    while (date <= last) {
        const label = date.toISOString().slice(0, 10)
        result.push({ label, value: values.has(label) ? values.get(label) : null })
        date.setUTCDate(date.getUTCDate() + 1)
    }

    return result
}
