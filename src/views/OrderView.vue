<template>
  <div class="container">
    <h1 class="title">Moje Porudžbine</h1>
    <div v-if="loading" class="loading">Učitavanje porudžbina...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="orders.length === 0 && !loading" class="empty">
      Nema porudžbina za prikazivanje.
    </div>
    <div v-for="order in orders" :key="order.orderId" class="order">
      <h2 class="order-title">Porudžbina #{{ order.orderId }}</h2>
      <p class="order-status">Status: <span>{{ order.status }}</span></p>
      <p class="order-price">Ukupna cena: <span>{{ order.totalPrice }} USD</span></p>
      <p class="order-date">Datum: <span>{{ new Date(order.createdAt).toLocaleDateString() }}</span></p>
      <div v-for="item in order.cart.cartPets" :key="item.cartPetId" class="order-item">
        <p>{{ item.pet.name }} - <span>{{ item.pet.price }} USD</span></p>
        <p>{{ item.pet.description }}</p>
        <p>Vrsta: {{ item.pet.type }}, Starost: {{ item.pet.age }} godina</p>
        <p>Veličina: {{ item.pet.size }}, Origin: {{ item.pet.origin }}</p>
        <div v-if="order.status === 'pristiglo' && !reviewedPets[item.petId]" class="review-form">
          <textarea v-model="reviews[item.petId].comment" placeholder="Unesite komentar..."></textarea>
          <input
            type="number"
            v-model="reviews[item.petId].rating"
            min="1"
            max="5"
            placeholder="Ocena (1-5)"
            required
          />
          <button @click="submitReview(order.orderId, item.petId)" class="review-button">
            Ostavi recenziju
          </button>
        </div>
        <div v-else-if="reviewedPets[item.petId]" class="reviewed-message">
          <p>Recenzija za ovog ljubimca je već poslata. Hvala!</p>
        </div>
      </div>
      <button 
        v-if="order.status !== 'otkazano' && order.status !== 'pristiglo'" 
        @click="confirmCancelOrder(order.orderId)" 
        class="cancel-button">
        Otkazi Porudžbinu
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import {jwtDecode} from "jwt-decode";

const getIdFromToken = () => {
  const token = localStorage.getItem("token");
  if (token) {
    const decodedToken = jwtDecode(token);
    return decodedToken.id;
  }
  return null;
};

const id = ref(getIdFromToken());
const orders = ref([]);
const loading = ref(false);
const error = ref(null);
const reviews = ref({});
const reviewedPets = ref({}); 

const loadOrders = async () => {
  if (!id.value) {
    error.value = "Korisnik nije prijavljen.";
    return;
  }

  loading.value = true;
  try {
    const token = localStorage.getItem("token");
    const response = await axios.get(`http://localhost:3000/api/order/user/${id.value}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.data.error) {
      error.value = response.data.message;
    } else {
      orders.value = response.data;

      orders.value.forEach(order => {
        order.cart.cartPets.forEach(item => {
          if (!reviews.value[item.petId]) {
            reviews.value[item.petId] = { comment: "", rating: 1 }; 
          }
          reviewedPets.value[item.petId] = false;
        });
      });
    }
  } catch (err) {
    error.value = "Došlo je do greške prilikom učitavanja porudžbina.";
  } finally {
    loading.value = false;
  }
};

const submitReview = async (orderId, petId) => {
  const token = localStorage.getItem("token");

  const reviewData = {
    petId: petId,
    rating: reviews.value[petId]?.rating,
    comment: reviews.value[petId]?.comment,
  };

  if (!reviewData.comment || reviewData.comment.trim() === "") {
    error.value = "Komentar ne sme biti prazan.";
    return;
  }

  if (!reviewData.rating || reviewData.rating < 1 || reviewData.rating > 5) {
    error.value = "Ocena mora biti između 1 i 5.";
    return;
  }

  try {
    const response = await axios.post(
      `http://localhost:3000/api/review/`,
      reviewData,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }
    );

    if (response.data.error) {
      error.value = response.data.message;
    } else {
      reviews.value[petId] = { comment: "", rating: 1 };
      reviewedPets.value[petId] = true;
    }
  } catch (err) {
    error.value = "Došlo je do greške prilikom postavljanja recenzije.";
  }
};

const cancelOrder = async (orderId) => {
  const token = localStorage.getItem("token");
  try {
    const response = await axios.patch(
      `http://localhost:3000/api/order/${orderId}`,
      { newStatus: "otkazano" },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (response.data.error) {
      error.value = response.data.message;
    } else {
      const updatedOrder = orders.value.find(order => order.orderId === orderId);
      if (updatedOrder) {
        updatedOrder.status = "otkazano";
      }
    }
  } catch (err) {
    error.value = "Došlo je do greške prilikom otkazivanja porudžbine.";
  }
};

const confirmCancelOrder = (orderId) => {
  if (confirm("Da li ste sigurni da želite da otkažete ovu porudžbinu?")) {
    cancelOrder(orderId);
  }
};

onMounted(() => {
  loadOrders();
});
</script>


<style scoped>
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    font-family: Arial, sans-serif;
  }
  
  .title {
    font-size: 2rem;
    font-weight: bold;
    color: #333;
    margin-bottom: 20px;
    text-align: center;
  }
  
  .loading {
    text-align: center;
    font-size: 1.2rem;
    color: #007bff;
  }
  
  .error {
    text-align: center;
    font-size: 1.2rem;
    color: #dc3545;
  }
  
  .empty {
    text-align: center;
    font-size: 1.2rem;
    color: #6c757d;
  }
  
  .order {
    background-color: #f8f9fa;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
  }
  
  .order-title {
    font-size: 1.5rem;
    color: #333;
    margin-bottom: 10px;
  }
  
  .order-status, .order-price, .order-date {
    font-size: 1.1rem;
    margin-bottom: 5px;
  }
  
  .order-status span, .order-price span, .order-date span {
    font-weight: bold;
    color: #007bff;
  }
  
  .review-form {
    margin-top: 20px;
  }
  
  .review-form textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 14px;
    resize: none;
  }
  
  .review-button {
    background-color: #28a745;
    margin-left: 5px;
    color: white;
    border: none;
    padding: 10px;
    cursor: pointer;
    margin-top: 10px;
  }
  
  .review-button:hover {
    background-color: #218838;
  }
  
  .cancel-button {
    background-color: red;
    color: white;
    border: none;
    padding: 10px;
    cursor: pointer;
  }
  
  .cancel-button:hover {
    background-color: darkred;
  }
  
  @media (max-width: 768px) {
    .container {
      padding: 10px;
    }
  
    .title {
      font-size: 1.5rem;
    }
  
    .order-title {
      font-size: 1.25rem;
    }
  
    .order-status, .order-price, .order-date {
      font-size: 1rem;
    }
  }
  </style>
  