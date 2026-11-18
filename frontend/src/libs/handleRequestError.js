export default function handleRequestError({ response, commit, dispatch, module_name }) {
    if (!response.success) {
        commit(`${module_name}/setError`, response.error, { root: true })
        dispatch('showAlert', response.error, { root: true })
    }

    dispatch('hideLoading', null, { root: true })
    return response.success
}
