<script setup>

const posts = {
  0: {
    username: "Gabriel",
    title: "Gab",
    contenido: "brielbrielbriel ga b r i e l bag riel",
  },
  1: {
    username: "Poalo",
    title: "Pal",
    conteindo: "olo pa oalo oalaopa oalopal aop",
  },
  2: {
    username: "Marcelo",
    title: "Mar",
    contenido: "celo mar cleo ma rl e ocl ame clo rm",
  },
  3: {
    username: "Martin",
    title: "Mrt",
    contenido: "ain mar aistn in antaitn4",
  },
};
console.log(posts);
</script>

<template>
  <div>
    <h3 v-if="user">Hi, {{ user.username }}</h3>
    <h3 v-if="!user">You are not logged in!</h3>
  </div>
  <div class="posts">
    <div v-for="item in data" v-bind:key="item.user_id">
      <article class="post-info">
        <router-link to="/user/:user">
          <img
            class="rounded-circle article-img"
            src="../assets/default.jpg"
            style="height: 65px; border-radius: 65px"
          />
        </router-link>

        <div class="media-body">
          <div class="article-metadata">
            <router-link to="/user/:user">{{ item.user_id }}</router-link>
            <small class="text-muted"> 2022-06-28 </small>
          </div>
          <h2>
            <router-link to="/post/:post" class="article-title">
              {{ item.title }};
            </router-link>
          </h2>
          <p class="article-content">{{ item.content }}</p>
        </div>
      </article>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";



export default {
  name: "Home",
  computed: {
    ...mapGetters(["user"]),
  }, 
  async created(){
    const response = await axios.get('/posts');
    const data = response.data.posts
    console.log ('posts2: ', data);
  }
};
</script>

<style scoped>
.posts {
  margin-top: 20px;
  margin-left: 190px;
  margin-bottom: 30px;
  width: 50%;
}

.post-info {
  background: #ffffff;
  padding: 10px 20px;
  border: 1px solid #dddddd;
  border-radius: 3px;
  margin-bottom: 20px;
  display: flex;
}
.article-metadata {
  margin-left: 10px;
  border-bottom: 1px solid #dddddd;
  width: 35rem;
}

.article-title {
  color: #262626;
  text-decoration: none;
  font-weight: 550;
}

.article-title:hover {
  color: #4899e1;
}

.article-metadata a {
  margin: 10px;
  margin-right: 30px;
  color: #4899e1;
  text-decoration: none;
}

.article-metadata a:hover {
  text-decoration: underline;
}

.media-body h2,
p {
  padding-left: 15px;
}
</style>
