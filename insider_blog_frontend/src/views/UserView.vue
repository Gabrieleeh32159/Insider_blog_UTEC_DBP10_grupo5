
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
        <router-link :to="{name: 'edit', params: {slug: this.user.id}}"> 
          <button class="btn btn-primary btn-block">Edit</button>
        </router-link>
      </div>
      </form>
    </div>
    <div class="posts">
    <div v-for="item in posts" v-bind:key="item.user_id">
      <div v-if="item.user_id == user_f.id">
      <article class="post-info">
        <router-link :to="{ name: 'Users', params: { slug: item.user_id } }">
          <img
            class="rounded-circle article-img"
            src="../assets/default.jpg"
            style="height: 65px; border-radius: 65px"
          />
        </router-link>

        <div class="media-body">
          <div class="article-metadata">
            <router-link
              :to="{ name: 'Users', params: { slug: item.user_id } }"
              >{{ item.author_name }}</router-link
            >
            <small class="text-muted"> 2022-06-28 </small>
          </div>
          <h2>
            <router-link
              :to="{ name: 'Posts', params: { slug: item.id } }"
              class="article-title"
            >
              {{ item.title }};
            </router-link>
          </h2>
          <p class="article-content">{{ item.content }}</p>
        </div>
      </article>
      </div>
    </div>
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
    ...mapGetters(['user',
    'posts']),
    user_f() {
      return store.state.users.find((d) => d.id == this.slug)
    }
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

.posts {
  margin-top: 2px;
  margin-left: 19px;
  margin-bottom: 3px;
  width: 100%;
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
