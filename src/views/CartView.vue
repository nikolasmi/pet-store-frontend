<template>
    <div class="cart-view p-6 max-w-4xl mx-auto bg-white rounded-lg shadow-lg">
      <h1 class="text-2xl font-semibold text-gray-800 mb-6">Vaša korpa</h1>
      <div v-if="cart && cart.cartPets.length > 0">
        <div v-for="item in cart.cartPets" :key="item.cartPetId" class="cart-item flex items-center justify-between border-b pb-4 mb-4">
          <div class="flex items-center">
            <div class="item-image">
              <img :src="`/${item.pet.imagePath}`" alt="pet image" class="w-20 h-20 object-cover rounded-md shadow-md" />
            </div>
            <div class="item-details ml-6">
              <h3 class="text-lg font-medium text-gray-800">{{ item.pet.name }}</h3>
              <p class="text-sm text-gray-500">{{ item.pet.description }}</p>
              <p class="price text-red-500">{{ item.pet.price }} USD</p>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <input
                type="number"
                v-model="item.quantity"
                min="1"
                step="1"
                @input="updateQuantity(item.cartPetId, item.quantity)"
            />
            <button @click="removeFromCart(item.cartPetId)" class="remove-btn bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-md font-semibold transition duration-200">Obriši</button>
          </div>
        </div>
        <div class="cart-summary mt-6 flex justify-between items-center">
          <p class="total-price text-xl font-semibold text-gray-900">Ukupno: {{ totalPrice }} USD</p>
          <button @click="checkout" class="checkout-btn bg-green-600 hover:bg-green-700 text-white py-2 px-6 rounded-md font-semibold transition duration-200">Naruči</button>
        </div>
      </div>
      <div v-else class="empty-cart-message">
        <p>Vaša korpa je prazna. Dodajte proizvode kako biste započeli kupovinu.</p>
        <a href="/">Idi u prodavnicu</a>
      </div>
    </div>
</template>
  
<script setup>
    import { ref, onMounted } from 'vue';
    import axios from 'axios';
  
    const cart = ref(null);
    const totalPrice = ref(0);
  
    const token = localStorage.getItem('token');
  
    const fetchCart = async () => {
        try {
            const response = await axios.get('http://localhost:3000/api/cart', {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });
            cart.value = response.data;
            
            // Postavi količinu na 1 ako nije postavljena
            cart.value.cartPets.forEach(item => {
                if (item.quantity === undefined || item.quantity === 0) {
                    item.quantity = 1;
                }
            });

            // Ažuriraj ukupnu cenu
            calculateTotalPrice();
        } catch (error) {
            console.error('Greška pri učitavanju korpe:', error);
        }
    };
  
    const updateQuantity = async (cartPetId, newQuantity) => {
        try {
            // Ažuriraj količinu na serveru
            await axios.patch('http://localhost:3000/api/cart', {
                cartPetId,
                quantity: newQuantity,
            }, {
                headers: {
                    Authorization: `Bearer ${token}`, 
                },
            });
            
            // Ažuriraj ukupnu cenu
            calculateTotalPrice();
        } catch (error) {
            console.error('Greška pri ažuriranju količine:', error);
        }
    };
  
    const removeFromCart = async (cartPetId) => {
      try {
        await axios.delete(`http://localhost:3000/api/cart/${cartPetId}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        fetchCart();
      } catch (error) {
        console.error('Greška pri brisanju proizvoda:', error);
      }
    };
  
    const calculateTotalPrice = () => {
        if (cart.value) {
            totalPrice.value = cart.value.cartPets.reduce(
            (acc, item) => acc + item.pet.price * item.quantity, 0);
        } 
    };
    
    const checkout = async () => {
        try {
            // Pošaljite totalPrice zajedno sa ostalim podacima kada kreirate porudžbinu
            await axios.post('http://localhost:3000/api/cart/makeOrder', 
            { totalPrice: totalPrice.value },  // Dodajte totalPrice ovde
            {
                headers: {
                Authorization: `Bearer ${token}`
                }
            }
            );
            alert('Porudžbina je uspešno kreirana!');
        } catch (error) {
            console.error('Greška pri kreiranju porudžbine:', error);
        }
    };
  
    onMounted(() => {
      fetchCart();
    });
</script>
  
<style scoped>
body {
  font-family: 'Roboto', sans-serif;
  background-color: #f7f7f7;
  margin: 0;
  padding: 0;
}

.cart-view {
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  color: #333;
  font-weight: 700;
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
}

.cart-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.item-image img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.item-details {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.item-details h3 {
  margin: 0;
  color: #333;
  font-weight: 500;
}

.item-details .price {
  color: #e74c3c;
  font-weight: 700;
  margin: 5px 0;
}

.item-details p {
  margin: 5px 0;
}

.quantity-input {
  width: 60px;
  padding: 5px;
  border: 1px solid #ddd;
  text-align: center;
}

.remove-btn {
  background-color: #e74c3c;
  color: #fff;
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.remove-btn:hover {
  background-color: #c0392b;
}

.checkout-btn {
  background-color: #27ae60;
  color: #fff;
  padding: 12px 30px;
  border: none;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.checkout-btn:hover {
  background-color: #219150;
}

.cart-summary {
  padding: 20px;
  border-top: 2px solid #eee;
  text-align: center;
}

.cart-summary h2 {
  margin-top: 0;
  font-weight: 700;
  margin-bottom: 10px;
}

.cart-summary p {
  margin: 5px 0;
  font-weight: 500;
}

.cart-summary {
  font-size: 1rem;
  background-color: #ffffff;
  padding: 1.25rem;
}

.cart-summary h2 {
  font-size: 1.25rem;
  color: #2d3748;
}

.cart-summary p {
  color: #718096;
  font-size: 1rem;
}

.checkout-btn {
  background-color: #2b6cb0;
  color: white;
  border-radius: 0.375rem;
  padding: 0.75rem 2rem;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.875rem;
  transition: all 0.3s ease;
}

.checkout-btn:hover {
  background-color: #3182ce;
  transform: translateY(-2px);
}

.remove-btn {
  background-color: #e53e3e;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 600;
  color: white;
  cursor: pointer;
}

.remove-btn:hover {
  background-color: #c53030;
}

.cart-item {
  padding: 1rem 0;
  border-bottom: 1px solid #edf2f7;
}

.item-image img {
  width: 4rem;
  height: 4rem;
  object-fit: cover;
  border-radius: 0.375rem;
}

.empty-cart-message {
    display: flex; 
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    background-color: #f9f9f9; 
    border: 2px dashed #d1d5db; 
    border-radius: 8px; 
    text-align: center;
    color: #4b5563; 
    font-size: 1.125rem; 
}

.empty-cart-message p {
    margin-bottom: 1rem; 
}

.empty-cart-message a {
    display: inline-block;
    padding: 0.5rem 1rem;
    background-color: #10b981; 
    color: #fff; 
    font-weight: 600; 
    text-decoration: none; 
    border-radius: 4px; 
    transition: background-color 0.3s; 
}

.empty-cart-message a:hover {
    background-color: #059669; 
}
</style>
  