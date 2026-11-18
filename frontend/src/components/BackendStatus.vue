<template>
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">Conexión con la API</h5>

      <p class="card-text">{{ status_message }}</p>

      <button
        type="button"
        class="btn btn-primary"
        :disabled="is_loading"
        @click="check_connection"
      >
        {{ is_loading ? 'Comprobando...' : 'Comprobar conexión' }}
      </button>
    </div>
  </div>
</template>

<script setup>
// Imports
import { onMounted, ref } from 'vue'

// Variables
const is_loading = ref(false)
const status_message = ref('Conexión pendiente')

// Methods
const check_connection = async () => {
  is_loading.value = true
  status_message.value = 'Conectando...'

  try {
    const api_url = import.meta.env.VITE_API_URL

    if (!api_url) {
      throw new Error('Falta configurar VITE_API_URL en .env.local')
    }

    const response = await fetch(`${api_url}/health`, {
      signal: AbortSignal.timeout(5000),
    })

    if (!response.ok) {
      throw new Error(`Error del servidor: ${response.status}`)
    }

    const data = await response.json()

    if (data.status !== 'ok') {
      throw new Error('El backend no reportó un estado correcto')
    }

    status_message.value = data.message
  } catch (error) {
    console.error('Error al conectar con la API:', error)
    status_message.value =
      error instanceof Error
        ? error.message
        : 'No fue posible conectar con el backend'
  } finally {
    is_loading.value = false
  }
}

// Hooks
onMounted(check_connection)
</script>