# Azeroth

Base mínima de Vue 3, Vite, Vue Router y Vuex.

## Desarrollo

Usa Node 24.15.0 (`nvm use`), instala dependencias con `npm install` y arranca con `npm run dev`.

Comandos: `npm run build`, `npm run lint` y `npm run format`.



## Extensión

- Añade estilos en `src/assets/scss/`. `main.scss` carga Bootstrap; `index.scss` expone variables, mixins y funciones a los estilos SCSS de los componentes.
- Añade utilidades en `src/libs/`.
- Copia componentes en `src/components/` y exporta los globales desde `src/components/index.js` como un objeto. Se registrarán con el prefijo `mn-`.
- Añade layouts en `src/templates/` y regístralos en `src/plugins/templates.js`.
- Añade módulos Vuex en `src/store/modules/` y agrégalos al objeto exportado por su `index.js`.
- Añade archivos de rutas que exporten arrays en `src/router/modules/` y combínalos en su `index.js`. Sus vistas van en `src/views/`.
- Registra utilidades compartidas con `registerProvides` en `src/main.js` para usarlas con `inject`.
