<template>
  <div class="Seccion">
    <h2>Secciones</h2>

    <!-- Botón para abrir el modal de creación -->
    <div class="d-flex justify-content-start">
      <b-button @click="showCreateModal" variant="primary">Crear Sección</b-button>
    </div>

    <!-- Modal de creación de seccion -->
    <b-modal v-model="createModalVisible" title="Crear Sección" hide-footer hide-header-close>
      <b-form @submit.prevent="createSeccion" class="mb-3">
        <b-form-group label="Nombre Sección" label-for="nombreSeccionInput">
          <b-form-input id="nombreSeccionInput" v-model="newSeccion.nombre_seccion" placeholder="Nombre Sección"
            required></b-form-input>
        </b-form-group>
        <b-form-group label="Curso" label-for="cursoInput">
          <b-form-select id="cursoInput" v-model="newSeccion.id_curso" :options="cursos" value-field="id_curso"
            text-field="curso_nombre" placeholder="Seleccione un curso" required></b-form-select>
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

    <!-- Modal de edición de seccion -->
    <b-modal v-if="editingSeccion" v-model="editModalVisible" title="Editar Sección" hide-footer hide-header-close>
      <b-form @submit.prevent="updateSeccion(editingSeccion)" class="mb-3">
        <b-form-group label="Nombre Sección" label-for="nombreSeccionInput">
          <b-form-input id="nombreSeccionInput" v-model="editingSeccion.nombre_seccion" placeholder="Nombre Sección"
            required></b-form-input>
        </b-form-group>
        <b-form-group label="Curso" label-for="cursoInput">
          <b-form-select id="cursoInput" v-model="editingSeccion.id_curso" :options="cursos" value-field="id_curso"
            text-field="curso_nombre" placeholder="Seleccione un curso" required></b-form-select>
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
      <p>¿Estás seguro de que deseas eliminar esta Sesión?</p>
      <div class="d-flex justify-content-end">
        <div class="mr-2">
          <b-button @click="deleteSeccionConfirmed" variant="danger">Eliminar</b-button>
        </div>
        <div>
          <b-button @click="cancelDelete" variant="secondary">Cancelar</b-button>
        </div>
      </div>
    </b-modal>

    <!-- Table of Contents -->
    <b-table :items="paginatedSeccion" :fields="fields" striped hover>
      <template #cell(nombre_seccion)="row">
        {{ row.value }}
      </template>
      <template #cell(curso)="row">
        {{ row.value }}
      </template>
      <template #cell(acción)="row">
        <b-button @click="editSeccion(row.item)" variant="info" size="sm">Editar</b-button>
        <b-button @click="deleteSeccion(row.item)" variant="danger" size="sm">Eliminar</b-button>
      </template>
    </b-table>

    <!-- Contenedor del paginador centrado -->
    <div class="pagination-container">
      <b-pagination v-model="currentPage" :total-rows="seccion.length" :per-page="perPage"></b-pagination>
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
      seccion: [],
      cursos: [],
      newSeccion: {
        nombre_seccion: '',
        id_curso: ''
      },
      postURL: 'http://127.0.0.1:5000/seccion',
      fields: ['nombre_seccion', 'curso', 'acción'],
      editingSeccion: null,
      createModalVisible: false,
      editModalVisible: false,
      confirmDeleteModalVisible: false,
      deletingSeccion: null,
      token: null,
    };
  },
  methods: {
    fetchCursos() {
      axios
        .post('http://127.0.0.1:5000/cursos', null, {
          headers: {
            Authorization: `Bearer ${this.token}`, // Incluir el token en el encabezado de la solicitud
          },
        })
        .then((res) => {
          this.cursos = res.data;
          console.log(res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    fetchSeccion() {
      axios
        .post(this.postURL + 's', null, {
          headers: {
            Authorization: `Bearer ${this.token}`, // Incluir el token en el encabezado de la solicitud
          },
        })
        .then((res) => {
          console.log(res);
          this.seccion = res.data;
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
    createSeccion() {
      axios
        .put(this.postURL, this.newSeccion, {
          headers: {
            Authorization: `Bearer ${this.token}`, // Incluir el token en el encabezado de la solicitud
          },
        })
        .then((res) => {
          this.seccion.push(res.data);
          this.createModalVisible = false;
          this.fetchSeccion();
          this.resetForm();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    showEditModal(seccion) {
      this.editingSeccion = { ...seccion };
      this.editingSeccion.id_curso = seccion.id_curso;
      this.editModalVisible = true;
    },
    cancelEdit() {
      this.editModalVisible = false;
      this.editingSeccion = null;
    },
    updateSeccion(seccion) {
      const transformedseccion = {
        id_seccion: seccion.id_seccion,
        nombre_seccion: seccion.nombre_seccion,
        id_curso: seccion.id_curso
      };
      axios
        .patch(this.postURL, transformedseccion, {
          headers: {
            Authorization: `Bearer ${this.token}`, // Incluir el token en el encabezado de la solicitud
          },
        })
        .then((res) => {
          console.log(res.data);
          this.fetchSeccion();
          this.cancelEdit();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    editSeccion(seccion) {
      this.showEditModal(seccion);
    },
    deleteSeccion(seccion) {
      this.deletingSeccion = seccion;
      this.confirmDeleteModalVisible = true;
    },
    deleteSeccionConfirmed() {
      axios
        .delete(this.postURL, { data: { id_seccion: this.deletingSeccion.id_seccion },
          headers: {
            Authorization: `Bearer ${this.token}`, // Incluir el token en el encabezado de la solicitud
          },
        })
        .then((res) => {
          console.log(res.data);
          this.fetchSeccion();
          this.cancelDelete();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    cancelDelete() {
      this.confirmDeleteModalVisible = false;
      this.deletingSeccion = null;
    },
    resetForm() {
      this.newSeccion = {
        nombre_seccion: '',
        id_curso: ''
      };
    },
  },
  computed: {
    paginatedSeccion() {
      const startIndex = (this.currentPage - 1) * this.perPage;
      const endIndex = startIndex + this.perPage;
      return this.seccion.slice(startIndex, endIndex);
    },
  },
  created() {
    this.token = localStorage.getItem('token')
    this.fetchSeccion();
    this.fetchCursos();
  },
};
</script>


<style scoped>
.Seccion {
  padding: 20px;
}
.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>