<template>
  <div class="container" v-if="user">
    <div class="posts">
      <div v-for="item in posts" v-bind:key="item.user_id">
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
                {{ item.title }}
              </router-link>
            </h2>
            <p class="article-content">{{ item.content }}</p>
          </div>
        </article>
      </div>
    </div>
    <TheGroups />
  </div>
  <div v-else>
    <h1>Please login or register to continue!! :D</h1>
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";
import store from "@/vuex";
import TheGroups from "@/components/TheGroups.vue";

export default {
  name: "Home",
  data() {
    return {
      groups: store.getters.groups,
    };
  },
  components: {
    TheGroups,
  },

  computed: {
    ...mapGetters(["user"]),
    ...mapGetters(["posts"]),
  },
  
  async created() {
    let post_response = await axios.get("/posts", {
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
    });
    let posts = await post_response.data.posts;
    this.$store.dispatch("posts", posts);

    let groups_response = await axios.get("/groups?page=0", {
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
    });
    let groups = groups_response.data.grupos;
    this.$store.dispatch("groups", groups);
  },
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
  margin-left: 190px;
  margin-right: 150px;
  margin-bottom: 30px;
}

.posts {
  margin-right: 50px;
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
  width: 25rem;
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
