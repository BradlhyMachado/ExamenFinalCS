<template>
  <div class="Horario">
    <h2>Horarios</h2>

    <!-- Botón para abrir el modal de creación -->
    <div class="d-flex justify-content-start">
      <b-button @click="showCreateModal" variant="primary">Crear Horario</b-button>
    </div>

    <!-- Modal de creación de horario -->
    <b-modal v-model="createModalVisible" title="Crear Horario" hide-footer hide-header-close>
      <b-form @submit.prevent="createHorario" class="mb-3">
        <b-form-group label="Dia Semana" label-for="diaSemanaInput">
          <b-form-select id="diaSemanaInput" v-model="newHorario.dia_semana" :options="diasSemana"
            placeholder="Día Semana" required></b-form-select>
        </b-form-group>
        <b-form-group label="Hora Inicio" label-for="horaInicioInput">
          <b-form-timepicker id="horaInicioInput" v-model="newHorario.hora_inicio" placeholder="Hora Inicio"
            required></b-form-timepicker>
        </b-form-group>
        <b-form-group label="Hora Fin" label-for="horaFinInput">
          <b-form-timepicker id="horaFinInput" v-model="newHorario.hora_fin" placeholder="Hora Fin"
            required></b-form-timepicker>
        </b-form-group>

        <b-form-group label="Sección" label-for="seccionInput">
          <b-form-select id="seccionInput" v-model="newHorario.id_seccion" :options="secciones" value-field="id_seccion"
            text-field="nombre_seccion" placeholder="Seleccione una sección" required></b-form-select>
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

    <!-- Modal de edición de horario -->
    <b-modal v-if="editingHorario" v-model="editModalVisible" title="Editar Horario" hide-footer hide-header-close>
      <b-form @submit.prevent="updateHorario(editingHorario)" class="mb-3">
        <b-form-group label="Dia Semana" label-for="diaSemanaInput">
          <b-form-select id="diaSemanaInput" v-model="editingHorario.dia_semana" :options="diasSemana"
            placeholder="Dia Semana" required></b-form-select>
        </b-form-group>
        <b-form-group label="Hora Inicio" label-for="horaInicioInput">
          <b-form-timepicker id="horaInicioInput" v-model="editingHorario.hora_inicio" placeholder="Hora Inicio"
            required></b-form-timepicker>
        </b-form-group>
        <b-form-group label="Hora Fin" label-for="horaFinInput">
          <b-form-timepicker id="horaFinInput" v-model="editingHorario.hora_fin" placeholder="Hora Fin"
            required></b-form-timepicker>
        </b-form-group>

        <b-form-group label="Sección" label-for="seccionInput">
          <b-form-select id="seccionInput" v-model="editingHorario.id_seccion" :options="secciones"
            value-field="id_seccion" text-field="nombre_seccion" placeholder="Seleccione una sección"
            required></b-form-select>
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
    <b-table :items="paginateHorario" :fields="fields" striped hover>
      <template #cell(dia_semana)="row">
        {{ row.value }}
      </template>
      <template #cell(hora_inicio)="row">
        {{ row.value }}
      </template>
      <template #cell(hora_fin)="row">
        {{ row.value }}
      </template>
      <template #cell(seccion)="row">
        {{ row.value }}
      </template>
      <template #cell(acción)="row">
        <b-button @click="editHorario(row.item)" variant="info" size="sm">Editar</b-button>
        <b-button @click="deleteHorario(row.item)" variant="danger" size="sm">Eliminar</b-button>
      </template>
    </b-table>

    <!-- Contenedor del paginador centrado -->
    <div class="pagination-container">
      <b-pagination v-model="currentPage" :total-rows="horario.length" :per-page="perPage"></b-pagination>
    </div>
  </div>
</template>

<script>
import axios from 'axios';


export default {
  data() {
    return {
      //diasSemana: ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
      diasSemana: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
      currentPage: 1,
      perPage: 5,
      horario: [],
      newHorario: {
        dia_semana: '',
        hora_inicio: '',
        hora_fin: '',
        id_seccion: ''
      },
      secciones: [],
      postURL: 'http://127.0.0.1:5000/horario',
      fields: ['dia_semana', 'hora_inicio', 'hora_fin', 'seccion', 'acción'],
      editingHorario: null,
      createModalVisible: false,
      editModalVisible: false,
      confirmDeleteModalVisible: false,
      deletingHorario: null,
    };
  },
  methods: {
    fetchHorario() {
      axios
        .post(this.postURL + 's', null, {
          headers: {
            Authorization: `Bearer ${this.token}`, // Incluir el token en el encabezado de la solicitud
          },
        })
        .then((res) => {
          console.log(res);
          this.horario = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    fetchSecciones() {
      axios
        .post('http://127.0.0.1:5000/seccions', null, {
          headers: {
            Authorization: `Bearer ${this.token}`, // Incluir el token en el encabezado de la solicitud
          },
        })
        .then((res) => {
          this.secciones = res.data;
          console.log(res.data);
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
    createHorario() {
      axios
        .put(this.postURL, this.newHorario,{
          headers: {
            Authorization: `Bearer ${this.token}`, // Incluir el token en el encabezado de la solicitud
          },
        })
        .then((res) => {
          this.horario.push(res.data);
          this.createModalVisible = false;
          this.fetchHorario();
          this.resetForm();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    showEditModal(horario) {
      this.editingHorario = { ...horario };
      this.editModalVisible = true;
    },
    cancelEdit() {
      this.editModalVisible = false;
      this.editingHorario = null;
    },
    updateHorario(horario) {
      const transformedhorario = {
        id_horario: horario.id_horario,
        dia_semana: horario.dia_semana,
        hora_inicio: horario.hora_inicio,
        hora_fin: horario.hora_fin,
        id_seccion: horario.id_seccion
      };
      axios
        .patch(this.postURL, transformedhorario,{
          headers: {
            Authorization: `Bearer ${this.token}`, // Incluir el token en el encabezado de la solicitud
          },
        })
        .then((res) => {
          console.log(res.data);
          this.fetchHorario();
          this.cancelEdit();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    editHorario(horario) {
      this.showEditModal(horario);
    },
    deleteHorario(horario) {
      this.deletingHorario = horario;
      this.confirmDeleteModalVisible = true;
    },
    deleteHorarioConfirmed() {
      axios
        .delete(this.postURL, { data: { id_horario: this.deletingHorario.id_horario },
          headers: {
            Authorization: `Bearer ${this.token}`, // Incluir el token en el encabezado de la solicitud
          },
        })
        .then((res) => {
          console.log(res.data);
          this.fetchHorario();
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
      this.newHorario = {
        dia_semana: '',
        hora_inicio: '',
        hora_fin: '',
        id_seccion: ''
      }
    }
  },
  computed: {
    paginateHorario() {
      const startIndex = (this.currentPage - 1) * this.perPage;
      const endIndex = startIndex + this.perPage;
      return this.horario.slice(startIndex, endIndex);
    },
  },
  created() {
    this.token = localStorage.getItem('token')
    this.fetchHorario();
    this.fetchSecciones();
  },
};
</script>


<style scoped>
.Horario {
  padding: 20px;
}
.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>