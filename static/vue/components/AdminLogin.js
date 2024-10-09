// File: static/vue/components/AdminLogin.js
const AdminLogin = {
    data() {
      return {
        username: '',
        password: '',
        error: ''
      };
    },
    methods: {
      async login() {
        try {
          const response = await fetch('/admin/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              username: this.username,
              password: this.password
            }),
          });
          const data = await response.json();
          if (response.ok) {
            localStorage.setItem('token', data.access_token);
            this.$router.push('/adminhome');
          } else {
            this.error = data.message;
          }
        } catch (error) {
          this.error = 'An error occurred. Please try again.';
        }
      }
    },
    template: `
    <div class="container mt-5">
      <h2 class="text-center mb-4">Admin Login</h2>
      <div class="row justify-content-center">
        <div class="col-md-6">
          <form @submit.prevent="login">
            <div class="form-group">
              <label for="username">Username:</label>
              <input type="text" class="form-control" id="username" v-model="username" required>
            </div>
            <div class="form-group">
              <label for="password">Password:</label>
              <input type="password" class="form-control" id="password" v-model="password" required>
            </div>
            <button type="submit" class="btn btn-primary btn-block mt-3">Login</button>
          </form>
          <p v-if="error" class="text-danger mt-3">{{ error }}</p>
          <p class="mt-3 text-center">
            Don't have an account? <router-link to="/admin-register">Register as new admin</router-link>
          </p>
        </div>
      </div>
    </div>
    `
  };
  
  export default AdminLogin;