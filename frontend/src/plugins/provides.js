export function registerProvides(app, utilities = {}) {
    Object.entries(utilities).forEach(([name, utility]) => {
        app.provide(name, utility)
    })
}
