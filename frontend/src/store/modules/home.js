import { missing_dates, sales_demo } from '../../data/demo.js'

export default {
    namespaced: true,
    state: () => ({ rows: sales_demo, missing_dates }),
    getters: {
        getRows: (state) => state.rows,
        getMissingDates: (state) => state.missing_dates,
    },
    mutations: {
        setRows: (state, payload) => {
            state.rows = payload
        },
    },
    actions: {
        // FastAPI aún no expone ventas. Este módulo conserva el extracto ilustrativo.
        list({ getters }) {
            return getters.getRows
        },
    },
}
