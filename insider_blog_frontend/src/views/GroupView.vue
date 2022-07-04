<template>
  <div class="posts">
    <h2>General</h2>
    <div v-for="item in posts" v-bind:key="item.user_id">
      <div v-if="item.group_id === 0">
        <article class="post-info">
          <router-link to="/user:/user">
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
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "GroupView",
  props: {
    slug: {
      type: String,
      required: true,
    },
  },
  computed: {
    ...mapGetters(["user"]),
    ...mapGetters(["posts"]),
    ...mapGetters(["groups"]),
    name_id(){
      console.log(this.posts)
      return this.posts.find((p) => p.group_id === this.slug)
    }
  },
  created(){
    for(var i = 0; i < this.groups.length; i++) {
      if(this.groups[i].group_name === this.slug){
        const id = this.groups[i].id;
      } 
    }
    console.log(this.slug)
  },
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
