import eslint from '@eslint/js'
import pluginVue from 'eslint-plugin-vue'

export default [
    { ignores: ['dist/**', 'node_modules/**'] },
    eslint.configs.recommended,
    ...pluginVue.configs['flat/recommended'],
    {
        files: ['**/*.{js,vue}'],
        rules: {
            'vue/html-indent': ['error', 4],
            'vue/script-indent': ['error', 4, { baseIndent: 0 }],
            'vue/multi-word-component-names': ['error', { ignores: ['Home'] }],
            'vue/component-definition-name-casing': 'off',
        },
    },
]
