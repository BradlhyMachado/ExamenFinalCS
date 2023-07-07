<template>
  <div class="App">

    <div v-if="user() == 'Administrador'">
      <b-navbar toggleable="lg" type="dark" variant="info">

        <b-navbar-brand href="#">Menú Académico</b-navbar-brand>

        <!-- Toggler del menú -->
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <!-- Menú -->
        <b-collapse is-nav id="nav-collapse">
          <b-navbar-nav>
            <b-nav-item>
              <router-link to="/grupoUsuario" class="nav-link-text">Grupo de Usuarios</router-link>
            </b-nav-item>

            <b-nav-item>
              <router-link to="/profesor" class="nav-link-text">Profesores</router-link>
            </b-nav-item>

            <b-nav-item>
              <router-link to="/estudiante" class="nav-link-text">Estudiantes</router-link>
            </b-nav-item>

            <b-nav-item>
              <router-link to="/curso" class="nav-link-text">Cursos</router-link>
            </b-nav-item>

            <b-nav-item>
              <router-link to="/seccion" class="nav-link-text">Secciones</router-link>
            </b-nav-item>

            <b-nav-item>
              <router-link to="/horario" class="nav-link-text">Horarios</router-link>
            </b-nav-item>
          </b-navbar-nav>
        </b-collapse>

        <!-- Usuario -->
        <b-navbar-nav class="ml-auto">
          <b-nav-item-dropdown :text="username" right>
            <b-dropdown-item @click="logout" class="dropdown-logout">Cerrar sesión</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>

      </b-navbar>
    </div>

    <div v-if="user() == 'Estudiantes'">
      <b-navbar toggleable="lg" type="dark" variant="info">

        <b-navbar-brand href="#">Menú Académico</b-navbar-brand>

        <!-- Toggler del menú -->
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <!-- Menú -->
        <b-collapse is-nav id="nav-collapse">
          <b-navbar-nav>
            <b-nav-item>
              <router-link to="/asistencia" class="nav-link-text">Asistencia</router-link>
            </b-nav-item>
          </b-navbar-nav>
        </b-collapse>

        <!-- Usuario -->
        <b-navbar-nav class="ml-auto">
          <b-nav-item-dropdown :text="username" right>
            <b-dropdown-item @click="logout" class="dropdown-logout">Cerrar sesión</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>

      </b-navbar>
    </div>

    <div v-if="user() == 'Profesores'">
      <b-navbar toggleable="lg" type="dark" variant="info">

        <b-navbar-brand href="#">Menú Académico</b-navbar-brand>

        <!-- Toggler del menú -->
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <!-- Menú -->
        <b-collapse is-nav id="nav-collapse">
          <b-navbar-nav>
            <b-nav-item>
              <router-link to="/participacion" class="nav-link-text">Participación</router-link>
            </b-nav-item>
          </b-navbar-nav>
        </b-collapse>

        <!-- Usuario -->
        <b-navbar-nav class="ml-auto">
          <b-nav-item-dropdown :text="username" right>
            <b-dropdown-item @click="logout" class="dropdown-logout">Cerrar sesión</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>

      </b-navbar>
    </div>

    <router-view></router-view> <!-- Esto se remplaza segun el componente seleccionado en el router-->
    <!-- fin Router -->
  </div>
</template>


<script>
import login from './components/login.vue';
import GrupoUsuarioComponent from './components/GrupoUsuarioComponent.vue';
import ProfesorComponent from './components/ProfesorComponent.vue';
import EstudianteComponent from './components/EstudianteComponent.vue';
import SeccionComponent from './components/SeccionComponent.vue';
import CursoComponent from './components/CursoComponent.vue';
import HorarioComponent from './components/HorarioComponent.vue';
import ParticipacionComponent from './components/ParticipacionComponent.vue';
import AsistenciaComponent from './components/AsistenciaComponent.vue';
export default {
  name: 'App',
  components: {
    login,
    GrupoUsuarioComponent,
    ProfesorComponent,
    EstudianteComponent,
    SeccionComponent,
    CursoComponent,
    HorarioComponent,
    ParticipacionComponent,
    AsistenciaComponent,
  },
  methods: {
    logout() {
      // Eliminar el token almacenado
      localStorage.removeItem('token');
      localStorage.removeItem('usuario');
      localStorage.removeItem('nombre_grupo');

      // Redireccionar al usuario a la página de inicio de sesión
      window.location.href = '/login';
      //this.$router.push('/login');
    },
    user() {
      return localStorage.getItem('nombre_grupo');
    },
    username(){
      return localStorage.getItem('usuario');
    }
  },
  computed: {
    username() {
      return localStorage.getItem('usuario');
    }
  }
}
</script>


<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.App {
  padding: 5px;
}
</style>