<template>
  <div class="posts">
    <article class="post-info">
      <div v-if="user">
        <div v-if="post.user_id === user.id">CAN EDIT</div>
      </div>
      <router-link :to="{ name: 'Users', params: { slug: post.author_name } }">
        <img
          class="rounded-circle article-img"
          src="../assets/default.jpg"
          style="height: 65px; border-radius: 65px"
        />
      </router-link>

      <div class="media-body">
        <div class="article-metadata">
          <router-link
            :to="{ name: 'Users', params: { slug: post.author_name } }"
            >{{ post.author_name }}</router-link
          >
          <small class="text-muted"> 2022-06-28 </small>
        </div>
        <h2>
          <router-link
            :to="{ name: 'Posts', params: { slug: post.id } }"
            class="article-title"
          >
            {{ post.title }};
          </router-link>
        </h2>
        <p class="article-content">{{ post.content }}</p>
      </div>
    </article>
  </div>
</template>

<script>
import store from "@/vuex";
import { mapGetters } from "vuex";
export default {
  name: "Posts",
  props: {
    slug: {
      type: String,
      required: true,
    },
  },
  computed: {
    ...mapGetters(["user"]),
    post() {
      return store.state.posts.find((d) => d.id == this.slug);
    },
  },
};
</script>

<style scoped>
  @import '../assets/styles.css'

</style>
