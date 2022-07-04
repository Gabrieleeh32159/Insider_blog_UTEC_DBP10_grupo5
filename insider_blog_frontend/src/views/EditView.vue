<template>
  <header class="site-header">
    <form @submit.prevent="handleSubmit">
      <h3>Edit {{ user.username }} Profile'</h3>
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
        <label>Description</label>
        <input
          type="text"
          name="description"
          v-model="description"
          class="form-control"
        />
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
          Submit
        </button>
      </div>
    </form>
  </header>
</template>

<script>
// Aca deberiamos mandar a la api los datos del usuario pa crear
import router from "@/router";
import store from "@/vuex";
import axios from "axios";
export default {
  name: "EditProfile",
  compontents: {},
  data() {
    return {
      username: "",
      email: "",
      description: "",
      password: "",
      confirm_pass: "",
    };
  },
  props: {
    slug: {
      type: String,
      required: true,
    },
  },
  computed: {
    user() {
      return store.state.user;
    },
  },
  methods: {
    async handleSubmit() {
      await axios.patch("/users/" + this.slug, {
        username: this.username,
      });

      await router.push("/" + this.slug);
    },
  },
};
</script>
