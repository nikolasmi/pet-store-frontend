<template>
    <div class="container">
      <form @submit.prevent="submitForm()" class="registration-form">
        <h2>Profil</h2>
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
        <button type="submit">Sačuvaj promene</button>
      </form>
    </div>
</template>
  
<script setup>
  import { reactive, onMounted } from "vue";
  import { jwtDecode } from "jwt-decode";
  import axios from "axios";
  import { toast } from 'vue3-toastify'  
  import "vue3-toastify/dist/index.css";

  
  const data = reactive({
    userId: null,
    email: "",
    pasword: "",
    name: "",
    phone: "",
    address: "",
    favoriteType: "",
  });
  
  const token = localStorage.getItem("token"); 
  if (!token) {
    alert("Niste prijavljeni!"); 
  } else {
    const decodedToken = jwtDecode(token);
    data.userId = decodedToken.id;
  }
  
  const fetchUserData = async () => {
    try {
      const response = await axios.get(`http://localhost:3000/api/user/${data.userId}`);
      Object.assign(data, response.data); 
    } catch (error) {
      console.error("Greška prilikom preuzimanja podataka korisnika:", error);
    }
  };
  
  const submitForm = async () => {
    try {
      await axios.put(`http://localhost:3000/api/user/${data.userId}`, { ...data });
      toast("podaci uspesno prosledjeni", {
            "theme": "auto",
            "type": "success",
            "rtl": true,
            "autoClose": 2000,
            "transition": "slide",
            "dangerouslyHTMLString": true
      })
    } catch (error) {
      console.error("Greška prilikom ažuriranja podataka korisnika:", error);
    }
  };
  
  onMounted(() => {
    if (data.userId) fetchUserData();
  });
</script>
  
<style scoped>
  @import "../assets/register.css";
</style>
