// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import VueResource from 'vue-resource'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import VueSweetalert2 from 'vue-sweetalert2';

import 'sweetalert2/dist/sweetalert2.min.css';
Vue.use(VueSweetalert2);

// para peticiones
Vue.use(VueResource);

// para navegacion
import VueRouter from 'vue-router'
Vue.use(VueRouter);

// Para el middleware
import {authAdmin, authProfesores, authEstudiantes} from './middlewares/authMiddleware';

// Para tener un router
import login from './components/login.vue';  
import GrupoUsuarioComponent from './components/GrupoUsuarioComponent.vue';
import ProfesorComponent from './components/ProfesorComponent.vue';
import EstudianteComponent from './components/EstudianteComponent.vue';
import SeccionComponent from './components/SeccionComponent.vue';
import CursoComponent from './components/CursoComponent.vue';
import HorarioComponent from './components/HorarioComponent.vue';
import ParticipacionComponent from './components/ParticipacionComponent.vue';
import AsistenciaComponent from './components/AsistenciaComponent.vue';

const router = new VueRouter({
  mode: 'history',
  base: __dirname,
  routes: [
    {
      path: '/login',
      component: login
    },
    {
      path: '/grupoUsuario',
      component: GrupoUsuarioComponent, beforeEnter : authAdmin
    },
    {
      path: '/profesor',
      component: ProfesorComponent, beforeEnter : authAdmin
    },
    {
      path: '/estudiante',
      component: EstudianteComponent, beforeEnter : authAdmin
    },
    {
      path: '/seccion',
      component: SeccionComponent, beforeEnter : authAdmin
    },
    {
      path: '/curso',
      component: CursoComponent, beforeEnter : authAdmin
    },
    {
      path: '/horario',
      component: HorarioComponent,  beforeEnter : authAdmin
    },
    {
      path: '/participacion',
      component: ParticipacionComponent, beforeEnter : authProfesores
    },
    {
      path: '/asistencia',
      component: AsistenciaComponent, beforeEnter : authEstudiantes
    },
  ]
});

// Import Bootstrap and BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue)

// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

Vue.use(VueResource);
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  router,
  el: '#app',
  components: { App },
  template: '<App/>'
}).$mount('#app')