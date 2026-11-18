// Local
import { 
    BackendStatus, 
    Header,
    InputCustom,
    Sidebar,
} from 'COMPONENTS/index.js'


// FontAwesome
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import { fas } from '@fortawesome/free-solid-svg-icons'
import { faFacebook, faFacebookF, faInstagram, faYoutube, faXTwitter, faWhatsapp, faTiktok } from '@fortawesome/free-brands-svg-icons'

library.add(fas,
    faFacebook, faFacebookF, faInstagram, faYoutube, faXTwitter, faWhatsapp, faTiktok
)


// Carousel
// import 'vue3-carousel/carousel.css'
// import { Carousel, Slide, Pagination, Navigation } from 'vue3-carousel'


export default (app) => {
    app.component('mn-backend-status', BackendStatus)
    app.component('mn-header', Header)
    app.component('mn-input-custom', InputCustom)
    app.component('mn-sidebar', Sidebar)
    
    app.component('fa-icon', FontAwesomeIcon)

    // app.component('Carousel', Carousel)
    // app.component('Slide', Slide)
    // app.component('Pagination', Pagination)
    // app.component('Navigation', Navigation)
}
