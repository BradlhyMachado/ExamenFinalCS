<template>
  <div class="GrupoUsuario">
    <h2>Grupo de Usuarios</h2>

    <!-- Botón para abrir el modal de creación -->
    <div class="d-flex justify-content-start">
      <b-button @click="showCreateModal" variant="primary">Crear Grupo</b-button>
    </div>

    <!-- Modal de creación de grupo -->
    <b-modal v-model="createModalVisible" title="Crear Grupo" hide-footer hide-header-close>
      <b-form @submit.prevent="creategroup" class="mb-3">
        <b-form-group label="Nombre Grupo" label-for="nombreGrupoInput">
          <b-form-input id="nombreGrupoInput" v-model="newGroup.nombre_grupo" placeholder="Nombre Grupo"></b-form-input>
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
      <p>¿Estás seguro de que deseas eliminar este Horario?</p>
      <div class="d-flex justify-content-end">
        <div class="mr-2">
          <b-button @click="deleteHorarioConfirmed" variant="danger">Eliminar</b-button>
        </div>
        <div>
          <b-button @click="cancelDelete" variant="secondary">Cancelar</b-button>
        </div>
      </div>
    </b-modal>

    <!-- Table of Contents -->
    <b-table :items="paginatedGroup" :fields="fields" striped hover>
      <template #cell(nombre_grupo)="row">
        {{ row.value }}
      </template>
      <template #cell(acción)="row">
        <b-button @click="deleteGrupo(row.item)" variant="danger" size="sm">Eliminar</b-button>
      </template>
    </b-table>

    <!-- Contenedor del paginador centrado -->
    <div class="pagination-container">
      <b-pagination v-model="currentPage" :total-rows="groups.length" :per-page="perPage"></b-pagination>
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
      groups: [],
      newGroup: {
        nombre_grupo: '',
      },
      postURL: 'http://127.0.0.1:5000/grupoUsuario',
      fields: ['nombre_grupo', 'acción'],
      createModalVisible: false,
      confirmDeleteModalVisible: false,
      deletingGrupo: null,
      token: null,
    };
  },
  methods: {
    fetchgroups() {
      axios
        .post(this.postURL + 's', null, {
          headers: {
            Authorization: `Bearer ${this.token}`, // Incluir el token en el encabezado de la solicitud
          },
        })
        .then((res) => {
          console.log(res);
          this.groups = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    showCreateModal() {
      this.createModalVisible = true;
    },
    creategroup() {
      axios
        .put(this.postURL, this.newGroup, {
          headers: {
            Authorization: `Bearer ${this.token}`, // Incluir el token en el encabezado de la solicitud
          },
        })
        .then((res) => {
          this.groups.push(res.data);
          console.log(res.data);
          this.resetForm();
          this.createModalVisible = false;
          this.fetchgroups();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    deleteGrupo(grupo) {
      this.deletingGrupo = grupo;
      this.confirmDeleteModalVisible = true;
    },
    deleteHorarioConfirmed() {
      axios
        .delete(this.postURL, { data: { id_grupo_usuario: this.deletingGrupo.id_grupo }, 
          headers: {
            Authorization: `Bearer ${this.token}`, // Incluir el token en el encabezado de la solicitud
          },
        })
        .then((res) => {
          console.log(res.data);
          this.fetchgroups();
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
      this.newGroup = {
        nombre_grupo: '',
      };
    },
  },
  computed: {
    paginatedGroup() {
      const startIndex = (this.currentPage - 1) * this.perPage;
      const endIndex = startIndex + this.perPage;
      return this.groups.slice(startIndex, endIndex);
    },
  },
  created() {
    this.token = localStorage.getItem('token')
    this.fetchgroups();
  },
};
</script>


<style scoped>
.GrupoUsuario {
  padding: 20px;
}
.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>