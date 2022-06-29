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
      <router-link to="/">Cuenta</router-link>
      <router-link to="/">Salir</router-link>

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
</style>
