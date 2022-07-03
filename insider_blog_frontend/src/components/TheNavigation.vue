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
    <div class="horizontal">
      <router-link to="/">Nueva publicación</router-link>
      <router-link to="/">Unirse a un grupo</router-link>
      <router-link to="/">Crear un grupo</router-link>
      <router-link to="/login">Login</router-link>
      <router-link to="/register">Registrarse</router-link>

      <!-- Si no esta loggeado 
                  <a class="nav-item nav-link" href="/login">Iniciar sesión</a>
                  <a class="nav-item nav-link" href="/register">Registrarse</a>
                -->
    </div>
  </div>
</template>

<script>
export default {
  name: "TheNavigation",
  data() {
    return {};
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

.navbar-light{
  background-color: #ffffff;
  box-shadow: 0px 14px 80px rgba(34,35,58, 0.2);
}

.auth-wrapper{
  display: flex;
  justify-content: center;
  flex-direction: column;
  text-align: left;
}

.auth-inner{
  width: 450px;
  margin: auto;
  background: #ffffff;
  box-shadow: 0px 14px 80px rgba(34,35,58, 0.2);
  padding: 40px 55px 45px 55px;
  border-radius: 15px;
  transition: all .3s;
}

.auth-wrapper .form-control:focus{
  border-color: #167bff;
  box-shadow: none;
}

.auth-wrapper h3{
  text-align: center;
  margin: 0;
  line-height: 1;
  padding-bottom: 20px;
}

.custom-control-label{
  font-weight: 400;
}

.forgot-password a{
  text-align: center;
  font-size: 13px;
  padding-top: 10px;
  color:#7f7d7d;
  margin: 0;

}

.forgot-password a{
  color: #167bff;
}


</style>
