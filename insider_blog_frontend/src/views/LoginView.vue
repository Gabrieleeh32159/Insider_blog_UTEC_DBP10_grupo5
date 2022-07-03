<template>
    <header class="site-header">
    <form @submit.prevent="handleSubmit">
        <h3>Login</h3>
        <div class="content-section">
            <div class="form-group">
                <label>Email</label>
                <input type="email" class="form-control form-control-lg" v-model="email" />
            </div>

            <div class="form-group">
                <label>Password</label>
                <input type="password" class="form-control form-control-lg" v-model="password" />
            </div>

        <div class="form-group">
            <button class="btn btn-primary btn-block">Login</button>
        </div>
    </div>
    </form>
    <div class="alert alert-danger" role="alert" v-if="error">
        ERRORRRRRRRRRRRRRRRRRRRR
    </div>
    </header>
</template>

<script>
import axios from 'axios'
    export default{
        name: 'Login',
        data(){
            return {
                email: '',
                password: '',
            }
        },
        methods: {
            async handleSubmit(){
                let user = {
                    "email" : this.email,
                    "password" : this.password
                };
                await axios.post('http://localhost:5000/users', user)
                .then(data => {
                    if(data.data.status == "ok"){
                        console.log("Todo OK")
                    } else {
                     this.error = true;
                    };
                })
            }
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