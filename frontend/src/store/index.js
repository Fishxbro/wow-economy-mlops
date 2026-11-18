import { createStore } from 'vuex'
import modules from './modules/index.js'

const store = createStore({
    state: () => ({
        loading: false,
        alert: null,
    }),
    getters: {
        getLoading: (state) => state.loading,
        getAlert: (state) => state.alert,
    },
    mutations: {
        setLoading(state, value) {
            state.loading = value
        },
        setAlert(state, value) {
            state.alert = value
        },
    },
    actions: {
        showLoading({ commit }) {
            commit('setLoading', true)
        },
        hideLoading({ commit }) {
            commit('setLoading', false)
        },
        showAlert({ commit }, alert) {
            commit('setAlert', alert)
        },
        clearAlert({ commit }) {
            commit('setAlert', null)
        },
    },
    modules,
})

export default store
