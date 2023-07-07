<template>
  <div class="Curso">
    <h2>Curso</h2>

    <!-- Botón para abrir el modal de creación -->
    <div class="d-flex justify-content-start">
      <b-button @click="showCreateModal" variant="primary">Crear Curso</b-button>
    </div>

    <!-- Modal de creación de grupo -->
    <b-modal v-model="createModalVisible" title="Crear Curso" hide-footer hide-header-close>
      <b-form @submit.prevent="createCurso" class="mb-3">
        <b-form-group label="Nombre Curso" label-for="nombreCursoInput">
          <b-form-input id="nombreCursoInput" v-model="newCurso.nombre_curso" placeholder="Nombre Curso"></b-form-input>
        </b-form-group>
        <div class="d-flex justify-content-end mt-3">
          <div class="mr-2">
            <b-button type="submit" variant="primary">Crear</b-button>
          </div>
          <div>
            <b-button @click="createModalVisible = false" variant="secondary">Cancelar</b-button>
          </div>
        </div>
      </b-form>
    </b-modal>

    <!-- Modal de confirmación de eliminación -->
    <b-modal v-model="confirmDeleteModalVisible" title="Confirmar Eliminación" hide-footer hide-header-close>
      <p>¿Estás seguro de que deseas eliminar este Curso?</p>
      <div class="d-flex justify-content-end">
        <div class="mr-2">
          <b-button @click="deleteCursoConfirmed" variant="danger">Eliminar</b-button>
        </div>
        <div>
          <b-button @click="cancelDelete" variant="secondary">Cancelar</b-button>
        </div>
      </div>
    </b-modal>

    <!-- Table of Contents -->
    <b-table :items="paginatedGroup" :fields="fields" striped hover>
      <template #cell(curso_nombre)="row">
        {{ row.value }}
      </template>
      <template #cell(acción)="row">
        <b-button @click="deleteCurso(row.item)" variant="danger" size="sm">Eliminar</b-button>
      </template>
    </b-table>

    <!-- Contenedor del paginador centrado -->
    <div class="pagination-container">
      <b-pagination v-model="currentPage" :total-rows="curso.length" :per-page="perPage"></b-pagination>
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
      curso: [],
      newCurso: {
        curso_nombre: '',
      },
      postURL: 'http://127.0.0.1:5000/curso',
      fields: ['curso_nombre', 'acción'],
      createModalVisible: false,
      confirmDeleteModalVisible: false,
      deletingCurso: null,
      token: null,
    };
  },
  methods: {
    fetchcurso() {
      axios
        .post(this.postURL + 's', null, {
          headers: {
            Authorization: `Bearer ${this.token}`, // Incluir el token en el encabezado de la solicitud
          },
        })
        .then((res) => {
          console.log(res);
          this.curso = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    showCreateModal() {
      this.createModalVisible = true;
    },
    createCurso() {
      axios
        .put(this.postURL, this.newCurso, {
          headers: {
            Authorization: `Bearer ${this.token}`, // Incluir el token en el encabezado de la solicitud
          },
        })
        .then((res) => {
          this.curso.push(res.data);
          console.log(res.data);
          this.resetForm();
          this.createModalVisible = false;
          this.fetchcurso();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    deleteCurso(grupo) {
      this.deletingCurso = grupo;
      this.confirmDeleteModalVisible = true;
    },
    deleteCursoConfirmed() {
      axios
        .delete(this.postURL, { data: { id_curso: this.deletingCurso.id_curso },
          headers: {
            Authorization: `Bearer ${this.token}`, // Incluir el token en el encabezado de la solicitud
          },
        })
        .then((res) => {
          console.log(res.data);
          this.fetchcurso();
          this.cancelDelete();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    cancelDelete() {
      this.confirmDeleteModalVisible = false;
      this.deletingHorario = null;
    },
    resetForm() {
      this.newCurso = {
        curso_nombre: '',
      };
    },
    confirmDelete(group) {
      if (window.confirm("¿Estás seguro de que deseas eliminar este registro?")) {
        this.deletegroup(group);
      }
    },
  },
  computed: {
    paginatedGroup() {
      const startIndex = (this.currentPage - 1) * this.perPage;
      const endIndex = startIndex + this.perPage;
      return this.curso.slice(startIndex, endIndex);
    },
  },
  created() {
    //localStorage.removeItem('token');
    this.token = localStorage.getItem('token')
    console.log(localStorage.getItem('token'));
    this.fetchcurso();
  },
};


</script>
<style scoped>
.Curso {
  padding: 20px;
}
.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>