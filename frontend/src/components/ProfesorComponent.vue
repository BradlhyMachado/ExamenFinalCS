<template>
  <div class="Profesores">
    <h2>Profesores</h2>

    <!-- Botón para abrir el modal de creación -->
    <div class="d-flex justify-content-start">
      <b-button @click="showCreateModal" variant="primary">Crear Profesor</b-button>
    </div>

    <!-- Modal de creación de profesor -->
    <b-modal v-model="createModalVisible" title="Crear Profesor" hide-footer hide-header-close>
      <b-form @submit.prevent="createProfesor" class="mb-3">
        <b-form-group label="DNI" label-for="dniInput">
          <b-form-input id="dniInput" v-model="newProfesor.usuario_dni" placeholder="DNI" required maxlength="8"
            pattern="[0-9]{8}" title="El DNI debe tener 8 dígitos"></b-form-input>
        </b-form-group>
        <b-form-group label="Nombre" label-for="nombreInput">
          <b-form-input id="nombreInput" v-model="newProfesor.usuario_nombre" placeholder="Nombre" required
            pattern="[a-zA-Z]+" title="El nombre solo se permiten letras"></b-form-input>
        </b-form-group>
        <b-form-group label="Apellido" label-for="apellidoInput">
          <b-form-input id="apellidoInput" v-model="newProfesor.usuario_apellido" placeholder="Apellido" required
            pattern="[a-zA-Z]+" title="El apellido solo se permiten letras"></b-form-input>
        </b-form-group>
        <b-form-group label="Teléfono" label-for="telefonoInput">
          <b-form-input id="telefonoInput" v-model="newProfesor.usuario_telefono" placeholder="Teléfono" required
            maxlength="9" pattern="[0-9]{9}" title="El teléfono debe tener 9 dígitos"></b-form-input>
        </b-form-group>
        <b-form-group label="Correo" label-for="correoInput">
          <b-form-input id="correoInput" v-model="newProfesor.usuario_correo" placeholder="Correo" required
            pattern="^[^\s@]+@[^\s@]+\.[^\s@]+$" title="Ingrese un correo electrónico válido"></b-form-input>
        </b-form-group>
        <b-form-group label="Contraseña" label-for="contraseñaInput">
          <b-form-input id="contraseñaInput" v-model="newProfesor.usuario_contraseña" placeholder="Contraseña"
            type="password" required minlength="8"></b-form-input>
        </b-form-group>
        <b-form-group label="Foto" label-for="rutaInput">
          <input id="rutaInput" type="file" @change="handleFileChange">
        </b-form-group>

        <div class="d-flex justify-content-end mt-3">
          <div class="mr-2">
            <b-button type="submit" variant="primary">Crear</b-button>
          </div>
          <div>
            <b-button @click="cancelCreate" variant="secondary">Cancelar</b-button>
          </div>
        </div>

      </b-form>
    </b-modal>

    <!-- Modal de edición de profesor -->
    <b-modal v-if="editingProfesor" v-model="editModalVisible" title="Editar Profesor" hide-footer hide-header-close>
      <b-form @submit.prevent="updateProfesor(editingProfesor)" class="mb-3">
        <b-form-group label="DNI" label-for="profesor_dni">
          <b-form-input id="profesor_dni" v-model="editingProfesor.profesor_dni" placeholder="DNI"
            readonly></b-form-input>
        </b-form-group>
        <b-form-group label="Nombre" label-for="nombre">
          <b-form-input id="nombre" v-model="editingProfesor.nombre" placeholder="Nombre" required pattern="[a-zA-Z]+"
            title="El nombre solo se permiten letras"></b-form-input>
        </b-form-group>
        <b-form-group label="Apellido" label-for="apellidos">
          <b-form-input id="apellidos" v-model="editingProfesor.apellidos" placeholder="Apellido" required
            pattern="[a-zA-Z]+" title="El apellido solo se permiten letras"></b-form-input>
        </b-form-group>
        <b-form-group label="Teléfono" label-for="telefonoInput">
          <b-form-input id="telefonoInput" v-model="editingProfesor.telefono" placeholder="Teléfono" required
            maxlength="9" pattern="[0-9]{9}" title="El teléfono debe tener 9 dígitos"></b-form-input>
        </b-form-group>
        <b-form-group label="Correo" label-for="correoInput">
          <b-form-input id="correoInput" v-model="editingProfesor.correo" placeholder="Correo" required
            pattern="^[^\s@]+@[^\s@]+\.[^\s@]+$" title="Ingrese un correo electrónico válido"></b-form-input>
        </b-form-group>
        <b-form-group label="Foto" label-for="rutaInput">
          <b-form-input id="rutaInput" v-model="editingProfesor.ruta" placeholder="Foto" required></b-form-input>
        </b-form-group>
        <div class="d-flex justify-content-end mt-3">
          <div class="mr-2">
            <b-button type="submit" variant="primary">Actualizar</b-button>
          </div>
          <div>
            <b-button @click="cancelEdit" variant="secondary">Cancelar</b-button>
          </div>
        </div>
      </b-form>
    </b-modal>

    <!-- Modal de confirmación de eliminación -->
    <b-modal v-model="confirmDeleteModalVisible" title="Confirmar Eliminación" hide-footer hide-header-close>
      <p>¿Estás seguro de que deseas eliminar a este profesor?</p>
      <div class="d-flex justify-content-end">
        <div class="mr-2">
          <b-button @click="deleteProfesorConfirmed" variant="danger">Eliminar</b-button>
        </div>
        <div>
          <b-button @click="cancelDelete" variant="secondary">Cancelar</b-button>
        </div>
      </div>
    </b-modal>

    <!-- Tabla de profesores -->
    <b-table :items="paginatedProfesores" :fields="fields" striped hover>
      <template #cell(usuario_dni)="row">
        {{ row.item.usuario_dni }}
      </template>
      <template #cell(usuario_nombre)="row">
        {{ row.item.usuario_nombre }}
      </template>
      <template #cell(usuario_apellidos)="row">
        {{ row.item.usuario_apellido }}
      </template>
      <template #cell(usuario_telefono)="row">
        {{ row.item.usuario_telefono }}
      </template>
      <template #cell(usuario_correo)="row">
        {{ row.item.usuario_correo }}
      </template>
      <template #cell(usuario_ruta)="row">
        {{ row.item.usuario_ruta }}
      </template>
      <template #cell(acción)="row">
        <b-button @click="editProfesor(row.item)" variant="info" size="sm">Editar</b-button>
        <b-button @click="deleteProfesor(row.item)" variant="danger" size="sm">Eliminar</b-button>
      </template>
    </b-table>

    <!-- Contenedor del paginador centrado -->
    <div class="pagination-container">
      <b-pagination v-model="currentPage" :total-rows="profesores.length" :per-page="perPage"></b-pagination>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
export default {
  data() {
    return {
      currentPage: 1,
      perPage: 5,
      profesores: [],
      newProfesor: {
        usuario_dni: '',
        usuario_nombre: '',
        usuario_apellido: '',
        usuario_telefono: '',
        usuario_correo: '',
        usuario_contraseña: '',
        usuario_ruta: '',
      },
      postURL: 'http://127.0.0.1:5000/profesor',
      fields: ['profesor_dni', 'nombre', 'apellidos', 'telefono', 'correo', 'ruta', 'acción'],
      editingProfesor: null,
      createModalVisible: false,
      editModalVisible: false,
      confirmDeleteModalVisible: false,
      deletingProfesor: null,
      token: null,
    };
  },
  methods: {
    handleFileChange(event) {
      const file = event.target.files[0];
      this.uploadFile(file);
    },
    uploadFile(file) {
      const formData = new FormData();
      formData.append('foto', file);
      axios
        .post('http://127.0.0.1:5000/uploadFile', formData)
        .then((res) => {
          let filePath = res.data;
          filePath = filePath.replace(/\\/g, '/'); // Reemplazar todas las barras invertidas por barras diagonales
          this.newProfesor.usuario_ruta = filePath;
          console.log(this.newProfesor.usuario_ruta);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    showCreateModal() {
      this.createModalVisible = true;
    },
    cancelCreate() {
      this.createModalVisible = false;
      this.resetForm();
    },
    createProfesor() {
      axios
        .put(this.postURL, this.newProfesor, {
          headers: {
            Authorization: `Bearer ${this.token}`, // Incluir el token en el encabezado de la solicitud
          },
        })
        .then((res) => {
          this.profesores.push(res.data);
          this.createModalVisible = false;
          this.resetForm();
          this.fetchProfesores();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    showEditModal(profesor) {
      this.editingProfesor = { ...profesor };
      this.editModalVisible = true;
    },
    cancelEdit() {
      this.editModalVisible = false;
      this.editingProfesor = null;
    },
    updateProfesor(profesor) {
      const transformedProfesor = {
        usuario_dni: profesor.profesor_dni,
        usuario_nombre: profesor.nombre,
        usuario_apellido: profesor.apellidos,
        usuario_telefono: profesor.telefono,
        usuario_correo: profesor.correo,
        usuario_contraseña: profesor.contraseña,
        usuario_ruta: profesor.ruta,
      };
      axios
        .patch(this.postURL, transformedProfesor, {
          headers: {
            Authorization: `Bearer ${this.token}`, // Incluir el token en el encabezado de la solicitud
          },
        })
        .then((res) => {
          console.log(res.data);
          this.fetchProfesores();
          this.cancelEdit();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    editProfesor(profesor) {
      this.showEditModal(profesor);
    },
    deleteProfesor(profesor) {
      this.deletingProfesor = profesor;
      this.confirmDeleteModalVisible = true;
    },
    deleteProfesorConfirmed() {
      axios
        .delete(this.postURL, { data: { dni: this.deletingProfesor.profesor_dni },
          headers: {
            Authorization: `Bearer ${this.token}`, // Incluir el token en el encabezado de la solicitud
          },
        })
        .then((res) => {
          console.log(res.data);
          this.fetchProfesores();
          this.cancelDelete();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    cancelDelete() {
      this.confirmDeleteModalVisible = false;
      this.deletingProfesor = null;
    },
    fetchProfesores() {
      axios
        .post(this.postURL + 's', null, {
          headers: {
            Authorization: `Bearer ${this.token}`, // Incluir el token en el encabezado de la solicitud
          },
        })
        .then((res) => {
          console.log(res);
          this.profesores = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    resetForm() {
      this.newProfesor = {
        usuario_dni: '',
        usuario_nombre: '',
        usuario_apellido: '',
        usuario_telefono: '',
        usuario_correo: '',
        usuario_contraseña: '',
        usuario_ruta: '',
      };
    },
  },
  computed: {
    paginatedProfesores() {
      const startIndex = (this.currentPage - 1) * this.perPage;
      const endIndex = startIndex + this.perPage;
      return this.profesores.slice(startIndex, endIndex);
    },
  },
  created() {
    this.token = localStorage.getItem('token')
    this.fetchProfesores();
  },
};
</script>


<style scoped>
.Profesores {
  padding: 20px;
}
.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>