<template>
  <div class="asistencia">
    <h1>Tomar Asistencia</h1>
    <div class="camera-container">
      <div class="camera-column1">
        <video ref="video" class="camera-video"></video>
        <div class="camera-button-container">
          <b-button @click="tomarFoto">Capturar foto</b-button>
        </div>
      </div>
      <div class="camera-column2">
        <div>
          <img v-if="photo" :src="photo" alt="Foto tomada" class="camera-photo">
        </div>
        <div v-if="photo" class="camera-button-container">
          <div class="camera1">
            <b-form>
              <b-button @click="tomarAsistencia">Tomar Asistencia</b-button>
            </b-form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import Swal from 'sweetalert2'
export default {
  data() {
    return {
      photo: null,
      stream: null,

      dni: null,
    };
  },
  created() {
    this.dni = localStorage.getItem('dni')
    navigator.mediaDevices.getUserMedia({ video: true })
      .then((stream) => {
        this.stream = stream;
        this.$refs.video.srcObject = stream;
        this.$refs.video.play();
      })
      .catch((error) => {
        console.error("Error al acceder a la cámara: ", error);
      });
  },
  beforeUnmount() {
    if (this.stream) {
      this.stream.getTracks().forEach((track) => track.stop());
    }
  },
  methods: {
    dataURItoBlob(dataURI) {
      const byteString = atob(dataURI.split(',')[1]);
      const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
      const arrayBuffer = new ArrayBuffer(byteString.length);
      const uint8Array = new Uint8Array(arrayBuffer);

      for (let i = 0; i < byteString.length; i++) {
        uint8Array[i] = byteString.charCodeAt(i);
      }

      return new Blob([arrayBuffer], { type: mimeString });
    },
    tomarFoto() {
      const video = this.$refs.video;
      const canvas = document.createElement("canvas");
      const context = canvas.getContext("2d");

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      this.photo = canvas.toDataURL("image/png");
    },
    tomarAsistencia() {
      if (this.photo) {
        const blob = this.dataURItoBlob(this.photo);
        const formData = new FormData();
        
        formData.append('dni', this.dni);
        formData.append('foto', blob, 'foto.png');
        axios
          .post("http://127.0.0.1:5000/tomarAsistencia", formData)
          .then((res) => {
            console.log(res.data['dist'], res.data['horario']);

            if (typeof res.data['horario'] === 'undefined') {
              Swal.fire({
                title: 'Error',
                text: 'El rostro no ha sido reconocido. Por favor, inténtalo de nuevo',
                icon: 'error',
              });
            } else if (res.data['horario'] === false) {
              Swal.fire({
                title: 'Error',
                text: 'No tienes clases a esta hora',
                icon: 'error',
              });
            } else if (res.data['dist'] < 0.6) {
              Swal.fire({
                title: 'Éxito',
                text: 'Asistencia tomada con éxito',
                icon: 'success',
              });
            } else {
              Swal.fire({
                title: 'Error',
                text: 'No coincides con la persona del DNI',
                icon: 'error',
              });
            }

          })
          .catch((error) => {
            Swal.fire({
              title: 'Error',
              text: 'El rostro no ha sido reconocido. Por favor, inténtalo de nuevo',
              icon: 'error',
            });
            console.log(error);
          });

      } else {
        print("no se tomo ninguna foot")
      }
    }
  },
};
</script>


<style scoped>
.asistencia {
  text-align: center;
  margin-top: 40px;
}
.camera-container {
  justify-content: center;
}
.camera-video {
  border: 1px solid #ccc;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
  width: 30%;
  height: auto;
}
.camera-button-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
.camera-photo {
  border: 1px solid #ccc;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
  max-width: 30%;
  height: auto;
}
@media (max-width: 767px) {
  .camera-container {
    flex-direction: column;
  }
}
</style>