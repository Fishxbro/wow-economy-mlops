import { createRouter, createWebHistory } from 'vue-router'
import modules from './modules/index.js'

export const routes = [
    ...modules,
    {
        path: '/:pathMatch(.*)*',
        redirect: '/',
    },
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
})

export default router
