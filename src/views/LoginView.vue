<template>
    <div id="wraper">
      <div class="container">
        <form @submit.prevent="submitForm()" class="login-form">
          <h2>Login</h2>
          <p>ulogujte se kako biste videli listu želja i korpu</p>
          <div class="form-group">
            <label for="email">Email:</label>
            <input v-model="data.email" type="email" id="email" name="email" required />
          </div>
          <div class="form-group">
            <label for="password">Lozinka:</label>
            <input v-model="data.pasword" type="password" id="password" name="password" required />
          </div>
          <button type="submit">Prijava</button>
        </form>
      </div>
    </div>
</template>
  
<script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  import router from '../router';
  import { toast } from 'vue3-toastify'  
  import "vue3-toastify/dist/index.css";
  
  const data = ref({
    email: '',
    pasword: '', 
  });
  
  async function submitForm() {
    try {
      const response = await axios.post('http://localhost:3000/auth/user/login', {
        email: data.value.email,
        pasword: data.value.pasword,  
      });
  
      const token = response.data.token;
  
      if (token) {
        localStorage.setItem('token', token);
        
        setTimeout(() => {
          localStorage.removeItem('token');
          router.push({ name: 'login' });
          toast.error('Istekla sesija');
        }, 600000);
        
        toast.success('Dobrodošli!');
        router.push('/');
      }
    } catch (error) {
      toast.error('Pogrešno korisničko ime ili lozinka');
    }
  }
</script>
  
<style scoped>
  .container {
    max-width: 400px;
    margin: 50px auto;
    padding: 20px;
    border-radius: 8px;
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  
  .login-form {
    text-align: center;
  }
  
  .form-group {
    margin-bottom: 20px;
    margin-top: 15px;
  }
  
  p {
    margin-top: 5px;
  }
  
  label {
    display: block;
    margin-bottom: 8px;
  }
  
  input[type="email"],
  input[type="password"] {
    width: calc(100% - 16px);
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #ccc;
  }
  
  button {
    padding: 10px 20px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button[type="submit"]:hover {
    background-color: rgb(0, 0, 0);
  }
</style>
  