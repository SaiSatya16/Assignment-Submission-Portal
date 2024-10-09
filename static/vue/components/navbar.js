const Navbar = Vue.component('navbar', {
    template: 
    `
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="/" style="color: #41B3A3; font-weight: bold;">GrowthX</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav ms-auto">
          <router-link to="/" class="nav-link" active-class="active">Home</router-link>
          <router-link to="/about" class="nav-link" active-class="active">About</router-link>
          <a href="#" @click.prevent="logout" class="nav-link">Logout</a>
        </div>
      </div>
    </div>
  </nav>
    
    `,
    data() {
        return {
          is_login: localStorage.getItem("token"),
          inactivityTimeout: 30 * 60 * 1000, // 30 minutes in milliseconds
          inactivityTimer: null,
        };
      },
      methods: {
        logout() {
          localStorage.removeItem("token");
          this.$router.push({ path: "/home" });
        },
        handleUserActivity() {
          localStorage.setItem("lastActivityTimestamp", Date.now().toString());
        },
        checkInactivity() {
          const lastActivityTimestamp = localStorage.getItem("lastActivityTimestamp");
          const currentTime = Date.now();
    
          if (lastActivityTimestamp && currentTime - lastActivityTimestamp > this.inactivityTimeout) {
            this.clearLocalStorage();
          }
        },
        clearLocalStorage() {
            localStorage.removeItem("token");
            this.$router.push({ path: "/home" });
        },
        startInactivityTimer() {
          this.inactivityTimer = setInterval(() => {
            this.checkInactivity();
          }, 60000); // Check every minute
        },
        stopInactivityTimer() {
          clearInterval(this.inactivityTimer);
        },
      },
      mounted() {
        document.addEventListener("mousemove", this.handleUserActivity);
        document.addEventListener("keydown", this.handleUserActivity);
        this.startInactivityTimer();
      },
      beforeDestroy() {
        document.removeEventListener("mousemove", this.handleUserActivity);
        document.removeEventListener("keydown", this.handleUserActivity);
        this.stopInactivityTimer();
      },
    });
    
    export default Navbar;