import router from "./router.js"
import Navbar from "./components/navbar.js"




new Vue ({
    el: '#app',
    template: `<div>
    <Navbar />
    <router-view class="m-3"/></div>`,
    router,
    components: {
        Navbar,
      },
    data: {
        message: 'Hello Vue!'
    }
})