<template>
    <nav
        class="site-header navbar navbar-expand-lg"
        aria-label="Navegación principal"
    >
        <div class="container-fluid header-inner px-4 px-xl-5">
            <router-link
                class="navbar-brand d-inline-flex align-items-center gap-3"
                to="/"
                aria-label="Azeroth Exchange, inicio"
            >
                <span
                    class="brand-mark"
                    aria-hidden="true"
                >
                    <img
                        :src="logo"
                        alt=""
                        class="brand-mark-outer"
                    >
                    <img
                        :src="logoDetail"
                        alt=""
                        class="brand-mark-inner"
                    >
                </span>
                <span class="brand-copy d-flex flex-column">
                    <span class="brand-title">AZEROTH</span>
                    <span class="brand-subtitle">EXCHANGE</span>
                </span>
            </router-link>

            <button
                class="navbar-toggler"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#headerNavigation"
                aria-controls="headerNavigation"
                aria-expanded="false"
                aria-label="Abrir menú"
            >
                <span class="navbar-toggler-icon" />
            </button>

            <div
                id="headerNavigation"
                class="collapse navbar-collapse"
            >
                <ul class="navbar-nav header-links mx-lg-auto align-items-lg-center">
                    <li class="nav-item">
                        <router-link
                            class="nav-link"
                            to="/"
                            active-class="active"
                        >Mercado</router-link>
                    </li>
                    <li class="nav-item">
                        <a
                            class="nav-link"
                            href="#tendencias"
                        >Tendencias</a>
                    </li>
                    <li class="nav-item">
                        <a
                            class="nav-link"
                            href="#herramientas"
                        >Herramientas</a>
                    </li>
                    <li class="nav-item">
                        <a
                            class="nav-link"
                            href="#guias"
                        >Guías</a>
                    </li>
                </ul>

                <div class="header-actions d-flex flex-column flex-lg-row align-items-start align-items-lg-center gap-3 gap-lg-5">
                    <span class="locale-label">ES / USD <span
                        class="locale-caret"
                        aria-hidden="true"
                    >▾</span></span>
                    <button
                        class="btn login-button"
                        type="button"
                        @click="router.push('/login')"
                    >
                        Entrar con Battle.net
                    </button>
                </div>
            </div>
        </div>
    </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
import logo from 'ASSETS/images/logo.svg'
import logoDetail from 'ASSETS/images/logo_2.svg'

defineOptions({ name: 'MnHeader' })

const router = useRouter()
</script>

<style lang="scss" scoped>
    .site-header {
        min-height: 94px;
        background: #0d1115;
        border-bottom: 1px solid #272b2e;
        font-family: 'Nunito-Regular', sans-serif;
    }

    .header-inner {
        max-width: 1536px;
    }

    .navbar-brand {
        flex-shrink: 0;
        margin: 0;
        color: #e6dfd0 !important;
    }

    .brand-mark {
        position: relative;
        display: block;
        width: 40px;
        height: 35px;
        flex-shrink: 0;
    }

    .brand-mark-outer {
        width: 40px;
        height: 35px;
    }

    .brand-mark-inner {
        position: absolute;
        top: 8px;
        left: 12px;
        width: 16px;
        height: 14px;
    }

    .brand-copy {
        line-height: 1;
    }

    .brand-title {
        font-size: 19px;
        font-weight: 900;
        letter-spacing: -.03em;
    }

    .brand-subtitle {
        margin-top: 7px;
        color: #ad9568;
        font-size: 9px;
        letter-spacing: .32em;
    }

    .header-links {
        gap: clamp(1.25rem, 2.5vw, 2.75rem);
    }

    .nav-link {
        color: #999b9f !important;
        font-size: 15px;
        white-space: nowrap;
        transition: color .2s ease;
    }

    .nav-link:hover,
    .nav-link:focus-visible,
    .nav-link.active {
        color: #e4c989 !important;
    }

    .nav-link.active {
        font-weight: 800;
    }

    .header-actions {
        flex-shrink: 0;
    }

    .locale-label {
        color: #85888b;
        font-size: 13px;
        white-space: nowrap;
    }

    .locale-caret {
        font-size: 10px;
    }

    .login-button {
        min-width: 238px;
        min-height: 56px;
        padding: .75rem 1.5rem;
        border: 1px solid #363a3d;
        border-radius: 7px;
        background: #171b1e;
        color: #e5e2dc;
        font-size: 15px;
        font-weight: 800;
        white-space: nowrap;
    }

    .login-button:hover,
    .login-button:focus-visible {
        border-color: #d9b76b;
        background: #202428;
        color: #f1d79b;
    }

    .navbar-toggler {
        border-color: #363a3d;
    }

    .navbar-toggler-icon {
        filter: invert(1);
    }

    @media (max-width: 991.98px) {
        .site-header {
            min-height: 76px;
        }

        .navbar-collapse {
            padding: 1.25rem 0 1.5rem;
        }

        .header-links {
            gap: .25rem;
            margin-bottom: 1rem;
        }

        .nav-link {
            padding: .6rem 0;
        }
    }
</style>
