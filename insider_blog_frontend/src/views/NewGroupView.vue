<template>
  <header class="site-header">
    <form @submit.prevent="handleSubmit">
      <h3>Crear Grupo</h3>
      <div class="content-section">
        <div class="form-group">
          <label>Name</label>
          <input class="form-control form-control-lg" v-model="groupname" />
        </div>

        <div class="form-group">
          <button class="btn btn-primary btn-block">Create</button>
        </div>
      </div>
    </form>
  </header>
</template>

<script>
//import router from "@/router";
import axios from "axios";
import { mapGetters } from "vuex";
//import store from "@/vuex";
export default {
  name: "NewGroup",
  data() {
    return {
      groupname: "",
    };
  },
  computed: {
    ...mapGetters({
      user: "user",
    }),
  },
  methods: {
    async handleSubmit() {
      let response = await axios.post("http://127.0.0.1:5000/groups?page=0", {
        groupname: this.groupname,
        user_id: this.user.id,

        headers: {
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      });
      this.$store.dispatch("groups", response.data.groups);
      //TheGroups.groups = response.data.groups;
      this.$router.push("/");
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
