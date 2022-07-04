<template>
  <header class="site-header">
    <form @submit.prevent="handleSubmit">
      <h3>Sign Up</h3>
      <div class="form-group">
        <label>Username</label>
        <input
          type="text"
          name="username"
          v-model="username"
          class="form-control"
        />
      </div>

      <div class="form-group">
        <label>Email</label>
        <input type="email" name="email" v-model="email" class="form-control" />
      </div>

      <div class="form-group">
        <label>Password</label>
        <input
          type="password"
          name="password"
          v-model="password"
          class="form-control"
        />
      </div>

      <div class="form-group">
        <label>Confirm Password</label>
        <input
          type="password"
          name="confirm_pass"
          v-model="confirm_pass"
          class="form-control"
        />
      </div>

      <div class="form-group">
        <button class="btn btn-primary btn-block" v-on:click="handleSubmit()">
          Sign Up
        </button>
      </div>
    </form>
  </header>
</template>

<script>
import router from "@/router";
import axios from "axios";

export default {
  name: "Register",
  compontents: {},
  data() {
    return {
      username: "",
      email: "",
      password: "",
      confirm_pass: "",
    };
  },
  methods: {
    async handleSubmit() {
      if (this.password == this.confirm_pass) {
        await axios.post("/users", {
          username: this.username,
          email: this.email,
          password: this.password,
        });
        await router.push("/login");
      }
    },
  },
};
</script>
