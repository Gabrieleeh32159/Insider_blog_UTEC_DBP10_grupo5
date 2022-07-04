<template>
  <header class="site-header">
    <form @submit.prevent="handleSubmit">
      <h3>Crear Post</h3>
      <div class="content-section">
        <div class="form-group">
          <label>Title</label>
          <input
            type="title"
            class="form-control form-control-lg"
            v-model="title"
          />
        </div>

        <div class="form-group">
          <label>Content</label>
          <input
            type="content"
            class="form-control form-control-lg"
            v-model="content"
          />
        </div>

        <div class="form-group">
          <label>Group</label>
          <input
            type="group"
            class="form-control form-control-lg"
            v-model="group"
          />
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
  name: "NewPost",
  data() {
    return {
      title: "",
      content: "",
    };
  },
  computed: {
    ...mapGetters({
      user: "user",
    }),
  },
  methods: {
    async handleSubmit() {
      await axios.post("/posts", {
        title: this.title,
        content: this.content,
        user_id: this.user.id,
        group_id: 0,
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
