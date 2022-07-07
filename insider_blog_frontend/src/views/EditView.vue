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
        <textarea v-model="description" class="form-control"></textarea>
      </div>

      <div class="form-group">
        <label>Password</label>
        <input v-model="password" class="form-control" />
      </div>

      <div class="form-group">
        <label>Confirm Password</label>
        <input v-model="confirm_pass" class="form-control" />
      </div>

      <div class="form-group">
        <button class="btn btn-primary btn-block" v-on:click="handleSubmit()">
          Submit
        </button>
      </div>

      <div
        id="diferent-passwords-alert"
        style="
          background-color: rgba(255, 20, 50, 0.8);
          border-radius: 10px;
          border: solid 3px red;
          margin-top: 20px;
          display: none;
        "
      >
        <h2>Contraseñas distintas</h2>
      </div>
    </form>
  </header>
</template>

<script>
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
      if (this.password == this.confirm_pass) {
        await axios.patch("/users/" + this.slug, {
          username: this.username,
        });

        await router.push("/" + this.slug);
      } else {
        console.log("gil");
      }
    },
  },
};
</script>
