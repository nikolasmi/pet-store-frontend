<template>
    <header>
        <router-link to="/"><h1>PetStore</h1></router-link>
    <div id="div-register">       
        <router-link to="/register"><img alt="login-icon" src="/icons8-register-32 (1).png"></router-link>
        <p>registracija</p>
    </div>
    <div id="div-log-in">
        <router-link to="/login"><img alt="login-icon" src="/icons8-log-in-30.png"></router-link>
        <p>prijava</p>
    </div>
    <div id="div-wish">
        <router-link to="/orders/user/id"><img alt="order-icon" src="/icons8-order-30.png"></router-link>
        <p>porudžbine</p>
    </div>
    <div id="div-cart"> 
        <router-link to="/cart"><img alt="cart-icon" src="/icons8-cart-30.png"></router-link>
        <p>korpa</p>
    </div>
    <div id="div-profile">
        <router-link to="/profile/id"><img alt="login-icon" src="/icons8-name-32.png"></router-link>
        <p>moj profil</p>
    </div>
    </header>
</template>

<style scoped>
    @import "../assets/home.css";
</style>