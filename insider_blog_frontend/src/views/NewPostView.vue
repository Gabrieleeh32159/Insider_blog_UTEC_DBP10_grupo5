<template>
    <header class="site-header">
    <form @submit.prevent="handleSubmit">
        <h3>Crear Post</h3>
        <div class="content-section">
            <legend class="border-bottom mb-4">{{ legend }}</legend>
            <div class="form-group">
                <label>Title</label>
                <input type="title" class="form-control form-control-lg" v-model="title" />
            </div>

            <div class="form-group">
                <label>Content</label>
                <input type="content" class="form-control form-control-lg" v-model="content" />
            </div>

            <div class="form-group">
                <label>Group</label>
                <input type="group" class="form-control form-control-lg" v-model="group" />
            </div>

        <div class="form-group">
            <button class="btn btn-primary btn-block">Create</button>
        </div>
    </div>
    </form>
    </header>
</template>

<script>
import router from '@/router';
import axios from 'axios'
    export default{
        name: 'NewPost',
        data(){
            return {
                title: '',
                content: '',
            }
        },
        methods: {
            async handleSubmit(){
                 await axios.post('/posts',{
                    title: this.title,
                    content: this.content,
                    group_name: this.group
                })
                await router.push('/');
            },
        }
    }
</script>

<style>
.site-header {
    margin-top: 15px;
    padding-left: 5%;
    width: 500px;
}

.form-group {
    margin-top: 20px;

}

</style>