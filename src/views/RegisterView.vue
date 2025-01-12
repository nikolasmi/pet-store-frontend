<template>
  <div class="container">
    <form @submit.prevent="submitForm()" class="registration-form">
      <h2>Registracija</h2>
      <div class="form-group">
        <label for="email">Email:</label>
        <input v-model="data.email" type="email" id="email" name="email" required />
      </div>
      <div class="form-group">
        <label for="pasword">Lozinka:</label>
        <input v-model="data.pasword" type="password" id="pasword" name="pasword" required />
      </div>
      <div class="form-group">
        <label for="name">Ime:</label>
        <input v-model="data.name" type="text" id="name" name="name" required />
      </div>
      <div class="form-group">
        <label for="phone">Telefon:</label>
        <input v-model="data.phone" type="tel" id="phone" name="phone" required />
      </div>
      <div class="form-group">
        <label for="address">Adresa:</label>
        <input v-model="data.address" type="text" id="address" name="address" required />
      </div>
      <div class="form-group">
        <label for="favoriteType">Omiljena vrsta ljubimca:</label>
        <input v-model="data.favoriteType" type="text" id="favoriteType" name="favoriteType" required />
      </div>
      <button type="submit">Registracija</button>
    </form>
  </div>
</template>
  
<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { toast } from 'vue3-toastify'  
import "vue3-toastify/dist/index.css";

const data = ref({
    email: '',
    pasword: '',
    name: '',
    phone: '',
    address: '',
    favoriteType: ''
});
  
  
function resetForm() {
    data.value = {
        email: '',
        pasword: '',
        name: '',
        phone: '',
        address: '',
        favoriteType: ''
    };
}
  
  
async function submitForm(){
    try {
        const { data: user } = await axios.post('http://localhost:3000/auth/user/register', data.value);
        toast("podaci uspesno prosledjeni", {
            "theme": "auto",
            "type": "success",
            "rtl": true,
            "autoClose": 2000,
            "transition": "slide",
            "dangerouslyHTMLString": true
        })
        resetForm();
    } catch (e) {
    }
}
  
</script>
  
<style scoped>
  @import "../assets/register.css";
</style>
  