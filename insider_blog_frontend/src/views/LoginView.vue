<template>
  <header class="site-header horizontal">
    <form @submit.prevent="handleSubmit">
      <h3>Login</h3>
      <div class="content-section">
        <div class="form-group">
          <label>Username</label>
          <input
            type="username"
            class="form-control form-control-lg"
            v-model="username"
          />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input
            type="password"
            class="form-control form-control-lg"
            v-model="password"
          />
        </div>

        <div class="form-group">
          <button class="btn btn-primary btn-block">Login</button>
        </div>
      </div>
    </form>
    <div>
      <TheGroups />
    </div>
  </header>
</template>

<script>
import TheGroups from "../components/TheGroups.vue";
import axios from "axios";
export default {
  name: "Login",
  components: {
    TheGroups,
  },
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    async handleSubmit() {
      const response = await axios.post(
        "http://localhost:5000/login",
        {},
        {
          auth: {
            username: this.username,
            password: this.password,
          },
        }
      );
      localStorage.setItem("token", response.data.token);
      this.$store.dispatch("user", response.data.user);

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
