export default [
    {
        path: '/',
        alias: '/Home',
        name: 'home',
        component: () => import('VIEWS/Home.vue'),
        meta: { layout: 'TDefault' },
    },
]
