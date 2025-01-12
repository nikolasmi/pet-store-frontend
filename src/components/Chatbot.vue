<script setup lang="ts">
import { ref, defineProps, onMounted } from 'vue';
import axios from 'axios';

const props = defineProps({
  initialMessage: {
    type: String,
    default: "Dobrodošli! Kako možemo da vam pomognemo?"
  }
});

// State for controlling the chat visibility
const isChatOpen = ref(true);
const newMessage = ref('');
const messages = ref([
  {
    from: 'admin',
    avatar: 'https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava1-bg.webp',
    text: props.initialMessage || "Dobrodošli! Kako možemo da vam pomognemo?",
    image: null
  }
]);

// Function to send a new message
const sendMessage = async () => {
  if (newMessage.value.trim()) {
    // Dodaj korisničku poruku u chat
    messages.value.push({
      from: 'user',
      avatar: 'https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava2-bg.webp',
      text: newMessage.value,
      image: null
    });

    // Očisti poruku od eventualnih novih redova
    const cleanedMessage = newMessage.value.replace(/\n/g, ' ').trim(); // ukloni nove redove

    try {
      // Pošaljite poruku Rasa serveru
      const response = await axios.post('http://localhost:5005/webhooks/rest/webhook', {
        sender: 'user',
        message: cleanedMessage
      });

      // Proveri odgovor od Rasa servera
      console.log(response.data);  // Proveri šta tačno server odgovara

      // Dodaj Rasa odgovor u chat
      response.data.forEach((message: any) => {
        messages.value.push({
          from: 'admin',
          avatar: 'https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava1-bg.webp',
          text: message.text,
          image: null
        });
      });
    } catch (error) {
      console.error('Error sending message to Rasa:', error);
    }

    // Očisti unos nakon slanja
    newMessage.value = '';

    // Spremi ažuriranu listu poruka u localStorage
    localStorage.setItem('chatMessages', JSON.stringify(messages.value));
  }
};

// Function to toggle chat visibility
const toggleChat = () => {
  isChatOpen.value = !isChatOpen.value;
};

// Učitavanje poruka iz localStorage prilikom inicijalizacije
onMounted(() => {
  const savedMessages = localStorage.getItem('chatMessages');
  if (savedMessages) {
    messages.value = JSON.parse(savedMessages);
  }
});
</script>

<template>
  <section style="background-color: #eee;">
    <div class="container py-5">

      <!-- Chat Container, will toggle between full view and minimized -->
      <div v-if="isChatOpen" class="row d-flex justify-content-center">
        <div class="col-md-8 col-lg-6 col-xl-4">
          <div class="card" id="chat1" style="border-radius: 15px;">
            <div class="card-header" @click="toggleChat">
              <i class="fas fa-angle-left"></i>
              <p class="mb-0 fw-bold">Petstore</p>
              <i class="fas fa-times"></i>
            </div>
            <div class="card-body">
              <div v-for="(message, index) in messages" :key="index" :class="message.from === 'user' ? 'message-user' : 'message-admin'">
                <img :src="message.avatar" alt="avatar" class="avatar" />
                <div :class="['message-content', message.from === 'user' ? 'bg-info' : 'bg-light']">
                  <p class="small mb-0">{{ message.text }}</p>
                  <div v-if="message.image">
                    <img :src="message.image" class="message-image" alt="image" />
                  </div>
                </div>
              </div>

              <!-- Message input -->
              <div class="form-outline">
                <textarea v-model="newMessage" class="form-control" rows="4"></textarea>
                <label class="form-label">Type your message</label>
              </div>

              <!-- Send button -->
              <button @click="sendMessage" class="btn btn-primary mt-2">Send</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Minimized Chatbox -->
      <div v-else class="chat-minimized" @click="toggleChat">
        <i class="fas fa-comment"></i>
      </div>

    </div>
  </section>
</template>

<style scoped>
/* Basic styles to replace Bootstrap */
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.row {
  display: flex;
  justify-content: center;
}

.card {
  border-radius: 15px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.card-header {
  background-color: #39c0ed;
  color: white;
  padding: 10px 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  border-top-left-radius: 15px;
  border-top-right-radius: 15px;
}

.card-body {
  padding: 20px;
}

.message-user,
.message-admin {
  display: flex;
  margin-bottom: 20px;
}

.message-user {
  justify-content: flex-start;
}

.message-admin {
  justify-content: flex-end;
}

.avatar {
  width: 45px;
  height: 45px;
  border-radius: 50%;
}

.message-content {
  max-width: 70%;
  padding: 10px;
  border-radius: 10px;
}

.bg-info {
  background-color: #39c0ed;
  color: white;
}

.bg-light {
  background-color: #f0f0f0;
  color: #333;
}

.message-image {
  width: 100%;
  border-radius: 10px;
  margin-top: 10px;
}

.form-outline {
  position: relative;
  margin-top: 20px;
}

.form-control {
  width: 100%;
  padding: 10px;
  border-radius: 10px;
  border: 1px solid #ccc;
  font-size: 14px;
  resize: none;
}

.form-label {
  position: absolute;
  top: -10px;
  left: 10px;
  background-color: white;
  padding: 0 5px;
  font-size: 12px;
  color: #aaa;
}

.btn {
  background-color: #39c0ed;
  color: white;
  border-radius: 5px;
  padding: 8px 15px;
  cursor: pointer;
}

.btn:hover {
  background-color: #317c9b;
}

/* Styles for minimized chatbox */
.chat-minimized {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #39c0ed;
  color: white;
  padding: 10px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 24px;
}
</style>
