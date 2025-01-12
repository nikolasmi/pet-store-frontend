<script setup lang="ts">
import { ref } from 'vue';
import Chatbot from './components/Chatbot.vue';
import Footer from './components/Footer.vue';
import Header from './components/Header.vue';

const isChatOpen = ref(false);
const initialMessage = "Dobrodošli! Kako možemo da vam pomognemo?";
</script>

<template>
  <Header />

  <div class="main-wrapper">
    <div class="inner-wrapper">
      <RouterView />

      
      <button 
        v-show="!isChatOpen" 
        @click="isChatOpen = true" 
        class="chatbot-button">
        Chat
      </button>

      <Chatbot v-show="isChatOpen" :initialMessage="initialMessage" @close="isChatOpen = false" />
    </div>
  </div>

  <Footer />
</template>

<style scoped>
.main-wrapper {
  display: flex;
  flex-grow: 1;
}

.inner-wrapper {
  width: 100%;
  position: relative;
}

/* Plivajući dugme koje pokreće chat */
.chatbot-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #39c0ed;
  color: white;
  border: none;
  border-radius: 50%;
  padding: 15px;
  font-size: 20px;
  cursor: pointer;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.chatbot-window {
  position: fixed;
  bottom: 80px; /* Visina od dna ekrana */
  right: 20px;
  width: 300px;
  height: 400px;
  background-color: white;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 15px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
</style>

