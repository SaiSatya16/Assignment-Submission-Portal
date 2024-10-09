const Home = Vue.component("home", {
    template: `
      <div class="main-container d-flex flex-column min-vh-100">
        <div class="flex-grow-1 d-flex align-items-center justify-content-center">
          <div class="content-container p-5 rounded">
            <h1 class="text-center mb-4" style="color: #41B3A3;">Assignment Submission Portal</h1>
            <h2 class="text-center mb-3" style="color: #085F63;">Sai Satya Narayana Jonnalagadda</h2>
            <div class="row justify-content-center">
              <div class="col-md-4 mb-3">
                <router-link to="/userlogin" class="btn btn-primary btn-lg btn-block">User Login</router-link>
              </div>
              <div class="col-md-4 mb-3">
                <router-link to="/adminlogin" class="btn btn-secondary btn-lg btn-block">Admin Login</router-link>
              </div>
              <div class="col-md-4 mb-3">
                <a href="/api/docs/" class="btn btn-info btn-lg btn-block">API Documentation</a>
              </div>
            </div>
            <div class="row justify-content-center mt-4">
              <div class="col-md-4 mb-3">
                <a href="https://drive.google.com/file/d/1Q6vLtvZDBiOLlxGnxCnI8JnyngMhaqpS/view?usp=sharing" 
                   target="_blank" rel="noopener noreferrer" 
                   class="btn btn-success btn-lg btn-block">View my resume</a>
              </div>
              <div class="col-md-4 mb-3">
                <a href="https://github.com/SaiSatya16/Assignment-Submission-Portal" 
                   target="_blank" rel="noopener noreferrer" 
                   class="btn btn-dark btn-lg btn-block">Source code</a>
              </div>
            </div>
                    </div>
        </div>
        <footer class="bg-light py-3 mt-auto">
          <div class="container text-center">
            <a href="https://github.com/SaiSatya16" target="_blank" rel="noopener noreferrer" class="me-3">
              <i class="fab fa-github"></i> GitHub
            </a>
            <a href="https://www.linkedin.com/in/sai-satya-jonnalagadda-157900225/" target="_blank" rel="noopener noreferrer">
              <i class="fab fa-linkedin"></i> LinkedIn
            </a>
          </div>
        </footer>
      </div>
    `,
  });
  
  export default Home;