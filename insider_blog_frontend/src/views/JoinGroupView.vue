<template>
  <header class="site-header">
    <form @submit.prevent="handleSubmit">
      <h3>Unirse a un grupo</h3>
      <div class="content-section">
        <div class="form-group">
          <label>Group</label>
          <select class="form-control form-control-lg" v-model="group">
            <option selected>General</option>
          </select>
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
  name: "JoinGroup",
  data() {
    return {
      title: "",
      content: "",
      group: 0,
    };
  },
  computed: {
    ...mapGetters({
      user: "user",
    }),
  },
  methods: {
    async handleSubmit() {
      let response = await axios.post(
        `"http://127.0.0.1:5000/user/${this.user.id}/group/${this.group}"`
      );
      console.log(response);
      //this.$store.dispatch("posts", posts);
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
