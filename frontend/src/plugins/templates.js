import TDefault from 'TEMPLATES/TDefault.vue'
import TLogin from 'TEMPLATES/TLogin.vue'
import TSession from 'TEMPLATES/TSession.vue'

export default (app) => {
    app.component('TDefault', TDefault)
    app.component('TLogin', TLogin)
    app.component('TSession', TSession)
}
