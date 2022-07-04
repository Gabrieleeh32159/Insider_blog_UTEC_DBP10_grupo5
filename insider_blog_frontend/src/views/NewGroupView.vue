<template>
  <header class="site-header">
    <form @submit.prevent="handleSubmit">
      <h3>Crear Grupo</h3>
      <div class="content-section">
        <div class="form-group">
          <label>Name</label>
          <input class="form-control form-control-lg" v-model="group_name" />
        </div>

        <div class="form-group">
          <button class="btn btn-primary btn-block">Create</button>
        </div>
      </div>
    </form>
  </header>
</template>

<script>
import router from "@/router";
import axios from "axios";
import { mapGetters } from "vuex";
export default {
  name: "NewGroup",
  data() {
    return {
      group_name: "",
    };
  },
  computed: {
    ...mapGetters({
      user: "user",
    }),
  },
  methods: {
    async handleSubmit() {
      /*
      await fetch("http://127.0.0.1:5000/groups", {
        method: "POST",
        body: {
          groupname: this.group_name,
        },
        mode: "no-cors",
      }).then((response) => console.log(response.body));
      */

      await axios.post("/groups", {
        group_name: this.group_name,
      });
      await router.push("/");
    },
  },
};
</script>

<style>
.site-header {
  margin-top: 15px;
  padding-left: 5%;
  width: 500px;
}

.form-group {
  margin-top: 20px;
}
</style>
