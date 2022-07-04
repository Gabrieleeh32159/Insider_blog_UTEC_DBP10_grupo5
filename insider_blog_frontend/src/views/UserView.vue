<template>
  <div class="container">
    <div class="account-info">
      <img class="account-img" src="../assets/default.jpg" />
      <div class="media-body">
        <h2 class="account-heading mt-lg-4">{{ user_f.username }}</h2>
        <p class="text-secondary">{{ user_f.email }}</p>
      </div>
    </div>
    <div v-if="user">
      <form @submit="handleSubmit">
        <div v-if="this.user.id == this.slug" class="form-group">
          <router-link :to="{ name: 'edit', params: { slug: this.user.id } }">
            <button class="btn btn-primary btn-block">Edit</button>
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import store from "@/vuex";
import { mapGetters } from "vuex";
export default {
  name: "UserAccount",
  props: {
    slug: {
      type: String,
      required: true,
    },
  },
  computed: {
    ...mapGetters(["user"]),
    user_f() {
      return store.state.users.find((d) => d.id == this.slug);
    },
  },
};
</script>

<style scoped>
.form-group {
  margin-top: 20px;
}

.container {
  padding: 20px;
  margin-top: 20px;
  margin-left: 190px;
  margin-bottom: 30px;
  width: 45%;
  border: 1px solid #dddddd;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.account-info {
  display: flex;
}
.account-img {
  height: 125px;
  width: 125px;
  margin-right: 20px;
  margin-bottom: 16px;
  border-radius: 50%;
}
</style>
