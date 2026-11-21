<template>
    <div class="container mt-5">
        <div class="row align-items-center g-4">
            <div class="col-12 col-lg-6">
                <h2 class="title-md text-white">
                    Cada objeto tiene un precio.
                </h2>
                <h2 class="title-md text-secondary">
                    Conoce el mejor.
                </h2>

                <p class="mt-4 text-white-50">
                    El mercado de World of Warcraft, en un solo lugar. Compara precios, descubre tendencias y haz que cada moneda de oro cuente.
                </p>

                <div class="row g-3 mt-4">
                    <div class="col-6">
                        <button
                            class="btn btn-secondary w-100"
                            @click="router.push('/search')"
                        >
                            Explorar el mercado
                        </button>
                    </div>
                    <div class="col-6">
                        <button
                            class="btn btn-grey border w-100"
                            @click="router.push('/login')"
                        >
                            Cómo funciona
                        </button>
                    </div>
                </div>
            </div>
            <div class="col-12 col-lg-6 text-center">
                <img
                    :src="heroChart"
                    class="img-fluid d-block mx-auto"
                    alt="Gráfica ascendente rodeada de círculos dorados"
                >
            </div>
        </div>

        <section
            class="row row-cols-1 row-cols-sm-2 row-cols-lg-4 g-4 mt-5 pt-4 border-top border-secondary border-opacity-25"
            aria-label="Ventajas de Azeroth Exchange"
        >
            <div class="col">
                <h3 class=" text-white fw-bold mb-2">
                    Precios históricos
                </h3>
                <p class="small text-white-50 mb-0">
                    El contexto detrás de cada compra
                </p>
            </div>
            <div class="col">
                <h3 class="text-white fw-bold mb-2">
                    Compara reinos
                </h3>
                <p class="small text-white-50 mb-0">
                    Encuentra dónde vender mejor
                </p>
            </div>
            <div class="col">
                <h3 class="text-white fw-bold mb-2">
                    Alertas a tu medida
                </h3>
                <p class="small text-white-50 mb-0">
                    Tu próximo precio, bajo control
                </p>
            </div>
            <div class="col">
                <h3 class="text-white fw-bold mb-2">
                    Retail + Classic
                </h3>
                <p class="small text-white-50 mb-0">
                    Tu aventura. Tu mercado.
                </p>
            </div>
        </section>

        <section class="row align-items-center g-4 mt-5 pt-4 mb-5">
            <div class="col-12 col-lg-9">
                <p class="small fw-bold text-secondary mb-2">
                    EL PULSO DE AZEROTH
                </p>
                <h2 class="text-white mb-2">
                    Tu próxima oportunidad empieza aquí.
                </h2>
                <p class="lead text-white-50 mb-0">
                    Busca un objeto y descubre cuánto vale realmente en tu mercado.
                </p>
            </div>
        </section>
        <market-table
            id="mercado"
            :table-headers="marketHeaders"
            @select-item="selectedItem = $event"
        />
        <section
            id="herramientas"
            class="mt-6 pt-4 mb-5 pb-5"
            aria-labelledby="tools-title"
        >
            <p class="small fw-bold text-secondary mb-2">
                MENOS INTUICIÓN. MÁS INFORMACIÓN.
            </p>
            <h2
                id="tools-title"
                class="text-white mb-2"
            >
                Domina el mercado, a tu manera.
            </h2>
            <p class="text-white-50 mb-4">
                Consulta el historial de un objeto y la predicción que genera el modelo.
            </p>

            <div class="row row-cols-1 row-cols-lg-2 g-4">
                <div class="col">
                    <div class="tool-card h-100 p-4 rounded-3">
                        <p class="small fw-bold text-secondary mb-2">
                            01 / HISTORIAL DE PRECIOS
                        </p>
                        <h3 class="h4 text-white">
                            Sigue cada escaneo.
                        </h3>
                        <p class="text-white-50">
                            Selecciona un objeto de la tabla para revisar cómo cambió su precio por unidad.
                        </p>

                        <div
                            v-if="selectedItem"
                            aria-live="polite"
                        >
                            <p class="fw-bold text-white mb-1">
                                {{ selectedItem.name }}
                            </p>
                            <p
                                v-if="history.length"
                                class="text-white mb-3"
                            >
                                {{ formatPrice(history.at(-1).price) }}
                                <span class="small text-white-50 ms-2">Último escaneo</span>
                            </p>
                            <p
                                v-if="loading"
                                class="text-white-50"
                            >
                                Cargando historial...
                            </p>
                            <p
                                v-else-if="historyError"
                                class="text-white-50"
                            >
                                {{ historyError }}
                            </p>
                            <template v-else-if="history.length > 1">
                                <svg
                                    class="history-chart"
                                    viewBox="0 0 440 110"
                                    role="img"
                                    :aria-label="`Evolución del precio de ${selectedItem.name} en ${history.length} escaneos`"
                                >
                                    <line
                                        x1="0"
                                        y1="95"
                                        x2="440"
                                        y2="95"
                                        stroke="#39434a"
                                    />
                                    <polyline
                                        :points="chartPoints"
                                        fill="none"
                                        stroke="#ddba71"
                                        stroke-width="3"
                                    />
                                </svg>
                                <div class="d-flex justify-content-between small text-white-50">
                                    <span>Primer escaneo</span>
                                    <span>{{ history.length }} escaneos</span>
                                    <span>Último escaneo</span>
                                </div>
                            </template>
                            <p
                                v-else-if="!loading"
                                class="text-white-50"
                            >
                                Este objeto solo tiene un escaneo.
                            </p>
                        </div>
                        <p
                            v-else
                            class="text-white-50 mb-0"
                        >
                            Elige un objeto en la tabla.
                        </p>
                    </div>
                </div>

                <div class="col">
                    <div class="tool-card h-100 p-4 rounded-3">
                        <p class="small fw-bold text-secondary mb-2">
                            02 / PREDICCIÓN DEL MODELO
                        </p>
                        <h3 class="h4 text-white">
                            Una señal para decidir.
                        </h3>
                        <p class="text-white-50">
                            El modelo estima si el siguiente precio subirá, bajará o se mantendrá estable.
                        </p>

                        <div
                            v-if="selectedItem"
                            aria-live="polite"
                        >
                            <p class="fw-bold text-white mb-3">
                                {{ selectedItem.name }}
                            </p>
                            <p
                                v-if="loading"
                                class="text-white-50"
                            >
                                Calculando predicción...
                            </p>
                            <p
                                v-else-if="predictionError"
                                class="text-white-50"
                            >
                                {{ predictionError }}
                            </p>
                            <div
                                v-else-if="prediction"
                                class="prediction-result p-3 rounded-3"
                            >
                                <p class="small text-white-50 mb-1">
                                    Resultado estimado
                                </p>
                                <p class="h3 text-secondary fw-bold mb-2">
                                    {{ predictionLabel }}
                                </p>
                                <p class="small text-white-50 mb-1">
                                    Confianza del modelo: {{ confidence }}%
                                </p>
                                <p class="small text-white-50 mb-0">
                                    Precio analizado: {{ formatPrice(prediction.current_price) }}
                                </p>
                            </div>
                        </div>
                        <p
                            v-else
                            class="text-white-50 mb-0"
                        >
                            Elige un objeto en la tabla.
                        </p>
                    </div>
                </div>
            </div>

            <div class="mt-6">
                <p class="small fw-bold text-secondary mb-4">
                    DE LA BÚSQUEDA A UNA MEJOR DECISIÓN
                </p>
                <div class="row row-cols-1 row-cols-md-3 g-4">
                    <div class="col">
                        <span class="h3 text-secondary">01</span>
                        <h3 class="h5 text-white mt-2">
                            Busca un objeto
                        </h3>
                        <p class="text-white-50">
                            Encuéntralo por nombre en el catálogo.
                        </p>
                    </div>
                    <div class="col">
                        <span class="h3 text-secondary">02</span>
                        <h3 class="h5 text-white mt-2">
                            Revisa su historial
                        </h3>
                        <p class="text-white-50">
                            Compara el precio y la cantidad entre escaneos.
                        </p>
                    </div>
                    <div class="col">
                        <span class="h3 text-secondary">03</span>
                        <h3 class="h5 text-white mt-2">
                            Consulta la predicción
                        </h3>
                        <p class="text-white-50">
                            Usa la estimación del modelo como información adicional.
                        </p>
                    </div>
                </div>
            </div>

            <div class="tool-card text-center rounded-3 p-4 p-md-5 mt-5">
                <p class="small fw-bold text-secondary mb-2">
                    EXPLORA LOS DATOS DISPONIBLES
                </p>
                <h2 class="text-white">
                    Haz que tu oro llegue más lejos.
                </h2>
                <p class="text-white-50 mb-4">
                    Busca un objeto y revisa la información que ofrece este conjunto de datos.
                </p>
                <a
                    class="btn btn-secondary px-4 py-3 fw-bold"
                    href="#mercado"
                >Explorar objetos</a>
            </div>
        </section>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { computed, ref, watch } from 'vue'
import heroChart from 'ASSETS/images/hero-chart.svg'
import MarketTable from 'COMPONENTS/MarketTable.vue'
import sendRequest from 'LIBS/sendRequest'
import { formatPrice } from '../utils/market.js'

const router = useRouter()
const selectedItem = ref(null)
const history = ref([])
const prediction = ref(null)
const historyError = ref('')
const predictionError = ref('')
const loading = ref(false)
let requestId = 0

const predictionLabel = computed(() => ({
    SUBE: 'Podría subir',
    BAJA: 'Podría bajar',
    ESTABLE: 'Podría mantenerse',
})[prediction.value?.prediction] || 'Sin resultado')

const confidence = computed(() => (Number(prediction.value?.confidence) * 100).toFixed(1).replace('.', ','))

const chartPoints = computed(() => {
    const prices = history.value.map((entry) => Number(entry.price)).filter(Number.isFinite)
    if (prices.length < 2) return ''
    const min = Math.min(...prices)
    const max = Math.max(...prices)
    return prices.map((price, index) => {
        const x = (index / (prices.length - 1)) * 440
        const y = max === min ? 55 : 95 - ((price - min) / (max - min)) * 80
        return `${x.toFixed(1)},${y.toFixed(1)}`
    }).join(' ')
})

watch(() => selectedItem.value?.item_key, async (itemKey) => {
    const currentRequest = ++requestId
    history.value = []
    prediction.value = null
    historyError.value = ''
    predictionError.value = ''
    if (!itemKey) {
        loading.value = false
        return
    }

    loading.value = true
    const [historyResult, predictionResult] = await Promise.all([
        sendRequest(`items/${encodeURIComponent(itemKey)}/history`),
        sendRequest(`predict/${encodeURIComponent(itemKey)}`),
    ])
    if (currentRequest !== requestId) return

    history.value = Array.isArray(historyResult.data?.history) ? historyResult.data.history : []
    prediction.value = predictionResult.success ? predictionResult.data : null
    historyError.value = historyResult.success ? '' : historyResult.error || 'No se pudo cargar el historial.'
    predictionError.value = predictionResult.success ? '' : predictionResult.error || 'No se pudo obtener la predicción.'
    loading.value = false
})
const marketHeaders = [
    { key: 'item', label: 'Objeto' },
    { key: 'price', label: 'Precio por unidad' },
    { key: 'change', label: 'Cambio entre escaneos' },
    { key: 'trend', label: 'Últimos escaneos' },
    { key: 'quantity', label: 'Cantidad escaneada' },
    { key: 'favorite', label: 'Favorito' },
]
</script>

<style scoped>
.tool-card { border: 1px solid #303a42; background: #151c22; }
.prediction-result { border: 1px solid #435747; background: #1a2924; }
.history-chart { display: block; width: 100%; height: 110px; margin: 18px 0 8px; }
</style>
