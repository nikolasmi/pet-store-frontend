<template>
  <div class="container">
    <div id="div-search">
      <input
        type="text"
        placeholder="Pretraga ljubimaca..."
        v-model="searchTerm"
        @input="filterItems"
      />
    </div>
    <div id="shop-page">
      <aside>
        <h2>Filteri</h2>
        <form id="filter-form" @submit.prevent="submitFilter">
          <div class="filter-group">
            <label for="minPrice">Minimalna cena</label>
            <input
              type="number"
              id="minPrice"
              v-model.number="filterData.minPrice"
              placeholder="Unesite minimalnu cenu"
            />
          </div>
          <div class="filter-group">
            <label for="minAge">Minimalna starost</label>
            <input
              type="number"
              id="minAge"
              v-model.number="filterData.minAge"
              placeholder="Unesite minimalnu starost"
            />
          </div>
          <div class="filter-group">
            <label>Tip</label>
            <select v-model="filterData.type">
              <option value="">Svi</option>
              <option value="pas">Pas</option>
              <option value="ribica">Ribica</option>
              <option value="hrcak">Hrčak</option>
              <option value="macka">Mačka</option>
              <option value="papagaj">Papagaj</option>
            </select>
          </div>
          <div class="filter-group">
            <label>Veličina</label>
            <select v-model="filterData.size">
              <option value="">Sve</option>
              <option value="mala">Mala</option>
              <option value="srednja">Srednja</option>
              <option value="velika">Velika</option>
            </select>
          </div>
          <div class="filter-group">
            <label>Dostupnost</label>
            <select v-model="filterData.availabe">
              <option value="">Sve</option>
              <option value="dostupno">Dostupni</option>
              <option value="nedostupno">Nedostupni</option>
            </select>
          </div>
          <button type="submit">Primeni filtere</button>
          <button type="button" @click="resetFilters" class="reset-button">Ukloni filtere</button>
        </form>
      </aside>
      <main>
        <div
          class="product"
          :key="pet.petId"
          :class="{ unavailable: pet.availabe === 'nedostupno' }"
          v-for="pet in filteredItems"
        >
          <img :src="`/${pet.imagePath}`" :alt="`${pet.imagePath}`" />
          <h2>{{ pet.name }}</h2>
          <p>{{ pet.description }}</p>
          <p>Tip: {{ pet.type }}</p>
          <p>Starost: {{ pet.age }} godine</p>
          <p>Veličina: {{ pet.size }}</p>
          <p>Cena: {{ pet.price }}$</p>
          <p>Status: {{ pet.availabe }}</p>
          <RouterLink :to="`/pet/${pet.petId}`">
            <button class="view-button">Pogledaj</button>
          </RouterLink>
          <button @click="addToCart(pet.petId)" :disabled="pet.availabe === 'nedostupno'">Kupi ljubimca</button>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import axios, { AxiosError } from 'axios';
import type { Pet } from '@/types/Pet';
import { toast } from 'vue3-toastify';
import { RouterLink } from 'vue-router';

const pets = ref<Pet[]>([]);
const filteredItems = ref<Pet[]>([]);
const searchTerm = ref("");

const filterData = ref({
  minPrice: null,
  minAge: null,
  type: "",
  size: "",
  availabe: "",
});

async function fetchPets() {
  try {
    const response = await axios.get("http://localhost:3000/api/pet");
    pets.value = response.data;
    filteredItems.value = [...pets.value];
  } catch (error) {
    console.error("Greška prilikom dohvatanja ljubimaca:", error);
    toast.error("Došlo je do greške prilikom dohvatanja ljubimaca.");
  }
}

async function addToCart(petId: number) {
    try {
        const token = localStorage.getItem('token'); 
        if (!token) {
            toast.error('Nema važećeg tokena');
            return;
        }

        const quantity = 1;

        await axios.post(
            'http://localhost:3000/api/cart/addToCart',
            { petId, quantity }, 
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        );

        toast.success('Proizvod dodat u korpu');
    } catch (error) {
        if (error instanceof AxiosError) {
            console.log('Greška prilikom dodavanja proizvoda u korpu:', error.response?.data);
            toast.error('Greška prilikom dodavanja proizvoda u korpu');
        }
    }
}

async function submitFilter() {
  try {
    const response = await axios.get("http://localhost:3000/api/pet", {
      params: {
        minPrice: filterData.value.minPrice,
        minAge: filterData.value.minAge,
        type: filterData.value.type,
        size: filterData.value.size,
        availabe: filterData.value.availabe,
      },
    });
    filteredItems.value = response.data;
  } catch (error) {
    console.error("Greška prilikom filtriranja ljubimaca:", error);
    toast.error("Došlo je do greške prilikom filtriranja ljubimaca.");
  }
}

function filterItems() {
  const search = searchTerm.value.toLowerCase();
  filteredItems.value = pets.value.filter((pet) =>
    pet.name.toLowerCase().includes(search)
  );
}

function resetFilters() {
  filterData.value = {
    minPrice: null,
    minAge: null,
    type: '',
    size: '',
    availabe: '',
  };
  searchTerm.value = '';
  fetchPets();
}

fetchPets();
</script>

<style scoped>
  .container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  font-family: Arial, sans-serif;
  background-color: #f9f9f9;
}

#div-search {
  width: 100%;
  margin-bottom: 20px;
  text-align: center;
}

#div-search input {
  width: 60%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  outline: none;
}

#div-search input:focus {
  border-color: #007bff;
}

#shop-page {
  display: flex;
  gap: 20px;
  width: 100%;
}

aside {
  flex: 0.8;
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

aside h2 {
  margin-bottom: 20px;
  color: #333;
  font-size: 20px;
}

.filter-group {
  margin-bottom: 15px;
}

.filter-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

.filter-group input,
.filter-group select {
  width: 100%;
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 5px;
  outline: none;
}

.filter-group input:focus,
.filter-group select:focus {
  border-color: #007bff;
}

button {
  padding: 10px 15px;
  font-size: 14px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button[type="submit"] {
  background-color: #007bff;
  color: white;
  margin-right: 10px;
}

button[type="submit"]:hover {
  background-color: #0056b3;
}

.reset-button {
  background-color: #f44336;
  color: white;
  margin-top: 5px;
}

.reset-button:hover {
  background-color: #d32f2f;
}

main {
  flex: 3.2;
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(4, 1fr); 
}

.product {
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.product img {
  width: 100%;
  height: 200px;
  border-radius: 10px;
  margin-bottom: 15px;
}

.product.unavailable {
  opacity: 0.8; 
  pointer-events: none; 
}

.product.unavailable img {
  opacity: 0.8; 
}

.product button.view-button {
  background-color: #17a2b8; 
  color: white;
  padding: 10px 20px;
  font-size: 14px;
  margin-bottom: 10px; 
  transition: background-color 0.3s ease;
  margin-right: 10px;
}

.product button.view-button:hover {
  background-color: #138496; 
}

button:disabled {
  background-color: #ccc;
  color: #666;
  cursor: not-allowed;
}

.product h2 {
  font-size: 18px;
  color: #333;
  margin-bottom: 10px;
}

.product p {
  font-size: 14px;
  color: #555;
  margin-bottom: 8px;
}

.product button {
  background-color: #28a745;
  color: white;
  padding: 10px 20px;
  font-size: 14px;
}

.product button:hover {
  background-color: #218838;
}

@media (max-width: 1024px) {
  main {
    grid-template-columns: repeat(3, 1fr); 
  }
}

@media (max-width: 768px) {
  main {
    grid-template-columns: repeat(2, 1fr); 
  }
}
</style>
