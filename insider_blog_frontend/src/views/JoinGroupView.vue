<template>
  <header class="site-header">
    <form @submit.prevent="handleSubmit">
      <h3>Unirse a un grupo</h3>
      <div class="content-section">
        <div class="form-group">
          <label>Grupo</label>
          <input type="group" name="group" v-model="group" class="form-control" />
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
      console.log("user", this.user.id)
      console.log("group!!!", this.group)
      await axios.post(
        "/user/"+this.user.id+"/group/"+this.group
      );
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
