<template>
  <div id="nav">
    <div class="horizontal">
      <router-link to="/">
        <img
          src="../assets/logo.png"
          style="height: 40px; border-radius: 20px"
        />
      </router-link>
      <router-link to="/">Inicio</router-link>
      <router-link to="/about">Sobre Nosotros</router-link>
    </div>
    <!-- Navbar Right Side -->
    <div class="horizontal" v-if="user">
      <router-link to="/newpost">Nueva publicación</router-link>
      <router-link to="/joingroup">Unirse a un grupo</router-link>
      <router-link to="/newgroup">Crear un grupo</router-link>
      <router-link :to="{ name: 'Users', params: { slug: user.id } }">{{
        user.username
      }}</router-link>
      <a href="javascript:void(0)" @click="handleClick" class="nav0link"
        >Logout</a
      >
    </div>
    <div class="horizontal" v-if="!user">
      <router-link to="/login">Login</router-link>
      <router-link to="/register">Registrarse</router-link>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import store from "@/vuex";
export default {
  name: "TheNavigation",
  data() {
    return {
      users: store.users,
    };
  },
  methods: {
    handleClick() {
      localStorage.removeItem("token");
      this.$store.dispatch("user", null);
      this.$router.push("/");
    },
  },
  computed: {
    ...mapGetters(["user"]),
  },
};
</script>

<style scoped>
#nav {
  background-color: rgb(0, 187, 227);
  display: flex;
  padding-inline: 170px;
  padding-block: 10px;
  justify-content: space-between;
}

.horizontal {
  display: flex;
  align-items: center;
}

.horizontal a {
  text-decoration: none;
  padding-inline: 10px;
  color: #ecf6fb;
  transition: 0.5s;
}

.horizontal a:hover {
  color: #ffffff;
  transform: scale(1.1);
}

.navbar-light {
  background-color: #ffffff;
  box-shadow: 0px 14px 80px rgba(34, 35, 58, 0.2);
}

.auth-wrapper {
  display: flex;
  justify-content: center;
  flex-direction: column;
  text-align: left;
}

.auth-inner {
  width: 450px;
  margin: auto;
  background: #ffffff;
  box-shadow: 0px 14px 80px rgba(34, 35, 58, 0.2);
  padding: 40px 55px 45px 55px;
  border-radius: 15px;
  transition: all 0.3s;
}

.auth-wrapper .form-control:focus {
  border-color: #167bff;
  box-shadow: none;
}

.auth-wrapper h3 {
  text-align: center;
  margin: 0;
  line-height: 1;
  padding-bottom: 20px;
}

.custom-control-label {
  font-weight: 400;
}

.forgot-password a {
  text-align: center;
  font-size: 13px;
  padding-top: 10px;
  color: #7f7d7d;
  margin: 0;
}

.forgot-password a {
  color: #167bff;
}
</style>
