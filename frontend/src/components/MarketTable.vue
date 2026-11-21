<template>
    <div class="market-widget">
        <form
            class="market-search"
            role="search"
            @submit.prevent="searchItems"
        >
            <label class="market-query">
                <span
                    class="search-icon"
                    aria-hidden="true"
                >⌕</span>
                <span class="visually-hidden">Buscar objetos</span>
                <input
                    v-model="query"
                    type="search"
                    maxlength="100"
                    placeholder="Busca materiales, equipo, consumibles..."
                >
            </label>
            <button
                class="search-button"
                type="submit"
                :disabled="loading"
            >
                {{ loading ? 'Buscando...' : 'Buscar objetos' }}
            </button>
        </form>

        <div class="market-toolbar">
            <div
                class="market-filters"
                aria-label="Filtros de objetos"
            >
                <button
                    type="button"
                    :class="{ active: !favoritesOnly }"
                    @click="favoritesOnly = false"
                >
                    Todos los objetos
                </button>
                <button
                    type="button"
                    :class="{ active: favoritesOnly }"
                    @click="favoritesOnly = true"
                >
                    Favoritos de esta página <span v-if="pageFavoriteCount">({{ pageFavoriteCount }})</span>
                </button>
            </div>
            <span class="market-source">Datos del mercado · API</span>
        </div>

        <div class="market-card">
            <div class="market-scroll">
                <table>
                    <thead>
                        <tr>
                            <th
                                v-for="header in tableHeaders"
                                :key="header.key"
                                scope="col"
                            >
                                {{ header.label }}
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr
                            v-for="item in visibleItems"
                            :key="item.item_key"
                        >
                            <td
                                v-for="header in tableHeaders"
                                :key="header.key"
                            >
                                <template v-if="header.key === 'item'">
                                    <div class="item-cell">
                                        <span
                                            class="item-symbol"
                                            aria-hidden="true"
                                        >{{ item.name?.slice(0, 1) || '?' }}</span>
                                        <span>
                                            <button
                                                type="button"
                                                class="item-name"
                                                :aria-label="`Consultar historial y predicción de ${item.name}`"
                                                @click="emit('select-item', item)"
                                            >
                                                {{ item.name }}
                                            </button>
                                            <small>ID {{ item.itemid || 'desconocido' }}</small>
                                        </span>
                                    </div>
                                </template>
                                <template v-else-if="header.key === 'price'">
                                    <span class="price-value">{{ formatPrice(item.price) }}</span>
                                </template>
                                <template v-else-if="header.key === 'change'">
                                    <span :class="changeClass(item)">{{ formatChange(item) }}</span>
                                </template>
                                <template v-else-if="header.key === 'trend'">
                                    <svg
                                        v-if="sparkline(item)"
                                        class="sparkline"
                                        viewBox="0 0 144 44"
                                        role="img"
                                        :aria-label="`Historial de ${item.name}`"
                                    >
                                        <polyline
                                            :points="sparkline(item)"
                                            fill="none"
                                            stroke="#62d4ac"
                                            stroke-width="2"
                                        />
                                    </svg>
                                    <span
                                        v-else
                                        class="muted"
                                    >Sin historial</span>
                                </template>
                                <template v-else-if="header.key === 'quantity'">
                                    {{ formatQuantity(item) }}
                                </template>
                                <template v-else-if="header.key === 'favorite'">
                                    <button
                                        class="favorite-button"
                                        type="button"
                                        :aria-label="isFavorite(item) ? `Quitar ${item.name} de favoritos` : `Agregar ${item.name} a favoritos`"
                                        :aria-pressed="isFavorite(item)"
                                        @click="toggleFavorite(item)"
                                    >
                                        {{ isFavorite(item) ? '★' : '☆' }}
                                    </button>
                                </template>
                                <template v-else>
                                    {{ item[header.key] ?? '—' }}
                                </template>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <p
                v-if="loading"
                class="market-message"
                role="status"
            >
                Cargando objetos...
            </p>
            <p
                v-else-if="error"
                class="market-message market-error"
                role="alert"
            >
                {{ error }} <button
                    type="button"
                    @click="loadItems"
                >
                    Reintentar
                </button>
            </p>
            <p
                v-else-if="!visibleItems.length"
                class="market-message"
            >
                {{ favoritesOnly ? 'No hay favoritos en esta página.' : 'No se encontraron objetos.' }}
            </p>

            <div class="market-footer">
                <span>Datos históricos del conjunto cargado · precio por unidad en oro, plata y cobre · cantidad del último escaneo.</span>
                <span
                    v-if="!loading && !error"
                    aria-live="polite"
                >
                    {{ totalCount ? `${firstItem}–${lastItem} de ${totalCount} objetos` : '0 objetos' }}
                </span>
            </div>
            <nav
                v-if="!loading && !error && totalPages > 1"
                class="market-pagination"
                aria-label="Páginas del mercado"
            >
                <button
                    type="button"
                    aria-label="Primera página"
                    :disabled="page === 1"
                    @click="changePage(1)"
                >
                    «
                </button>
                <button
                    type="button"
                    :disabled="page === 1"
                    @click="changePage(page - 1)"
                >
                    Anterior
                </button>
                <button
                    v-for="number in pageNumbers"
                    :key="number"
                    type="button"
                    :class="{ current: page === number }"
                    :aria-current="page === number ? 'page' : undefined"
                    :aria-label="`Página ${number}`"
                    @click="changePage(number)"
                >
                    {{ number }}
                </button>
                <button
                    type="button"
                    :disabled="page === totalPages"
                    @click="changePage(page + 1)"
                >
                    Siguiente
                </button>
                <button
                    type="button"
                    aria-label="Última página"
                    :disabled="page === totalPages"
                    @click="changePage(totalPages)"
                >
                    »
                </button>
                <span class="page-summary">Página {{ page }} de {{ totalPages }}</span>
            </nav>
        </div>
    </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import sendRequest from 'LIBS/sendRequest'
import { formatPrice } from '../utils/market.js'

const props = defineProps({
    tableHeaders: {
        type: Array,
        required: true,
    },
    pageSize: {
        type: Number,
        default: 5,
    },
})
const emit = defineEmits(['select-item'])

const query = ref('')
const submittedQuery = ref('')
const items = ref([])
const histories = ref({})
const loading = ref(false)
const error = ref('')
const page = ref(1)
const totalCount = ref(0)
const favoritesOnly = ref(false)
const favorites = ref(readFavorites())
let requestId = 0

const visibleItems = computed(() =>
    favoritesOnly.value
        ? items.value.filter((item) => favorites.value.includes(item.item_key))
        : items.value,
)
const pageFavoriteCount = computed(() => items.value.filter((item) => favorites.value.includes(item.item_key)).length)
const totalPages = computed(() => Math.ceil(totalCount.value / props.pageSize))
const firstItem = computed(() => (page.value - 1) * props.pageSize + 1)
const lastItem = computed(() => Math.min(page.value * props.pageSize, totalCount.value))
const pageNumbers = computed(() => {
    const start = Math.max(1, Math.min(page.value - 2, totalPages.value - 4))
    const end = Math.min(totalPages.value, start + 4)
    return Array.from({ length: end - start + 1 }, (_, index) => start + index)
})

function readFavorites() {
    try {
        const stored = JSON.parse(globalThis.localStorage.getItem('wow-market-favorites') || '[]')
        return Array.isArray(stored) ? stored.filter((key) => typeof key === 'string') : []
    } catch {
        return []
    }
}

function isFavorite(item) {
    return favorites.value.includes(item.item_key)
}

function toggleFavorite(item) {
    favorites.value = isFavorite(item)
        ? favorites.value.filter((key) => key !== item.item_key)
        : [...favorites.value, item.item_key]
    try {
        globalThis.localStorage.setItem('wow-market-favorites', JSON.stringify(favorites.value))
    } catch {
        // La tabla sigue funcionando si el navegador bloquea el almacenamiento.
    }
}

async function loadItems() {
    const currentRequest = ++requestId
    loading.value = true
    error.value = ''
    items.value = []
    histories.value = {}
    emit('select-item', null)
    const result = await sendRequest('items', 'GET', null, {
        search: submittedQuery.value,
        limit: props.pageSize,
        offset: (page.value - 1) * props.pageSize,
    })
    if (currentRequest !== requestId) return

    if (!result.success || !Array.isArray(result.data)) {
        error.value = result.error || 'No se pudo cargar el catálogo.'
        loading.value = false
        return
    }

    items.value = result.data
    emit('select-item', items.value[0] ?? null)
    const countHeader = result.headers?.get('X-Total-Count')
    totalCount.value = countHeader === null || countHeader === undefined
        ? (page.value - 1) * props.pageSize + items.value.length
        : Number(countHeader)
    loading.value = false

    // El historial permite calcular la variación y la cantidad sin inventar datos.
    for (let offset = 0; offset < items.value.length; offset += 5) {
        if (currentRequest !== requestId) return
        await Promise.all(items.value.slice(offset, offset + 5).map(async (item) => {
            const historyResult = await sendRequest(
                `items/${encodeURIComponent(item.item_key)}/history`,
            )
            if (currentRequest === requestId && historyResult.success) {
                histories.value = { ...histories.value, [item.item_key]: historyResult.data?.history || [] }
            }
        }))
    }
}

function searchItems() {
    submittedQuery.value = query.value.trim()
    page.value = 1
    favoritesOnly.value = false
    loadItems()
}

function changePage(number) {
    if (number < 1 || number > totalPages.value || number === page.value) return
    page.value = number
    loadItems()
}

function formatQuantity(item) {
    const history = histories.value[item.item_key]
    const quantity = Number(history?.at(-1)?.quantity)
    return Number.isFinite(quantity) ? quantity.toLocaleString('es-MX') : '—'
}

function changeValue(item) {
    const history = histories.value[item.item_key]
    if (!history || history.length < 2) return null
    const latest = history.at(-1)
    const previous = history.at(-2)
    const currentPrice = Number(latest.price)
    const previousPrice = Number(previous.price)
    if (!Number.isFinite(currentPrice) || !Number.isFinite(previousPrice) || previousPrice <= 0) return null
    return ((currentPrice - previousPrice) / previousPrice) * 100
}

function formatChange(item) {
    const change = changeValue(item)
    return change === null ? 'Sin datos previos' : `${change > 0 ? '+' : ''}${change.toFixed(1).replace('.', ',')}%`
}

function changeClass(item) {
    const change = changeValue(item)
    return change === null ? 'muted' : change > 0 ? 'change-up' : change < 0 ? 'change-down' : 'muted'
}

function sparkline(item) {
    const history = histories.value[item.item_key]
    if (!history || history.length < 2) return ''
    const points = history
        .filter((point) => Number.isFinite(Number(point.price)))
        .slice(-24)
    if (points.length < 2) return ''
    const prices = points.map((point) => Number(point.price))
    const min = Math.min(...prices)
    const max = Math.max(...prices)
    return prices.map((price, index) => {
        const x = (index / (prices.length - 1)) * 142 + 1
        const y = max === min ? 22 : 40 - ((price - min) / (max - min)) * 36
        return `${x.toFixed(1)},${y.toFixed(1)}`
    }).join(' ')
}

onMounted(loadItems)
</script>

<style scoped>
.market-widget { width: 100%; }
.market-search { display: flex; align-items: center; gap: 20px; padding: 13px 15px 13px 23px; border: 1px solid #303a42; border-radius: 10px; background: #151c22; }
.market-query { display: flex; align-items: center; flex: 1; min-width: 0; gap: 16px; }
.search-icon { color: #94a3ad; font-size: 34px; line-height: 1; }
.market-query input { width: 100%; min-width: 0; border: 0; outline: 0; background: transparent; color: #eee; font: inherit; font-size: 16px; }
.market-query input::placeholder { color: #84909a; }
.search-button { min-height: 54px; min-width: 190px; border: 0; border-radius: 7px; background: #ddba71; color: #111; font-weight: 800; }
.search-button:hover:not(:disabled) { background: #edca82; }
.search-button:disabled { opacity: .65; }
.market-toolbar { display: flex; justify-content: space-between; align-items: center; gap: 16px; margin: 24px 0 20px; }
.market-filters { display: flex; flex-wrap: wrap; gap: 8px; }
.market-filters button { min-height: 40px; padding: 0 24px; border: 1px solid #2d3941; border-radius: 6px; background: #10171b; color: #9da7ae; }
.market-filters button.active { border-color: #705a30; background: #30291c; color: #e5c784; font-weight: 800; }
.market-source { color: #8d9a9b; font-size: 12px; white-space: nowrap; }
.market-card { overflow: hidden; border: 1px solid #303a42; border-radius: 10px; background: #10171c; }
.market-scroll { overflow-x: auto; }
table { width: 100%; min-width: 800px; border-collapse: collapse; }
th { padding: 18px 25px; background: #1b232b; color: #8998a2; text-align: left; text-transform: uppercase; font-size: 11px; font-weight: 800; white-space: nowrap; }
td { height: 82px; padding: 10px 25px; border-bottom: 1px solid #27323a; color: #c5c9cb; white-space: nowrap; }
tbody tr:nth-child(even) { background: #1b2128; }
.item-cell { display: flex; align-items: center; gap: 17px; }
.item-symbol { display: grid; place-items: center; width: 50px; height: 50px; flex: none; border: 1px solid #879eb2; border-radius: 8px; background: #242934; color: #c8adda; font-size: 24px; font-weight: 800; }
.item-name { display: block; padding: 0; border: 0; background: transparent; color: #a8c7df; font-weight: 800; text-align: left; }
.item-name:hover, .item-name:focus-visible { color: #d0e6f6; text-decoration: underline; }
.item-cell small { display: block; margin-top: 3px; color: #7f8d97; }
.price-value { color: #ece0c1; font-weight: 800; }
.change-up { color: #63d6aa; font-weight: 800; }
.change-down { color: #f09087; font-weight: 800; }
.muted { color: #80909a; font-size: 13px; }
.sparkline { display: block; width: 144px; height: 44px; }
.favorite-button { padding: 0; border: 0; background: transparent; color: #c5ae78; font-size: 26px; line-height: 1; }
.favorite-button:hover { color: #f3d98e; }
.market-message { margin: 0; padding: 24px; color: #aab5bb; }
.market-error { color: #f09087; }
.market-error button, .market-footer button { padding: 0; border: 0; background: transparent; color: #ddba71; font-weight: 800; }
.market-footer { display: flex; justify-content: space-between; gap: 20px; padding: 25px; color: #80909a; font-size: 12px; }
.market-pagination { display: flex; justify-content: center; flex-wrap: wrap; gap: 8px; padding: 0 24px 24px; }
.market-pagination button { min-width: 38px; min-height: 38px; padding: 0 12px; border: 1px solid #303a42; border-radius: 6px; background: #151c22; color: #bbc4ca; }
.market-pagination button:hover:not(:disabled), .market-pagination button.current { border-color: #a98747; background: #30291c; color: #e5c784; }
.market-pagination button:disabled { opacity: .4; cursor: not-allowed; }
.page-summary { align-self: center; margin-left: 8px; color: #8d9a9b; font-size: 12px; }
@media (max-width: 640px) { .market-search { flex-direction: column; align-items: stretch; } .search-button { width: 100%; } .market-toolbar { align-items: flex-start; flex-direction: column; } .market-footer { flex-direction: column; } }
</style>
