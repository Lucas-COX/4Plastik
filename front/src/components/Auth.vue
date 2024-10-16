<template>
    <div class="login-container">
      <h2>Connexion au service</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Nom d'utilisateur</label>
          <input type="text" v-model="username" id="username" required />
        </div>
        <div class="form-group">
          <label for="password">Mot de passe</label>
          <input type="password" v-model="password" id="password" required />
        </div>
        <button type="submit">Se connecter</button>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LoginPage',
    data() {
      return {
        username: '',
        password: '',
        errorMessage: ''
      };
    },
    methods: {
      async handleLogin() {
        const resp = await fetch(`${import.meta.env.VITE_API_URL}/token`, {
          method: 'POST',
          body: JSON.stringify({
            username: this.username,
            password: this.password,
          }),
          headers: {
            "Content-Type": "application/json"
          }
        })
        if (resp.ok) {
          const data = await resp.json();
          localStorage.setItem('token', data.access_token);
          this.$router.push({ name: 'test' });
        } else {
          this.errorMessage = "Nom d'utilisateur ou mot de passe incorrect.";
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .login-container {
    max-width: 400px;
    margin: 50px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #f9f9f9;
  }
  .form-group {
    margin-bottom: 15px;
  }
  label {
    display: block;
    margin-bottom: 5px;
  }
  input {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
  }
  button {
    width: 100%;
    padding: 10px;
    background-color: #42b983;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  button:hover {
    background-color: #369f74;
  }
  .error-message {
    color: red;
    margin-top: 10px;
  }
  </style>
  
