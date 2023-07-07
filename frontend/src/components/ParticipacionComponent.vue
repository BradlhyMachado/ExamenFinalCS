<template>
  <div class="Participacion">
    <h2>Participaciones</h2>

    <!-- Botón para abrir el modal de creación -->
    <div class="d-flex justify-content-start">
      <b-button @click="showCreateModal" variant="primary">Crear Participación</b-button>
    </div>

    <!-- Modal de creación de Participacion -->
    <b-modal v-model="createModalVisible" title="Crear Participación" hide-footer hide-header-close>
      <b-form @submit.prevent="createParticipacion" class="mb-3">
        <b-form-group label="Puntos" label-for="notaFinalInput">
          <b-form-input id="notaFinalInput" v-model="newParticipacion.nota_final" placeholder="1" disabled></b-form-input>
        </b-form-group>
        <b-form-group label="Sección" label-for="seccionInput">
          <b-form-select id="seccionInput" v-model="newParticipacion.nombre_seccion" :options="secciones"
            value-field="nombre_seccion" text-field="nombre_seccion" placeholder="Seleccione una sección"
            required></b-form-select>
        </b-form-group>
        <b-form-group label="Estudiante" label-for="idEstudianteInput">
          <b-form-select id="idEstudianteInput" v-model="newParticipacion.id_estudiante" :options="estudiantes"
            value-field="id_estudiante" text-field="estudiante" placeholder="Seleccione un estudiante"
            required></b-form-select>
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

    <!-- Modal de edición de Participacion -->
    <b-modal v-if="editingParticipacion" v-model="editModalVisible" title="Modificar Participación" hide-footer
      hide-header-close>
      <b-form @submit.prevent="updateParticipacion(editingParticipacion)" class="mb-3">
        <b-form-group label="Puntos ganados" label-for="notaFinalInput">
          <div class="d-flex">
            <b-button @click="incrementNotaFinal" variant="primary" class="mr-2">+</b-button>
            <b-form-input id="notaFinalInput" v-model="editingParticipacion.nota_final"
              placeholder="Nota Final"></b-form-input>
            <b-button @click="decrementNotaFinal" variant="danger" class="ml-2">-</b-button>
          </div>
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
      <p>¿Estás seguro de que deseas eliminar esta participación?</p>
      <div class="d-flex justify-content-end">
        <div class="mr-2">
          <b-button @click="deleteParticipacionConfirmed" variant="danger">Eliminar</b-button>
        </div>
        <div>
          <b-button @click="cancelDelete" variant="secondary">Cancelar</b-button>
        </div>
      </div>
    </b-modal>

    <!-- Table of Contents -->
    <b-table :items="paginatedParticipacion" :fields="fields" striped hover>
      <template #cell(estudiante)="row">
        {{ row.value }}
      </template>
      <template #cell(nombre_seccion)="row">
        {{ row.value }}
      </template>
      <template #cell(nota_final)="row">
        {{ row.value }}
      </template>
      <template #cell(acción)="row">
        <b-button @click="editParticipacion(row.item)" variant="info" size="sm">Editar</b-button>
        <b-button @click="deleteParticipacion(row.item)" variant="danger" size="sm">Eliminar</b-button>
      </template>
    </b-table>

    <!-- Paginación -->
    <b-pagination :total-rows="participacion.length" :per-page="perPage" v-model="currentPage"
      class="mt-3"></b-pagination>
  </div>
</template>


<script>
import axios from 'axios';
export default {
  name: 'Participacion',
  data() {
    return {
      participacion: [],
      perPage: 10,
      currentPage: 1,
      createModalVisible: false,
      editModalVisible: false,
      editingParticipacion: null,
      newParticipacion: {
        nota_final: '',
        id_horario: '',
        nombre_seccion: '',
        id_estudiante: '',
      },
      secciones: [],
      estudiantes: [],
      postURL: 'http://127.0.0.1:5000/participacion',
      fields: [
        { key: 'estudiante', label: 'Estudiante' },
        { key: 'nombre_seccion', label: 'Seccion' },
        { key: 'nota_final', label: 'Puntos Ganados' },
        { key: 'acción', label: 'Acción' },
      ],
      confirmDeleteModalVisible: false,
      deletingParticipacion: null,
      token: null,
    };
  },
  methods: {
    fetchSecciones() {
      axios
        .post('http://127.0.0.1:5000/seccions', null, {
          headers: {
            Authorization: `Bearer ${this.token}`, // Incluir el token en el encabezado de la solicitud
          },
        })
        .then((res) => {
          this.secciones = res.data;
          if (this.newParticipacion.nombre_seccion) {
            this.fetchEstudiantes(this.newParticipacion.nombre_seccion);
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    fetchEstudiantes(nombre_seccion) {
      axios
        .post('http://127.0.0.1:5000/seccionByEstudiante', { nombre_seccion })
        .then((res) => {
          console.log(res.data);
          this.estudiantes = res.data;
          this.fetchParticipacion();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    fetchParticipacion() {
      axios
        .post(this.postURL + 's', null, {
          headers: {
            Authorization: `Bearer ${this.token}`, // Incluir el token en el encabezado de la solicitud
          },
        })
        .then((res) => {
          console.log(res.data);
          this.participacion = res.data;
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
    createParticipacion() {
      this.newParticipacion.nota_final = 1; // Establecer los puntos en 1
      axios
        .put(this.postURL, this.newParticipacion, {
          headers: {
            Authorization: `Bearer ${this.token}`, // Incluir el token en el encabezado de la solicitud
          },
        })
        .then((res) => {
          console.log(res.data);
          this.participacion.push(res.data);
          this.createModalVisible = false;
          this.fetchParticipacion();
          this.resetForm();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    editParticipacion(participacion) {
      this.editingParticipacion = { ...participacion };
      this.editModalVisible = true;
    },
    updateParticipacion(participacion) {
      axios
        .patch(this.postURL, participacion, {
          headers: {
            Authorization: `Bearer ${this.token}`, // Incluir el token en el encabezado de la solicitud
          },
        })
        .then((res) => {
          console.log(res.data);
          this.fetchParticipacion();
          this.editModalVisible = false;
          this.editingParticipacion = null;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    cancelEdit() {
      this.editingParticipacion = null;
      this.editModalVisible = false;
    },
    deleteParticipacion(participacion) {
      this.deletingParticipacion = participacion;
      this.confirmDeleteModalVisible = true;
    },
    deleteParticipacionConfirmed() {
      axios
        .delete(this.postURL, { data: { id_participacion: this.deletingParticipacion.id_participacion },
          headers: {
            Authorization: `Bearer ${this.token}`, // Incluir el token en el encabezado de la solicitud
          },
        })
        .then((res) => {
          console.log(res.data);
          this.fetchParticipacion();
          this.cancelDelete();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    cancelDelete() {
      this.confirmDeleteModalVisible = false;
      this.deletingParticipacion = null;
    },
    incrementNotaFinal() {
      this.editingParticipacion.nota_final++;
    },
    decrementNotaFinal() {
      if (this.editingParticipacion.nota_final > 0) {
        this.editingParticipacion.nota_final--;
      }
    },
    getIdHorarioBySeccion() {
      const dat = {
        nombre_seccion: this.newParticipacion.nombre_seccion,
      };
      axios
        .post('http://127.0.0.1:5000/seccionByHorario', dat)
        .then((res) => {
          console.log(res.data);
          if (typeof res.data[0] === 'undefined') {
            const idHorario = '';
            this.newParticipacion.id_horario = idHorario;
          } else {
            const idHorario = res.data[0].id_horario;
            this.newParticipacion.id_horario = idHorario;
          }
          this.fetchEstudiantes(this.newParticipacion.nombre_seccion);
          this.fetchParticipacion();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    resetForm() {
      this.newParticipacion = {
        nota_final: '',
        id_horario: '',
        nombre_seccion: '',
        id_estudiante: ''
      };
    }
  },
  watch: {
    'newParticipacion.nombre_seccion': function (newVal, oldVal) {
      if (newVal !== oldVal) {
        this.getIdHorarioBySeccion();
      }
    },
  },
  computed: {
    paginatedParticipacion() {
      const start = (this.currentPage - 1) * this.perPage;
      const end = this.currentPage * this.perPage;
      return this.participacion.slice(start, end);
    },
  },
  created() {
    this.token = localStorage.getItem('token')
    this.fetchParticipacion();
    this.fetchSecciones();
  },
};
</script>


<style scoped>
.Participacion {
  padding: 20px;
}
.mt-3 {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>