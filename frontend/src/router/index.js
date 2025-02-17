import VueRouter from "vue-router"
import WebAppHome from '@/components/WebAppHome.vue'
import Sis from '@/components/Sis.vue'

export default new VueRouter({
    routes: [
        {
            path: '/humaine',
            name: 'WebAppHome',
            component: WebAppHome
        },
        {
            path: '/humaine/sis',
            name: 'Sis',
            component: Sis
        }
    ],
    mode: 'history'
})