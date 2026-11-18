<template>
  <button
    ref="menu_button"
    type="button"
    class="sidebar-toggle"
    aria-label="Abrir menú"
    aria-controls="dashboard-sidebar"
    :aria-expanded="menu_open"
    @click="menu_open = true"
  >
    ☰
  </button>

  <div
    v-if="menu_open && is_mobile"
    class="sidebar-backdrop"
    aria-hidden="true"
    @click="close_menu"
  ></div>

  <aside
    id="dashboard-sidebar"
    ref="sidebar_ref"
    class="dashboard-sidebar"
    :class="{ 'is-open': menu_open }"
    :role="is_mobile && menu_open ? 'dialog' : undefined"
    :aria-modal="is_mobile && menu_open ? true : undefined"
    aria-label="Navegación de PizzaDemand"
    @keydown="handle_keydown"
  >
    <header class="sidebar-header">
      <RouterLink
        to="/dashboard"
        class="sidebar-brand"
        @click="close_menu"
      >
        <slot name="logo">
          <span aria-hidden="true">◒</span>
        </slot>

        <span>PizzaDemand</span>
      </RouterLink>

      <button
        type="button"
        class="sidebar-close"
        aria-label="Cerrar menú"
        @click="close_menu"
      >
        ×
      </button>
    </header>

    <p class="sidebar-caption">
      ANÁLISIS Y PLANIFICACIÓN
    </p>

    <nav class="sidebar-navigation" aria-label="Menú principal">
      <RouterLink
        v-for="item in navigation_items"
        :key="item.to"
        :to="item.to"
        custom
        v-slot="{ href, navigate, isActive, isExactActive }"
      >
        <a
          :href="href"
          class="sidebar-link"
          :class="{
            'is-active': item.exact ? isExactActive : isActive,
          }"
          :aria-current="
            (item.exact ? isExactActive : isActive)
              ? 'page'
              : undefined
          "
          @click="handle_navigation($event, navigate)"
        >
          {{ item.label }}
        </a>
      </RouterLink>
    </nav>

    <footer class="sidebar-footer">
      <span class="sidebar-badge">
        Demo histórica · 2015
      </span>

      <p>
        Un proyecto de Ingeniería<br />
        Informática · UdeG
      </p>
    </footer>
  </aside>
</template>

<script setup>
// Imports
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

// Hooks
const route = useRoute()

// Variables
const menu_open = ref(false)
const is_mobile = ref(false)
const sidebar_ref = ref(null)
const menu_button = ref(null)

const navigation_items = [
  { label: 'Resumen', to: '/dashboard', exact: true },
  { label: 'Ventas históricas', to: '/dashboard/sales' },
  { label: 'Predicciones', to: '/dashboard/predictions' },
  { label: 'Modelos y experimentos', to: '/dashboard/models' },
  { label: 'Pipeline', to: '/dashboard/pipeline' },
  { label: 'Monitoreo', to: '/dashboard/monitoring' },
  { label: 'Configuración', to: '/dashboard/settings' },
]

let media_query
let previous_overflow = ''
let scroll_locked = false

// Watches
watch(() => route.fullPath, close_menu)

watch([menu_open, is_mobile], async ([open, mobile]) => {
  if (open && mobile) {
    if (!scroll_locked) {
      previous_overflow = document.body.style.overflow
      document.body.style.overflow = 'hidden'
      scroll_locked = true
    }

    await nextTick()
    sidebar_ref.value?.querySelector('a, button')?.focus()
  } else if (scroll_locked) {
    document.body.style.overflow = previous_overflow
    scroll_locked = false

    if (mobile) {
      await nextTick()
      menu_button.value?.focus()
    }
  }
})

// Methods
function close_menu() {
  menu_open.value = false
}

function handle_navigation(event, navigate) {
  navigate(event)
  close_menu()
}

function update_mobile(event) {
  is_mobile.value = event.matches

  if (!event.matches) {
    close_menu()
  }
}

function handle_keydown(event) {
  if (!is_mobile.value || !menu_open.value) return

  if (event.key === 'Escape') {
    event.preventDefault()
    close_menu()
    return
  }

  if (event.key !== 'Tab') return

  const elements = sidebar_ref.value.querySelectorAll(
    'a[href], button:not([disabled])',
  )

  const first = elements[0]
  const last = elements[elements.length - 1]

  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault()
    last?.focus()
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault()
    first?.focus()
  }
}

onMounted(() => {
  media_query = window.matchMedia('(max-width: 991.98px)')
  is_mobile.value = media_query.matches
  media_query.addEventListener('change', update_mobile)
})

onBeforeUnmount(() => {
  media_query?.removeEventListener('change', update_mobile)

  if (scroll_locked) {
    document.body.style.overflow = previous_overflow
  }
})
</script>

<style scoped>
.dashboard-sidebar {
  --sidebar-accent: #b94729;
  --sidebar-soft: #fbece5;
  --sidebar-ink: #272b28;
  --sidebar-muted: #696f69;

  position: fixed;
  inset: 0 auto 0 0;
  z-index: 1045;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 248px;
  height: 100dvh;
  padding: 24px;
  overflow-y: auto;
  background: #fff;
  color: var(--sidebar-ink);
  font-family: Inter, system-ui, sans-serif;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.sidebar-brand {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: var(--sidebar-ink);
  font-size: 18px;
  font-weight: 700;
  line-height: 1.4;
  text-decoration: none;
  white-space: nowrap;
}

.sidebar-caption {
  margin: 0;
  color: var(--sidebar-muted);
  font-size: 11px;
  line-height: 1.4;
  letter-spacing: 0.02em;
}

.sidebar-navigation {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 24px;
}

.sidebar-link {
  display: flex;
  align-items: center;
  box-sizing: border-box;
  min-height: 44px;
  padding: 12px;
  color: var(--sidebar-ink);
  font-size: 14px;
  line-height: 1.4;
  text-decoration: none;
  overflow-wrap: anywhere;
  transition: background-color 150ms ease, color 150ms ease;
}

.sidebar-link:hover {
  background: #f7f5f1;
  color: var(--sidebar-accent);
}

.sidebar-link.is-active {
  background: var(--sidebar-soft);
  color: var(--sidebar-accent);
}

.sidebar-footer {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 16px;
}

.sidebar-badge {
  padding: 8px;
  border-radius: 6px;
  background: var(--sidebar-soft);
  color: var(--sidebar-accent);
  font-size: 12px;
  line-height: 1.4;
}

.sidebar-footer p {
  margin: 0;
  color: var(--sidebar-muted);
  font-size: 12px;
  line-height: 1.4;
}

.sidebar-toggle,
.sidebar-close {
  display: none;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  padding: 0;
  border: 1px solid #e5e6df;
  border-radius: 6px;
  background: #fff;
  color: #272b28;
  font-size: 24px;
  cursor: pointer;
}

.sidebar-backdrop {
  position: fixed;
  inset: 0;
  z-index: 1040;
  background: rgb(25 32 28 / 38%);
}

.sidebar-link:focus-visible,
.sidebar-brand:focus-visible,
.sidebar-toggle:focus-visible,
.sidebar-close:focus-visible {
  outline: 2px solid #b94729;
  outline-offset: 3px;
}

@media (max-width: 991.98px) {
  .sidebar-toggle {
    position: fixed;
    top: 16px;
    left: 16px;
    z-index: 1030;
    display: flex;
  }

  .sidebar-close {
    display: flex;
    flex-shrink: 0;
  }

  .dashboard-sidebar {
    width: min(300px, calc(100vw - 48px));
    visibility: hidden;
    transform: translateX(-100%);
    transition: transform 200ms ease, visibility 200ms ease;
  }

  .dashboard-sidebar.is-open {
    visibility: visible;
    transform: translateX(0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .dashboard-sidebar,
  .sidebar-link {
    transition: none;
  }
}
</style>