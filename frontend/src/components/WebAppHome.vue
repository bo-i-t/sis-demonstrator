<template>
  <div id="app">
    <WebAppHeader />
    <SisButton />
    <SessionEnd class="logout" />
    <Slide class="slide">
      <button @click="switchToSis()">
        <router-link style="color: white" to="">Sis-Fragebogen</router-link>
      </button>
      <hr />
      <button @click="closeSession()">
        <router-link style="color: white" to="">Abmelden</router-link>
      </button>
    </Slide>
    <transition name="fade" appear>
      <div class="modal-overlay" v-if="showIntro"></div>
    </transition>
    <transition name="slide" appear>
      <div class="popup" v-if="showIntro">
        <h3><b>Willkommen in unserem Demonstrator!</b></h3>
        <p>Möchten Sie den Demonstrator starten ?</p>
        <div>
          <button
            class="start-session-button"
            type="button"
            @click="
              sessionStart();
              showIntro = false;
            "
          >
            Starten
          </button>
        </div>
      </div>
    </transition>
    <transition name="fade" appear>
      <div class="modal-overlay" v-if="logout"></div>
    </transition>
    <transition name="slide" appear>
      <div class="popup" v-if="logout">
        <h3><b>Möchten Sie den Demonstrator wirklich beenden?</b></h3>
        <p>
          Wenn Sie zustimmen, werden alle bisherigen Aufnahmen von dieser Seite
          entfernt.
        </p>
        <div>
          <button id="cancel-button" type="button" @click="logout = false">
            Abbrechen
          </button>
          <button
            id="end-session-button"
            type="button"
            @click="
              signout();
              logout = false;
            "
          >
            Beenden
          </button>
        </div>
      </div>
    </transition>
    <transition name="fade" appear>
      <div class="modal-overlay" v-if="showModal"></div>
    </transition>
    <transition name="slide" appear>
      <div class="popup" v-if="showModal">
        <h3><b>Möchten Sie diese Aufnahme wirklich löschen ?</b></h3>
        <p>
          Wenn Sie diese Aufnahme löschen wird diese hier und auch in Ihrem
          Ordner entfernt.
        </p>
        <div>
          <button class="cancel-button" type="button" @click="showModal = false">
            Abbrechen
          </button>
          <button
            class="delete"
            type="button"
            @click="
              removeRecord(numberOfRecord, fileDate);
              showModal = false;
            "
          >
            Löschen
          </button>
        </div>
      </div>
    </transition>
    <div class="record-audio">
      <h1>Neue Aufnahme erstellen</h1>
      <p>Nehmen Sie hier eine Audiodatei auf.</p>
      <div id="audio">
        <vue-record-audio
          id="record"
          @touchend="loadingData = true"
          style="background-color: rgb(205, 193, 197)"
          mimeType="audio/webm"
          mode="press"
          @result="onResult"
        /><b-icon-arrow-left id="arrow" v-if="hover"></b-icon-arrow-left>
      </div>
    </div>
    <div
      id="card-recording"
      title="Aufnahme"
      v-for="(rec, index) in recordings"
      :key="index"
    >
      <h5 class="card-header">Aufnahme</h5>
      <div class="card-body">
        <div class="btn-group" role="group">
          <audio class="m-2 w-75" controls :src="rec.wav" />
          <button
            type="button"
            @click="
              getIndex(index);
              showModal = true;
            "
            style="width: 200px"
            class="btn btn-outline-danger m-2"
          >
            <BIconTrash />
          </button>
        </div>
        <div
          class="form text-right px-2 py-1"
          v-for="(tra, idx) in rec.transcript"
          :key="idx"
        >
          <textarea
            v-on:change="NlpPredict(tra)"
            class="form-control"
            type="text"
            v-model="tra.txt"
          />
          <span class="badge badge-secondary">{{ tra.spk }}</span>
          <span class="badge badge-primary">{{ tra.cls }}</span>
        </div>
      </div>
    </div>
    <hr />
    <div class="no-audio" v-if="hiddenElement">
      <b-icon-folder
        class="icon"
        @mouseover="hover = true"
        @mouseleave="hover = false"
      ></b-icon-folder>
      <br />Sie müssen erst eine Audio aufnehmen
    </div>
    <div class="loading" v-if="loadingData">
      <b-spinner id="spinner" type="grow" label="Loading..."></b-spinner>
    </div>
  </div>
</template>

<script>
import router from "../router";
import { Slide } from "vue-burger-menu";
import WebAppHeader from "./WebAppHeader";
import SisButton from "./SisButton";
import SessionEnd from "./SessionEnd.vue";

export default {
  name: 'WebAppHome',
  components: {
    WebAppHeader,
    SisButton,
    SessionEnd,
    Slide,
  },
  props: {
    data: [],
  },
  created() {
    this.$root.$refs.WebAppHome = this;
  },
  mounted: function () {
    this.haveSession();
  },
  methods: {
    closeSession() {
      if (this.$route.path == "/humaine/") {
        this.$root.$refs.WebAppHome.popupLogout();
      } else if (this.$route.path == "/sis") {
        this.$root.$refs.Sis.popupLogout();
      }
    },
    switchToSis() {
      router.push({ name: "Sis" });
    },
    getIndex(index) {
      this.numberOfRecord = index;
    },
    signout() {
      this.axios.get("humaine/destroy_session").then((resp) => {});
      this.$session.destroy();
      this.showIntro = true;
      this.$root.$refs.SessionEnd.changeIcon();
    },
    popupLogout() {
      this.logout = true;
    },
    hoverIcon() {
      document.getElementById("record").style.color = "red";
    },
    haveSession() {
      if (this.$session.exists()) {
        this.showIntro = false;
      } else {
        this.showIntro = true;
        this.$root.$refs.SessionEnd.changeIcon();
      }
    },
    sessionStart() {
      this.$session.start();
      this.$root.$refs.SessionEnd.changeIcon();
    },
    getIntro() {
      this.showIntro = true;
    },
    removeRecord(index, filedate) {
      this.recordings.splice(index, 1);
      this.axios.get("humaine/delete_file" + "/" + filedate.toString());
      this.recordedData.pop();
      if (this.recordedData.length == 0) {
        this.hiddenElement = true;
      }
    },
    downloadRecord(data) {
      const link = document.createElement("a");
      link.href = data;
      let date = new Date();
      link.download = "Aufnahme " + date.toString();
      link.click();
    },
    onResult(data) {
      this.loadingData = true;
      this.$session.set("data", data);
      this.recordedData.push(data);
      this.hiddenElement = false;
      let cdate = new Date();
      this.fileDate = cdate;
      let wav = window.URL.createObjectURL(data);
      let formData = new FormData();
      formData.append("file", data, cdate.toString());
      this.axios
        .post("humaine/transcription", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((resp) => {
          this.loadingData = false;
          this.recordings.push({
            wav: wav,
            blob: data,
            date: cdate,
            transcript: resp.data.transcript,
          });
        });
    },
    previewAudio() {
      let audio = document.getElementById("audio-preview");
      let reader = new FileReader();

      reader.readAsDataURL(this.file);
      reader.addEventListener("load", function () {
        audio.src = reader.result;
      });
    },
    handleFileUpload(event) {
      this.file = event.target.files[0];
      this.previewAudio();
    },
  },
  data() {
    return {
      numberOfRecord: "",
      loadingData: false,
      logout: false,
      hover: false,
      recordedData: [],
      showIntro: false,
      hiddenElement: true,
      showModal: false,
      recordings: [],
      fileDate: "",
    };
  },
};
</script>

<style>
@import "../assets/styles/webAppHome.css";
</style>