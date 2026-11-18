<template>
    <section :class="[`mn-input-custom text-left mb-${mb}`, { 'input-style-vuetify': style_mode === 'vuetify' }]">
        <!-- Label -->
        <span v-if="label && style_mode !== 'vuetify'" :class="`description-xs text-${variant}`">
            {{ label }}
        </span>

        <div v-if="style_mode === 'vuetify' && type !== 'area'"
            class="vuetify-field"
            :class="{
                'is-filled': hasValue,
                'has-label': Boolean(label),
                'is-empty-date': type === 'date' && !hasValue && Boolean(label),
            }">
            <input :value="input_value"
                :id="_id"
                @input="onInput"
                @change="onChange"
                ref="input_ref"
                class="vuetify-field__input"
                :class="[
                    `theme-${theme} variant-${variant}`,
                    has_icon ? 'padding-icon' : '',
                    type === 'hex' ? 'padding-color-preview' : '',
                    type === 'tel' ? 'padding-tel-prefix' : '',
                    is_pass ? 'input-pass' : '',
                ]"
                :placeholder="placeholder_for_vuetify"
                :minlength="min_length"
                :maxlength="type === 'tel' ? 10 : max_length"
                :type="local_type"
                :inputmode="type === 'tel' ? 'numeric' : null"
                :autocomplete="type === 'tel' ? 'tel' : null"
                :max="max"
                :min="min"
                :disabled="disabled" />

            <label v-if="label" :for="_id" class="vuetify-field__label">
                {{ label }}
            </label>

            <div v-if="type === 'tel'" class="tel-prefix">
                <span class="tel-prefix__flag">🇲🇽</span>
                <span class="tel-prefix__code">+52</span>
            </div>

            <!-- Color Preview Vuetify para tipo 'hex' -->
            <div class="div-color-preview" v-if="type === 'hex'">
                <div class="color-preview-box" :style="{ backgroundColor: modelValue || 'transparent' }"></div>
            </div>

            <div :class="`div-icon icon-theme-${theme}`" @click="showPassword()" v-if="has_icon">
                <div class="div-icon--image">
                    <fa-icon :icon="icon" class="fa-md" />
                </div>
            </div>
        </div>

        <div v-else-if="style_mode === 'vuetify' && type === 'area'"
            class="vuetify-field vuetify-field--area"
            :class="{ 'is-filled': hasValue, 'has-label': Boolean(label) }">
            <textarea :value="modelValue"
                @input="onInput"
                @change="onChange"
                ref="input_ref"
                class="vuetify-field__input"
                :class="[`theme-${theme} variant-${variant}`]"
                :rows="rows"
                :placeholder="placeholder_for_vuetify"></textarea>

            <label v-if="label" :for="_id" class="vuetify-field__label">
                {{ label }}
            </label>
        </div>

        <!-- Input -->
        <template v-else>
            <div class="div-input flex-start-center" v-if="type !== 'area'">
                <input :value="input_value"
                    :id="_id"
                    @input="onInput"
                    @change="onChange"
                    ref="input_ref"
                    :class="`theme-${theme} variant-${variant}
                        ${has_icon ? 'padding-icon' : ''} 
                        ${type === 'hex' ? 'padding-color-preview' : ''}
                        ${type === 'tel' ? 'padding-tel-prefix' : ''}
                        ${is_pass ? 'input-pass' : ''}`"
                    :placeholder="placeholder"
                    :minlength="min_length"
                    :maxlength="type === 'tel' ? 10 : max_length"
                    :type="local_type"
                    :inputmode="type === 'tel' ? 'numeric' : null"
                    :autocomplete="type === 'tel' ? 'tel' : null"
                    :max="max"
                    :min="min"
                    :disabled="disabled" />

                <div v-if="type === 'tel'" class="tel-prefix">
                    <span class="tel-prefix__flag">🇲🇽</span>
                    <span class="tel-prefix__code">+52</span>
                </div>

                <!-- Color Preview Default para tipo 'hex' -->
                <div class="div-color-preview" v-if="type === 'hex'">
                    <div class="color-preview-box" :style="{ backgroundColor: modelValue || 'transparent' }"></div>
                </div>

                <div :class="`div-icon icon-theme-${theme}`" @click="showPassword()" v-if="has_icon">
                    <div class="div-icon--image">
                        <fa-icon :icon="icon" class="fa-md" />
                    </div>
                </div>
            </div>

            <div class="div-area" v-else>
                <textarea :value="modelValue"
                    @input="onInput"
                    @change="onChange"
                    ref="input_ref"
                    :class="`theme-${theme} variant-${variant}`"
                    :rows="rows">
                </textarea>
            </div>
        </template>

        <!-- Min Length -->
        <div class="text-end" v-if="min_length">
            <small class="description-xxs">
                Longuitud minima: {{ modelValue ? modelValue.length : 0 }}/{{ min_length }}
            </small>
        </div>

        <!-- Error Label -->
        <div class="text-start" v-if="error_label !== null && error_label !== ''">
            <span class="error-label">
                {{ error_label }}
            </span>
        </div>
    </section>
</template>

<script setup>
    import { ref, computed, watch, onMounted } from 'vue'

    // Props
    const props = defineProps({
        modelValue: {
            required: false,
            type: [String, Number, Date, null],
            default: () => {
                return null
            },
        },
        _id: {
            type: String,
            default: () => `input-${Math.random().toString(36).slice(2, 9)}`,
        },
        type: {
            type: String,
            required: false,
            default: 'text',
            validator: function (value) {
                return [
                    'text',
                    'number',
                    'float',
                    'price',
                    'password',
                    'search',
                    'date',
                    'time',
                    'datetime-local',
                    'hour',
                    'email',
                    'tel',
                    'color',
                    'hex',
                    'area',
                ].includes(value)
            },
        },
        number_value: {
            type: Boolean,
            required: false,
            default: false,
        },
        theme: {
            type: String,
            require: false,
            default: 'white',
            validator: function (value) {
                return ['white', 'dark'].includes(value)
            },
        },
        variant: {
            type: String,
            require: false,
            default: 'bootstrap',
            validator: function (value) {
                return [
                    'transparent',
                    'white',
                    'primary',
                    'secondary',
                    'success',
                    'info',
                    'warning',
                    'danger',
                    'light',
                    'dark',
                    'bootstrap',
                ].includes(value)
            },
        },
        style_mode: {
            type: String,
            required: false,
            default: 'default',
            validator: function (value) {
                return ['default', 'vuetify'].includes(value)
            },
        },
        currency: {
            type: String,
            required: false,
            default: 'MXN',
        },
        price_decimal: {
            type: Number,
            required: false,
            default: 2,
        },
        label: {
            type: String,
            required: false,
            default: '',
        },
        placeholder: {
            required: false,
            type: String,
            default: '',
        },
        min_length: {
            required: false,
            type: Number,
            default: null,
        },
        max_length: {
            required: false,
            type: Number,
            default: null,
        },
        max: {
            required: false,
            type: [Number, String],
            default: null,
        },
        min: {
            required: false,
            type: [Number, String],
            default: null,
        },
        error_label: {
            require: false,
            type: String,
            default: '',
        },
        disabled: {
            require: false,
            type: Boolean,
            default: false,
        },
        mb: {
            require: false,
            type: [Number, String],
            default: '3',
        },
        rows: {
            require: false,
            type: [Number, String],
            default: '2',
        },
    })

    // Emits
    const emits = defineEmits(['update:modelValue', 'change'])

    // Computeds
    const is_pass = computed(() => {
        return props.type == 'password'
    })
    const has_icon = computed(() => {
        return props.type == 'password' || props.type == 'search'
    })
    const icon = computed(() => {
        return props.type == 'search'
            ? 'search'
            : props.type == 'password'
                ? local_type.value == 'password'
                    ? 'eye'
                    : 'eye-slash'
                : null
    })
    const hasValue = computed(() => {
        if(props.type === 'tel') {
            return get_national_phone(props.modelValue).length > 0
        }
        return props.modelValue !== null && props.modelValue !== undefined && String(props.modelValue).length > 0
    })
    const placeholder_for_vuetify = computed(() => {
        return props.placeholder === '' ? ' ' : props.placeholder
    })
    const input_value = computed(() => {
        if(props.type === 'price') {
            return price_value.value
        }
        if(props.type === 'tel') {
            return tel_value.value
        }
        return props.modelValue
    })

    // Refs
    const input_ref = ref(null)

    // Variables
    let local_type = ref(null)
    const price_value = ref('')
    const tel_value = ref('')

    // Methods
    const normalizeNumber = (value) => {
        value = value.replace(/[^0-9.-]/g, '')
        value = value.replace(/(?!^)-/g, '')
        const parts = value.split('.')
        if(parts.length > 2) {
            value = parts.shift() + '.' + parts.join('')
        }
        return value
    }

    const normalizePriceLive = (value) => {
        value = value.replace(/[^0-9.]/g, '')
        if(!value) {
            return ''
        }
        const parts = value.split('.')
        const integerPart = parts[0]
        const decimalPart = parts[1] ?? null
        const formattedInteger = integerPart.replace(/^0+(?!$)/, '').replace(/\B(?=(\d{3})+(?!\d))/g, ',')
        let formattedDecimal = ''
        if(decimalPart !== null) {
            formattedDecimal = '.' + decimalPart.slice(0, props.price_decimal)
        }
        return `$${formattedInteger}${formattedDecimal}`
    }

    const get_national_phone = (value) => {
        const digits = String(value ?? '').replace(/\D/g, '')
        const phone = digits.length === 12 && digits.startsWith('52') ? digits.slice(2) : digits

        return phone.slice(0, 10)
    }

    const build_full_phone = (value) => {
        const national_phone = get_national_phone(value)
        return national_phone ? `52${national_phone}` : ''
    }

    const showPassword = () => {
        if(props.type === 'password') {
            local_type.value = local_type.value === 'password' ? 'text' : 'password'
        }
    }

    const normalizeInputValue = (event) => {
        let value = event.target.value

        if(props.type === 'number') {
            value = value.replace(/[^0-9]/g, '')
            event.target.value = value
            return props.number_value && value !== '' ? Number(value) : value
        }

        if(props.type === 'float') {
            value = normalizeNumber(value)
            event.target.value = value
            return value
        }

        if(props.type === 'price') {
            let raw = value.replace(/[^0-9.]/g, '')
            const parts = raw.split('.')
            if(parts.length > 2) {
                raw = parts.shift() + '.' + parts.join('')
            }
            if(parts[1]) {
                raw = `${parts[0]}.${parts[1].slice(0, props.price_decimal)}`
            }
            const formatted = normalizePriceLive(raw)
            event.target.value = formatted
            price_value.value = formatted
            return raw
        }

        if(props.type === 'tel') {
            const national_phone = get_national_phone(value)
            tel_value.value = national_phone
            event.target.value = national_phone
            return build_full_phone(national_phone)
        }

        return value
    }

    const onInput = (event) => {
        const value = normalizeInputValue(event)

        emits('update:modelValue', value === '' ? null : value)
    }

    const onChange = (event) => {
        emits('change', normalizeInputValue(event))
    }

    const focus = () => {
        input_ref.value?.focus()
    }

    defineExpose({
        focus,
    })

    // Watchers
    watch(
        () => props.modelValue,
        (val) => {
            if(props.type === 'price') {
                price_value.value = normalizePriceLive(String(val ?? ''))
            }
            if(props.type === 'tel' && String(val ?? '') !== build_full_phone(tel_value.value)) {
                tel_value.value = get_national_phone(val)
            }
        },
        { immediate: true },
    )

    // Vue Cyclelife
    onMounted(() => {
        let local_types_text = ['search', 'number', 'float', 'price', 'hex']
        local_type.value = !local_types_text.includes(props.type) ? props.type : 'text'
    })
</script>

<style lang="scss" scoped>
    $themes: (
        'white': white,
        'dark': #00000080,
    );

    $variants: (
        'primary': var(--bs-primary),
        'secondary': var(--bs-secondary),
        'success': var(--bs-success),
        'info': var(--bs-info),
        'warning': var(--bs-warning),
        'danger': var(--bs-danger),
        'light': var(--bs-light),
        'dark': var(--bs-dark),
        'bootstrap': var(--bs-border-color),
    );

    .mn-input-custom {
        position: relative;
        text-align: left;
        width: 100%;

        .vuetify-field {
            position: relative;
            width: 100%;

            > .div-icon {
                position: absolute;
                top: 50%;
                right: 10px;
                width: auto;
                transform: translateY(-50%);

                .div-icon--image {
                    margin-left: 0;
                }
            }

            &__input {
                width: 100%;
                height: 56px;
                border: 1px solid rgba(60, 60, 67, 0.38);
                border-radius: 4px;
                padding: 18px 14px 6px;
                font-size: 16px;
                outline: none;
                background: #fff;
                color: #1f1f1f;
                transition:
                    border-color 0.18s ease,
                    box-shadow 0.18s ease;

                &::placeholder {
                    transition: opacity 0.18s ease;
                }

                &:focus {
                    border-color: #1976d2;
                    box-shadow: 0 0 0 1px #1976d2;
                }
            }

            &__label {
                position: absolute;
                left: 14px;
                top: 16px;
                font-size: 16px;
                color: rgba(60, 60, 67, 0.6);
                background: #fff;
                padding: 1px 4px;
                pointer-events: none;
                transition:
                    transform 0.18s ease,
                    top 0.18s ease,
                    font-size 0.18s ease,
                    color 0.18s ease;
                transform-origin: left top;
            }

            &:focus-within {
                .vuetify-field__input::placeholder {
                    opacity: 0.5;
                }

                .vuetify-field__label {
                    top: -8px;
                    font-size: 12px;
                    color: #1976d2;
                }
            }

            &.is-filled {
                .vuetify-field__label {
                    top: -8px;
                    font-size: 12px;
                    color: rgba(60, 60, 67, 0.6);
                }
            }

            &.has-label:not(:focus-within) {
                .vuetify-field__input::placeholder {
                    opacity: 0;
                }
            }

            &.is-empty-date:not(:focus-within) {
                .vuetify-field__label {
                    top: 1px;
                    left: 1px;
                    width: calc(100% - 48px);
                    height: calc(100% - 2px);
                    display: flex;
                    align-items: center;
                    padding: 0 17px;
                    box-sizing: border-box;
                    z-index: 1;
                }
            }
        }

        .vuetify-field--area {
            .vuetify-field__input {
                min-height: 96px;
                padding-top: 24px;
                resize: vertical;
            }
        }

        .div-input {
            position: relative;
            width: 100%;
        }

        input {
            height: 40px;
        }

        textarea {
            height: auto !important;
        }

        input,
        textarea {
            display: block;
            width: 100%;
            padding: 0.375rem 0.75rem;
            border-radius: var(--bs-border-radius);
            font-weight: 400;
            appearance: none;

            &::placeholder {
                font-family: Poppins-regular;
                font-weight: 600;
                font-size: 16px;
                opacity: 0.5;
            }
        }

        // Padding for input icon
        .padding-icon {
            padding: 6px 36px 6px 12px !important;
        }

        // Padding for Color preview
        .padding-color-preview {
            padding-right: 42px !important;
        }

        .padding-tel-prefix {
            padding-left: 92px !important;
        }

        .vuetify-field__input.padding-tel-prefix {
            padding: 18px 14px 6px 92px !important;
        }

        .tel-prefix {
            position: absolute;
            left: 12px;
            top: 50%;
            transform: translateY(-50%);
            display: flex;
            align-items: center;
            gap: 6px;
            color: #1f1f1f;
            font-size: 14px;
            pointer-events: none;
            z-index: 1;

            &__flag {
                font-size: 15px;
                line-height: 1;
            }

            &__code {
                font-weight: 600;
            }
        }

        .input-pass {
            &:invalid {
                border: 1px solid var(--bs-danger);
            }
            &:invalid:focus {
                border: 1px solid var(--bs-danger);
                box-shadow: 0 0 8px 1px var(--bs-danger) !important;
                background: linear-gradient(180deg, rgba(255, 255, 255, 1) 0%, rgba(232, 172, 172, 1) 100%);
            }
        }

        // Input Themes
        @each $theme, $color in $themes {
            $label-color: #ffffff;
            @if $theme == 'white' {
                $label-color: #000000;
            }

            .theme-#{$theme} {
                background-color: $color;
                color: $label-color !important;

                &::placeholder {
                    color: $label-color !important;
                }
            }

            .icon-theme-#{$theme} {
                color: $label-color !important;
            }
        }

        // Input Variants
        @each $variant, $color in $variants {
            .variant-#{$variant} {
                border: 1px solid $color;

                &:focus-visible {
                    outline: none;
                    border: 1px solid $color !important;
                    box-shadow: 0 0 8px 1px $color !important;
                }
            }
        }

        // Icon
        .div-icon {
            cursor: pointer;
            opacity: 0.5;
            width: 0px;

            &--image {
                display: flex;
                justify-content: center;
                align-items: center;
                margin-left: -34px;
                padding: 6px;
            }
        }

        // Color Preview (Solo para type 'hex')
        .div-color-preview {
            position: absolute;
            right: 12px;
            top: 50%;
            transform: translateY(-50%);
            display: flex;
            align-items: center;
            justify-content: center;
            pointer-events: none;

            .color-preview-box {
                width: 22px;
                height: 22px;
                border-radius: 4px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background-color: transparent;
                box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.05);
            }
        }
    }

    .error_label {
        color: #ff4539;
        font-size: 14px;
    }

    input:-webkit-autofill,
    input:-webkit-autofill:hover,
    input:-webkit-autofill:focus,
    input:-webkit-autofill:active {
        transition: background-color 9999s ease-in-out 0s;
        -webkit-text-fill-color: #1c355e;
        caret-color: #1c355e;
    }
</style>
