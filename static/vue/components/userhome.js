// File: static/vue/components/UserDashboard.js
const userhome = {
    data() {
      return {
        task: '',
        admin: '',
        admins: [],
        error: '',
        success: ''
      };
    },
    mounted() {
      this.fetchAdmins();
    },
    methods: {
      async fetchAdmins() {
        try {
          const response = await fetch('/admins', {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          });
          const data = await response.json();
          if (response.ok) {
            this.admins = data.admins;
          } else {
            this.error = data.message;
          }
        } catch (error) {
          this.error = 'An error occurred while fetching admins.';
        }
      },
      async uploadAssignment() {
        try {
          const response = await fetch('/upload', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
              task: this.task,
              admin: this.admin
            }),
          });
          const data = await response.json();
          if (response.ok) {
            this.success = 'Assignment uploaded successfully.';
            this.task = '';
            this.admin = '';
          } else {
            this.error = data.message;
          }
        } catch (error) {
          this.error = 'An error occurred while uploading the assignment.';
        }
      }
    },
    template: `
      <div class="container mt-5">
        <h2 class="text-center mb-4">User Dashboard</h2>
        <div class="row justify-content-center">
          <div class="col-md-6">
            <form @submit.prevent="uploadAssignment">
              <div class="form-group">
                <label for="task">Task:</label>
                <textarea class="form-control" id="task" v-model="task" required></textarea>
              </div>
              <div class="form-group">
                <label for="admin">Select Admin:</label>
                <select class="form-control" id="admin" v-model="admin" required>
                  <option value="">Select an admin</option>
                  <option v-for="adminName in admins" :key="adminName" :value="adminName">{{ adminName }}</option>
                </select>
              </div>
              <button type="submit" class="btn btn-primary btn-block mt-3">Upload Assignment</button>
            </form>
            <p v-if="error" class="text-danger mt-3">{{ error }}</p>
            <p v-if="success" class="text-success mt-3">{{ success }}</p>
          </div>
        </div>
      </div>
    `
  };
  
  export default userhome;