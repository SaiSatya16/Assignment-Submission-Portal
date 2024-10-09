const home = Vue.component("home", {
    template: `
    <div class="container mt-5">
    <h1 class="text-center mb-4">Assignment Submission Portal</h1>
    <div class="row justify-content-center">
      <div class="col-md-4">
        <router-link to="/userlogin" class="btn btn-primary btn-lg btn-block mb-3">User Login</router-link>
      </div>
      <div class="col-md-4">
        <router-link to="/adminlogin" class="btn btn-secondary btn-lg btn-block">Admin Login</router-link>
      </div>
    </div>
  </div>
    `,
  });
  
  export default home;