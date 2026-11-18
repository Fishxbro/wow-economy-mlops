import { createApp } from 'vue'
import App from 'SRC/App.vue'
import router from 'SRC/router'
import store from 'SRC/store'
import Vue3Toastify from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'


// Global Styles
import 'ASSETS/scss/main.scss'

import 'bootstrap/dist/js/bootstrap.bundle.min.js'

// Imports 
import {
	templates,
    components,
} from 'SRC/plugins'


// Create App
const app = createApp(App)

// Router
app.use(router)
	
// Store
app.use(store)

// Templates
app.use(templates)

// Components
app.use(components)

// Libs

app.use(Vue3Toastify, {
    position: 'top-right',
    autoClose: 4000,
    closeOnClick: true,
    pauseOnHover: true,
    pauseOnFocusLoss: true,
    hideProgressBar: false,
    newestOnTop: true,
    clearOnUrlChange: false,
    theme: 'auto',
    limit: 5,
})


// Mount
app.mount('#app')
