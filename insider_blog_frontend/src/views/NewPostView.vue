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
          <textarea
            class="form-control form-control-lg"
            v-model="content"
          ></textarea>
        </div>

        <div class="form-group">
          <label>Group</label>
          <select class="form-control form-control-lg" v-model="group">
              <option v-for="group_name in user.groups_ids " 
                value={{group(group_name)}}
                >{{group_name}}</option>
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
import store from "@/vuex";
import axios from "axios";
import { mapGetters } from "vuex";
export default {
  name: "NewPost",
  data() {
    return {
      title: "",
      content: "",
      group: 0,
    };
  },
  computed: {
    user(){
      return store.state.user
    },
    group(search) {
      return store.state.groups.find((g) => g.group_name === search)
    }
  },
  methods: {
    async handleSubmit() {
      await axios.post("http://127.0.0.1:5000/posts", {
        title: this.title,
        content: this.content,
        user_id: store.state.user.id,
        group_id: this.group,
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
