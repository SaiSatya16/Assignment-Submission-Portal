// File: static/vue/components/AdminDashboard.js
const adminhome = {
    data() {
      return {
        assignments: [],
        error: '',
        success: ''
      };
    },
    mounted() {
      this.fetchAssignments();
    },
    methods: {
      async fetchAssignments() {
        try {
          const response = await fetch('/assignments', {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          });
          const data = await response.json();
          if (response.ok) {
            this.assignments = data.assignments;
            console.log(data.assignments);
          } else {
            this.error = data.message;
          }
        } catch (error) {
          this.error = 'An error occurred while fetching assignments.';
        }
      },
      async updateAssignmentStatus(id, status) {
        try {
          const response = await fetch(`/assignments/${id}/${status}`, {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          });
          const data = await response.json();
          if (response.ok) {
            this.success = `Assignment ${status} successfully.`;
            this.fetchAssignments();
          } else {
            this.error = data.message;
          }
        } catch (error) {
          this.error = `An error occurred while ${status}ing the assignment.`;
        }
      }
    },
    template: `
      <div class="container mt-5">
        <h2 class="text-center mb-4">Admin Dashboard</h2>
        <div v-if="assignments.length > 0">
          <table class="table">
            <thead>
              <tr>
                <th>User ID</th>
                <th>Name</th>
                <th>Task</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="assignment in assignments" :key="assignment._id">
                <td>{{ assignment.user_id }}</td>
                <td>{{ assignment.user_name }}</td>
                <td>{{ assignment.task }}</td>
                <td>{{ assignment.status }}</td>
                <td>
                  <button @click="updateAssignmentStatus(assignment._id, 'accept')" class="btn btn-success btn-sm mr-2">Accept</button>
                  <button @click="updateAssignmentStatus(assignment._id, 'reject')" class="btn btn-danger btn-sm">Reject</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else>
          <p>No assignments found.</p>
        </div>
        <p v-if="error" class="text-danger mt-3">{{ error }}</p>
        <p v-if="success" class="text-success mt-3">{{ success }}</p>
      </div>
    `
  };
  
  export default adminhome;