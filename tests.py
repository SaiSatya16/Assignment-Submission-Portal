import unittest
from app import create_app
from extensions import mongo
import json
import logging
import sys

class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        # Set up logging
        cls.logger = logging.getLogger('TestApp')
        cls.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        cls.logger.addHandler(handler)

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()
        mongo.cx.close()  # Close the MongoClient

    def setUp(self):
        with self.app.app_context():
            mongo.db.users.delete_many({})
            mongo.db.admins.delete_many({})
            mongo.db.assignments.delete_many({})

    def tearDown(self):
        pass

    def test_user_registration(self):
        response = self.client.post('/register', json={'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User created successfully', response.data)

    def test_user_login(self):
        self.client.post('/register', json={'username': 'testuser', 'password': 'testpass'})
        response = self.client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'access_token', response.data)

    def test_admin_registration(self):
        response = self.client.post('/admin/register', json={'username': 'testadmin', 'password': 'testpass'})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Admin created successfully', response.data)

    def test_admin_login(self):
        self.client.post('/admin/register', json={'username': 'testadmin', 'password': 'testpass'})
        response = self.client.post('/admin/login', json={'username': 'testadmin', 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'access_token', response.data)

    def test_get_admin_list(self):
        self.client.post('/admin/register', json={'username': 'testadmin', 'password': 'testpass'})
        self.client.post('/register', json={'username': 'testuser', 'password': 'testpass'})
        
        login_response = self.client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
        access_token = json.loads(login_response.data)['access_token']
        
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.get('/admins', headers=headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'testadmin', response.data)

    def test_upload_assignment(self):
        self.client.post('/register', json={'username': 'testuser', 'password': 'testpass'})
        self.client.post('/admin/register', json={'username': 'testadmin', 'password': 'testpass'})
        
        login_response = self.client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
        access_token = json.loads(login_response.data)['access_token']
        
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.post('/upload', json={'task': 'Test assignment', 'admin': 'testadmin'}, headers=headers)
        
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertIn('message', response_data)
        self.assertIn('assignment_id', response_data)
        
        self.assertEqual(response_data['message'], 'Assignment uploaded successfully.')


    def test_get_assignments(self):
        self.client.post('/admin/register', json={'username': 'testadmin', 'password': 'testpass'})
        self.client.post('/register', json={'username': 'testuser', 'password': 'testpass'})
        
        user_login = self.client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
        user_token = json.loads(user_login.data)['access_token']
        
        admin_login = self.client.post('/admin/login', json={'username': 'testadmin', 'password': 'testpass'})
        admin_token = json.loads(admin_login.data)['access_token']
        
        # Upload an assignment
        upload_response = self.client.post('/upload', json={'task': 'Test assignment', 'admin': 'testadmin'}, 
                                        headers={'Authorization': f'Bearer {user_token}'})
        self.assertEqual(upload_response.status_code, 201)
        
        # Get assignments
        response = self.client.get('/assignments', headers={'Authorization': f'Bearer {admin_token}'})
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('assignments', response_data)
        # self.assertGreater(len(response_data['assignments']), 0)
        # self.assertEqual(response_data['assignments'][0]['task'], 'Test assignment')



    def test_accept_assignment(self):
        self.logger.debug("Starting test_accept_assignment")
        
        # Register admin and user
        admin_response = self.client.post('/admin/register', json={'username': 'testadmin', 'password': 'testpass'})
        self.logger.debug(f"Admin registration response: {admin_response.data}")
        
        user_response = self.client.post('/register', json={'username': 'testuser', 'password': 'testpass'})
        self.logger.debug(f"User registration response: {user_response.data}")
        
        # Login as user
        user_login = self.client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
        user_token = json.loads(user_login.data)['access_token']
        self.logger.debug(f"User login token: {user_token}")
        
        # Login as admin
        admin_login = self.client.post('/admin/login', json={'username': 'testadmin', 'password': 'testpass'})
        admin_token = json.loads(admin_login.data)['access_token']
        self.logger.debug(f"Admin login token: {admin_token}")
        
        # Upload an assignment
        upload_response = self.client.post('/upload', json={'task': 'Test assignment', 'admin': 'testadmin'},
                                        headers={'Authorization': f'Bearer {user_token}'})
        self.logger.debug(f"Upload response: {upload_response.data}")
        self.assertEqual(upload_response.status_code, 201)
        
        upload_data = json.loads(upload_response.data)
        assignment_id = upload_data.get('assignment_id')
        self.logger.debug(f"Uploaded assignment ID: {assignment_id}")
        
        self.assertIsNotNone(assignment_id)
        
        response = self.client.post(f'/assignments/{assignment_id}/accept', 
                                    headers={'Authorization': f'Bearer {admin_token}'})
        
        self.logger.debug(f"Accept response: {response.data}")
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Assignment accepted successfully', response.data)

    def test_reject_assignment(self):
        self.logger.debug("Starting test_reject_assignment")
        
        # Register admin and user
        admin_response = self.client.post('/admin/register', json={'username': 'testadmin', 'password': 'testpass'})
        self.logger.debug(f"Admin registration response: {admin_response.data}")
        
        user_response = self.client.post('/register', json={'username': 'testuser', 'password': 'testpass'})
        self.logger.debug(f"User registration response: {user_response.data}")
        
        # Login as user
        user_login = self.client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
        user_token = json.loads(user_login.data)['access_token']
        self.logger.debug(f"User login token: {user_token}")
        
        # Login as admin
        admin_login = self.client.post('/admin/login', json={'username': 'testadmin', 'password': 'testpass'})
        admin_token = json.loads(admin_login.data)['access_token']
        self.logger.debug(f"Admin login token: {admin_token}")
        
        # Upload an assignment
        upload_response = self.client.post('/upload', json={'task': 'Test assignment', 'admin': 'testadmin'},
                                        headers={'Authorization': f'Bearer {user_token}'})
        self.logger.debug(f"Upload response: {upload_response.data}")
        self.assertEqual(upload_response.status_code, 201)
        
        upload_data = json.loads(upload_response.data)
        assignment_id = upload_data.get('assignment_id')
        self.logger.debug(f"Uploaded assignment ID: {assignment_id}")
        
        self.assertIsNotNone(assignment_id)
        
        response = self.client.post(f'/assignments/{assignment_id}/reject', 
                                    headers={'Authorization': f'Bearer {admin_token}'})
        
        self.logger.debug(f"Reject response: {response.data}")
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Assignment rejected successfully', response.data)
if __name__ == '__main__':
    unittest.main()