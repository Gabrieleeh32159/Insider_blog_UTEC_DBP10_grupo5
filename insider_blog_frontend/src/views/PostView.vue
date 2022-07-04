<template>
  <div class="posts">
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
          <router-link to="/user/:user">Gabriel</router-link>
          <small class="text-muted"> 2022-06-28 </small>
        </div>
        <h2>
          <router-link to="/post/:post" class="article-title">
            Nuevo Post;
          </router-link>
        </h2>
        <p class="article-content">
          Marvin danos mas tiempo mavin danos mas tiempo marvin danos mas tiempo
        </p>
      </div>
    </article>
  </div>
</template>

<script>
import store from '@/vuex'
export default{
    name: 'Posts',
    props: {
        slug: {
            type: String,
            required: true,
        },
    }

}

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
