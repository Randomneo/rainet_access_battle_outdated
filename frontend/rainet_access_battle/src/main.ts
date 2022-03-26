import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app_id = createApp(App)

app_id.use(router)

app_id.mount('#app_id')
