<template>
    <div class="pet-view">
      <div v-if="pet" class="pet-details">
        <img :src="`/${pet.imagePath}`" :alt="pet.name" class="pet-image" />
        <div class="pet-info">
          <h1>{{ pet.name }}</h1>
          <p><strong>Tip:</strong> {{ pet.type }}</p>
          <p><strong>Starost:</strong> {{ pet.age }} godine</p>
          <p><strong>Veličina:</strong> {{ pet.size }}</p>
          <p><strong>Poreklo:</strong> {{ pet.origin }}</p>
          <p><strong>Cena:</strong> {{ pet.price }}$</p>
          <p><strong>Status:</strong> {{ pet.availabe }}</p>
          <p><strong>Opis:</strong> {{ pet.description }}</p>
          <!-- Dugme za dodavanje u korpu -->
          <button @click="addToCart(pet.petId)" class="add-to-cart-btn">Dodaj u korpu</button>
        </div>
      </div>
  
      <!-- Sekcija za komentare -->
      <div class="reviews-section">
        <h2>Komentari i ocene</h2>
        <div v-if="reviews.length > 0">
          <div v-for="review in reviews" :key="review.reviewId" class="review">
            <div class="review-header">
              <span class="review-rating">Ocena: {{ review.rating }}★</span>
              <span class="review-author">- {{ review.user.name }}</span>
            </div>
            <p class="review-comment">{{ review.comment }}</p>
          </div>
        </div>
        <div v-else>
          <p>Još uvek nema komentara za ovog ljubimca.</p>
        </div>
      </div>
    </div>
  </template>
  
<script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useRoute } from 'vue-router';
  import type { Pet } from '@/types/Pet';
  import type { Review } from '@/types/Review'
  
  const pet = ref<Pet | null>(null); // Tipiziraj pet kao Pet ili null
  const reviews = ref<Review[]>([]); // Tipiziraj reviews kao array Review objekata
  
  const route = useRoute();
  
  // Funkcija za dohvat podataka o ljubimcu
  async function fetchPetDetails() {
    const petId = route.params.id; // Preuzima ID ljubimca iz URL-a
    try {
      const response = await axios.get(`http://localhost:3000/api/pet/${petId}`);
      pet.value = response.data;
      await fetchReviews(Number(petId)); // Fetch komentare kada se ljubimac učita
    } catch (error) {
      console.error('Greška prilikom učitavanja podataka o ljubimcu:', error);
    }
  }
  
  // Funkcija za dohvat komentara za određenog ljubimca
  async function fetchReviews(petId: number) {
    const token = localStorage.getItem('token'); // Preuzimanje tokena iz localStorage
    if (!token) {
        console.log('Nema važećeg tokena');
        return;
    }

    try {
        const response = await axios.get(`http://localhost:3000/api/review/all`, {
        headers: {
            Authorization: `Bearer ${token}`, // Dodavanje tokena u Authorization header
        },
        });
        reviews.value = response.data.filter((review: Review) => review.petId === petId); // Filtriramo komentare za trenutno prikazanog ljubimca
    } catch (error) {
        console.error('Greška prilikom učitavanja komentara:', error);
    }
  }
  
  // Funkcija za dodavanje proizvoda u korpu
  async function addToCart(petId: number) {
    const token = localStorage.getItem('token');
    if (!token) {
      console.log('Nema važećeg tokena');
      return;
    }
  
    try {
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
      console.log('Proizvod dodat u korpu');
    } catch (error) {
      console.error('Greška prilikom dodavanja proizvoda u korpu:', error);
    }
  }
  
  onMounted(fetchPetDetails);
  onMounted(fetchReviews);
</script>
  
<style scoped>
    .pet-view {
    display: flex;
    flex-direction: column; /* Promena na vertikalni raspored */
    align-items: center;
    padding: 20px;
    }

    .pet-details {
    display: flex;
    gap: 20px;
    max-width: 800px;
    width: 100%;
    background-color: #fff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .pet-image {
    width: 300px;
    height: 300px;
    object-fit: cover;
    border-radius: 10px;
    }

    .pet-info {
    max-width: 400px;
    }

    .pet-info h1 {
    font-size: 24px;
    color: #333;
    }

    .pet-info p {
    font-size: 16px;
    color: #555;
    margin-bottom: 10px;
    }

    .pet-info strong {
    font-weight: bold;
    color: #333;
    }

    .add-to-cart-btn {
    background-color: #ff9800;
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    margin-top: 20px;
    transition: background-color 0.3s;
    }

    .add-to-cart-btn:hover {
    background-color: #e68900;
    }

  .reviews-section {
    margin-top: 30px;
    width: 100%; /* Širina sekcije za komentare */
    max-width: 800px; /* Ograničena širina sekcije za komentare */
    background-color: #fff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  .review {
    border-bottom: 1px solid #ddd;
    padding: 10px 0;
  }
  
  .review-header {
    display: flex;
    justify-content: space-between;
    font-weight: bold;
  }
  
  .review-rating {
    color: #ff9800;
  }
  
  .review-author {
    color: #888;
  }
  
  .review-comment {
    margin-top: 10px;
    color: #333;
  }
</style>

  