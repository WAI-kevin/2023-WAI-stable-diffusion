import { createApp } from 'vue';
import vSelect from 'vue-select';
import { createPinia, PiniaVuePlugin } from 'pinia';
import piniaPluginPersist from 'pinia-plugin-persist';
import 'vuetify/styles';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

import App from './App.vue';
import router from './router';

import '@/assets/css/component.css';
import '@/assets/css/modal.css';
import '@/assets/css/reset.css';
import '@/assets/css/menu.css';
import '@/assets/css/basic.css';
import '@/assets/css/page.css';
import '@/assets/css/layout.css';
import 'vue-select/dist/vue-select.css';
import '@mdi/font/css/materialdesignicons.css';
import '@fortawesome/fontawesome-free/css/all.css';

// If you don't need the styles, do not connect
const Vue3 = createApp(App);

export const pinia = createPinia(); // 삭제 금지, router에서 사용
pinia.use(piniaPluginPersist);

const vuetify = createVuetify({
  components,
  directives,
});

Vue3.use(router).use(pinia).use(PiniaVuePlugin).use(vuetify);
Vue3.config.productionTip = false;
Vue3.component('v-select', vSelect);

import GlobalComponents from './globalComponents';

Object.entries(GlobalComponents).forEach(([name, component]) => {
  Vue3.component(name, component);
});

/* eslint-disable no-new */
Vue3.mount('#app');
