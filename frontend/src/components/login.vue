<template>
  <div class="login">
    <h2>Iniciar sesión</h2>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="correo">Correo electrónico:</label>
        <input type="email" id="correo" v-model="correo" required>
      </div>
      <div class="form-group">
        <label for="contrasena">Contraseña:</label>
        <input type="password" id="contrasena" v-model="contrasena" required>
      </div>
      <button type="submit">Iniciar sesión</button>
    </form>
  </div>
</template>
  
<script>
import axios from 'axios';
import Swal from 'sweetalert2'
export default {
  name: 'Login',
  data() {
    return {
      correo: '',
      contrasena: '',
    };
  },
  methods: {
    login() {
      const data = {
        usuario_correo: this.correo,
        usuario_contrasena: this.contrasena,
      };

      axios
        .post('http://127.0.0.1:5000/login', data)
        .then((res) => {
          console.log(res.data);
          if (res.data['estado']) {
            Swal.fire({
              title: 'Éxito',
              text: 'El inicio de sesión fue exitoso!!!',
              icon: 'success',
            });
            // Almacenar el token en el Local Storage
            localStorage.setItem('token', res.data['token']);
            // Almacenar el nombre del usuario
            localStorage.setItem('usuario', res.data['usuario']);
            // Almacenar el dni del usuario
            localStorage.setItem('dni', res.data['dni']);
            // Almacenar el nombre del grupo del usuario
            localStorage.setItem('nombre_grupo', res.data['nombre_grupo']);
            // Redirección usando Vue Router
            this.$router.push('/');
          } else {
            Swal.fire({
              title: 'Error',
              text: 'La contraseña o correo son incorrectos',
              icon: 'error',
            });
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>


<style scoped>
.login {
  max-width: 400px;
  margin: 0 auto;
}
.form-group {
  margin-bottom: 20px;
}
label {
  display: block;
  margin-bottom: 5px;
}
input[type="email"],
input[type="password"] {
  width: 100%;
  padding: 10px;
  font-size: 16px;
}
button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  cursor: pointer;
}
</style>