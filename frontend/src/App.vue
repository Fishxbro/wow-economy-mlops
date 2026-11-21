<template>
    <component :is="layout">
        <router-view />
    </component>
</template>

<script setup>
    import { computed } from 'vue'
    import { useRoute } from 'vue-router'

    const route = useRoute()
    const layout = computed(() => route.meta.layout || 'TDefault')
</script>

<style>
    @font-face {
        font-family: 'Londrina-Regular';
        src: url('./assets/fonts/Londrina_Solid/LondrinaSolid-Regular.ttf') format('truetype');
        font-style: normal;
        font-weight: 400;
        font-display: swap;
    }

    body {
        background-color: #0C1013 !important;
        font-family: 'Nunito-Regular', sans-serif;
    }
</style>
