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
      await axios.post("/groups", {
        groupname: this.groupname,
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
