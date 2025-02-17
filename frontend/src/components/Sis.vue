<template>
  <div>
    <WebAppHeader />
    <BackHomeButton class="backwards" />
    <SessionEnd class="logout" /><br />
    <Slide class="slide">
      <button @click="backHome()">
        <router-link style="color: white" to="">Startseite</router-link>
      </button>
      <hr />
      <button @click="exportToPDF">
        <router-link style="color: white" to="">Herunterladen</router-link>
      </button>
      <hr />
      <button @click="closeSession()">
        <router-link style="color: white" to="">Abmelden</router-link>
      </button>
    </Slide>
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
        <div class="buttons">
          <button class="cancel-button" type="button" @click="logout = false">
            Abbrechen
          </button>
          <button
            class="end-session-button"
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
    <button id="download-button" @click="exportToPDF">
      <b-icon-download></b-icon-download>
    </button>
    <div class="choose-audio-container">
      <span id="title">
        <h5>Audiodatei wählen: {{ this.category2 }}</h5>
      </span>
      <select class="dropdown" v-model="selected_file">
        <option v-for="file of jsonFiles" :key="file" :value="file">
          {{ file }}
        </option>
      </select>
      <button id="choose-audio" type="button" @click="chooseAudioFile(selected_file)">
        <a style="color: black" href="#input">übernehmen</a>
      </button>
    </div>
    <br />
    <div id="container">
      <div id="pdf">
        <div id="input">
          <h3 style="text-align: center">SIS-ambulant</h3>
          <br />
          <input
            style="font-size: smaller"
            placeholder="Name der pflegebedürftigen Person"
          />
          <input style="font-size: smaller" placeholder="Geburtsdatum" />
          <input
            style="font-size: smaller"
            placeholder="Gespräch am/Handzeichen Pflegefachkraft"
          />
          <input
            style="font-size: smaller"
            placeholder="pflegebedürftige Person/Angehöriger/Betreuer"
          />
        </div>
        <br />
        <b-card
          id="card0"
          header="aktuelle Situation"
          header-text-variant="white"
        >
          <b-card-text>
            <input
              style="width: 100%; border: none"
              v-if="category0"
              type="text"
              :value="category0"
            />
            <input
              style="width: 100%; border: none"
              id="placeholder"
              v-else
              type="text"
              placeholder="keine Angabe"
            />
          </b-card-text>
        </b-card>
        <b-card
          id="card1"
          header="kognitive und kommunikative Fähigkeiten"
          header-text-variant="white"
        >
          <b-card-text>
            <input
              style="width: 100%; border: none"
              v-if="category1"
              type="text"
              :value="category1"
            />
            <input
              style="width: 100%; border: none"
              id="placeholder"
              v-else
              type="text"
              placeholder="keine Angabe"
            />
          </b-card-text>
        </b-card>
        <b-card
          id="card2"
          header="Mobilität und Beweglichkeit"
          header-text-variant="white"
        >
          <b-card-text>
            <input
              style="width: 100%; border: none"
              v-if="category2"
              type="text"
              :value="category2"
            />
            <input
              style="width: 100%; border: none"
              id="placeholder"
              v-else
              type="text"
              placeholder="keine Angabe"
            />
          </b-card-text>
        </b-card>
        <b-card
          id="card3"
          header="krankheitsbezogene Anforderung und Belastung"
          header-text-variant="white"
        >
          <b-card-text>
            <input
              style="width: 100%; border: none"
              v-if="category3"
              type="text"
              :value="category3"
            />
            <input
              style="width: 100%; border: none"
              id="placeholder"
              v-else
              type="text"
              placeholder="keine Angabe"
            />
          </b-card-text>
        </b-card>
        <b-card
          id="card4"
          header="Selbstversorgung"
          header-text-variant="white"
        >
          <b-card-text>
            <input
              style="width: 100%; border: none"
              v-if="category4"
              type="text"
              :value="category4"
            />
            <input
              style="width: 100%; border: none"
              id="placeholder"
              v-else
              type="text"
              placeholder="keine Angabe"
            />
          </b-card-text>
        </b-card>
        <b-card
          id="card5"
          header="Leben in sozialen Beziehungen"
          header-text-variant="white"
        >
          <b-card-text>
            <input
              style="width: 100%; border: none"
              v-if="category5"
              type="text"
              :value="category5"
            />
            <input
              style="width: 100%; border: none"
              id="placeholder"
              v-else
              type="text"
              placeholder="keine Angabe"
            />
          </b-card-text>
        </b-card>
        <b-card
          id="card6"
          header="Haushaltsführung"
          header-text-variant="white"
        >
          <b-card-text>
            <input
              style="width: 100%; border: none"
              v-if="category6"
              type="text"
              :value="category6"
            />
            <input
              style="width: 100%; border: none"
              id="placeholder"
              v-else
              type="text"
              placeholder="keine Angabe"
            />
          </b-card-text>
        </b-card>
      </div>
    </div>
  </div>
</template>

<script>
import { Slide } from "vue-burger-menu";
import WebAppHome from "./WebAppHome";
import router from "../router";
import WebAppHeader from "./WebAppHeader";
import SisButton from "./SisButton";
import SessionEnd from "./SessionEnd";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";
import BackHomeButton from "./BackHomeButton";

export default {
  name: 'Sis',
  props: {
    title: String,
  },
  components: {
    WebAppHeader,
    BackHomeButton,
    SisButton,
    SessionEnd,
    WebAppHome,
    Slide,
  },
  created() {
    this.$root.$refs.Sis = this;
  },
  methods: {
    closeSession() {
      if (this.$route.path == "/") {
        this.$root.$refs.WebAppHome.popupLogout();
      } else if (this.$route.path == "/humaine/sis") {
        this.$root.$refs.Sis.popupLogout();
      }
    },
    backHome() {
      router.push('/humaine/');
    },
    signout() {
      this.axios.get("humaine/destroy_session").then((resp) => {});
      this.$session.destroy();
      router.push('/humaine/');
    },
    popupLogout() {
      this.logout = true;
    },
    categorys(data) {
      for (const [index, item] of data.entries()){
        let category = item['cls'];
        let text = item['txt'];
        if (category == "aktuelle Situation") {
          this.category0 += text + ";  ";
        }
        if (category == "kognitive und kommunikative Fähigkeiten") {
          this.category1 += text + ";  ";
        }
        if (category == "Mobilität und Beweglichkeit") {
          this.category2 += text + ";  ";
        }
        if (category == "krankheitsbezogene Anforderung und Belastung") {
          this.category3 += text + ";  ";
        }
        if (category == "Selbstversorgung") {
          this.category4 += text + ";  ";
        }
        if (category == "Leben in sozialen Beziehungen") {
          this.category5 += text + ";  ";
        }
        if (category == "Haushaltsführung") {
          this.category6 += text + ";  ";
        }
      };
    },
    chooseAudioFile(file) {
      let nameJson = file + ".json";
      this.axios
        .get("humaine/get_result" + "/" + nameJson.toString())
        .then((resp) => {
          this.data = resp.data;
          this.categorys(resp.data);
        });
    },
    getJsonFiles() {
      this.axios.get("humaine/file_list").then((resp) => {
        this.jsonFiles = resp.data;
      });
    },
    exportToPDF() {
      var dom = document.getElementById("pdf");
      html2canvas(dom).then(function (canvas) {
        var img = canvas.toDataURL("image/png");
        var doc = new jsPDF();
        doc.addImage(img, "JPEG", 5, 5, 200, 287);
        doc.save("SIS-Fragebogen.pdf");
      });
    },
    getRecordingData() {
      this.axios.get("humaine/latest_result").then((resp) => {
        this.newdata = resp.data;
        this.categorys(resp.data);
      });
    },
  },
  mounted: function () {
    if(this.$root.$refs.WebAppHome.recordedData != ''){
      this.getRecordingData();
    }
    this.getJsonFiles();
  },
  data() {
    return {
      showQuestionaire: false,
      logout: false,
      selected_file: '',
      newdata: [],
      category0: "",
      category1: "",
      category2: "",
      category3: "",
      category4: "",
      category5: "",
      category6: "",
      jsonFiles: [],
      data: [],
    };
  },
};
</script>

<style>
@import "../assets/styles/sis.css";
</style>
