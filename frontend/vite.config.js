import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const aliasPaths = {
    SRC: './src',
    TEMPLATES: './src/templates',
    VIEWS: './src/views',
    COMPONENTS: './src/components',
    ASSETS: './src/assets',
    ROUTER: './src/router',
    STORE: './src/store',
    PLUGINS: './src/plugins',
    LIBS: './src/libs',
}

export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: Object.fromEntries(
            Object.entries(aliasPaths).map(([name, path]) => [
                name,
                fileURLToPath(new URL(path, import.meta.url)),
            ]),
        ),
    },
    css: {
        preprocessorOptions: {
            scss: {
                additionalData: (source, filename) =>
                    filename.includes('/src/assets/scss/')
                        ? source
                        : `@use 'ASSETS/scss/index.scss' as *;\n${source}`,
            },
        },
    },
})
