<template>
    <header class="site-header">
    <form @submit.prevent="handleSubmit">
        <h3>Sign Up</h3>
        <div class="form-group">
            <label>Username</label>
            <input type="text" name="username" v-model="username" class="form-control"/>
        </div>

        <div class="form-group">
            <label>Email</label>
            <input type="email" name="email" v-model="email" class="form-control"/>
        </div>

        <div class="form-group">
            <label>Password</label>
            <input type="password" name="password" v-model="password" class="form-control"/>
        </div>

        <div class="form-group">
            <label>Confirm Password</label>
            <input type="password" name="confirm_pass" v-model="confirm_pass" class="form-control"/>
        </div>

        <div class="form-group">
            <button class="btn btn-primary btn-block" v-on:click="handleSubmit()" >Sign Up</button>
        </div>
    </form>
    </header>
</template>

<script>
// Aca deberiamos mandar a la api los datos del usuario pa crear
import axios from 'axios'
import VueAxios from 'vue-axios'
    export default
    {
        name: 'Register',
        data() {
            return {
                username: "",
                email: "",
                password: "",
            };
        },
        methods: {
            async handleSubmit(){
                await axios.post('http://127.0.0.1:5000/users',{
                    username: this.username,
                    email: this.email,
                    password: this.password
                })
            },
        }
    }

</script>