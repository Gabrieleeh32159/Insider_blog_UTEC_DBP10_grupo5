<template>
  <div class="container">
    <div class="account-info">
      <img class="account-img" src="../assets/default.jpg" />
      <div class="media-body">
        <h2 class="account-heading mt-lg-4">{{ user.username }}</h2>
        <p class="text-secondary">{{ user.email }}</p>
      </div>
    </div>
    <div class="form-group">
      <button class="btn btn-primary btn-block">Edit</button>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "UserAccount",
  computed: {
    ...mapGetters({
      user: "user",
    }),
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
