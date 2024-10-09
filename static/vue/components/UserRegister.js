// File: static/vue/components/UserRegister.js
const UserRegister = {
    data() {
      return {
        username: '',
        password: '',
        confirmPassword: '',
        error: '',
        success: ''
      };
    },
    methods: {
      async register() {
        if (this.password !== this.confirmPassword) {
          this.error = "Passwords do not match.";
          return;
        }
        try {
          const response = await fetch('/register', {
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
            this.success = "Registration successful. You can now log in.";
            this.error = '';
            // Optionally, redirect to login page after a delay
            setTimeout(() => this.$router.push('/userlogin'), 2000);
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
        <h2 class="text-center mb-4">User Registration</h2>
        <div class="row justify-content-center">
          <div class="col-md-6">
            <form @submit.prevent="register">
              <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" class="form-control" id="username" v-model="username" required>
              </div>
              <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" class="form-control" id="password" v-model="password" required>
              </div>
              <div class="form-group">
                <label for="confirmPassword">Confirm Password:</label>
                <input type="password" class="form-control" id="confirmPassword" v-model="confirmPassword" required>
              </div>
              <button type="submit" class="btn btn-primary btn-block mt-3">Register</button>
            </form>
            <p v-if="error" class="text-danger mt-3">{{ error }}</p>
            <p v-if="success" class="text-success mt-3">{{ success }}</p>
            <p class="mt-3 text-center">
              Already have an account? <router-link to="/userlogin">Login</router-link>
            </p>
          </div>
        </div>
      </div>
    `
  };
  
  export default UserRegister;