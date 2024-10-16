# Assignment Submission Portal

This is a Flask-RESTful application that provides an API for an assignment submission portal. It allows users to upload assignments and admins to review them. The application uses MongoDB Atlas as its database and incorporates JWT for authentication.

## Features

- User and Admin authentication using JWT
- Assignment submission by users
- Assignment review (accept/reject) by admins
- MongoDB Atlas integration for data storage
- Input validation using Marshmallow schemas
- Comprehensive error handling and logging
- Unit tests for all major functionalities
- Vue.js frontend for user interaction

### Application currently live at [Assignment Submission Portal](http://satya.ap-south-1.elasticbeanstalk.com)

### API Documentation available at [API Documentation](http://satya.ap-south-1.elasticbeanstalk.com/api/docs/)

- deployed on AWS Elastic Beanstalk and MongoDB Atlas cloud services.
- The application is secured with JWT tokens and has separate routes for users and admins.
- Employed aws codepipeline for CI/CD pipeline to deploy the application on AWS Elastic Beanstalk connected to the GitHub repository.

## Screenshots

### Home Page
![Home Page](screenshots/Screenshot2.png)

### API Documentation
![API Documentation](screenshots/Screenshot1.png)

### User Dashboard
![User Dashboard](screenshots/Screenshot3.png)

### Admin Dashboard
![Admin Dashboard](screenshots/Screenshot4.png)


## Prerequisites

- Python 3.7+
- MongoDB Atlas account
- Git (for cloning the repository)

## Setup

1. Clone this repository:

```bash 
git clone https://github.com/SaiSatya16/Assignment-Submission-Portal
cd Assignment-Submission-Portal
```

2. Create a virtual environment and activate it:
```bash 
python -m venv venv
source venv/bin/activate
```
- On Windows, use `venv\Scripts\activate`

3. Install the required packages:
```bash 
pip install -r requirements.txt
```


4. Set up environment variables:

- currently, database is hosted on MongoDB Atlas, so you can skip this step and go ahead with the next step to run the application on my database which is already hosted on MongoDB Atlas
- If you want to host the database on your own, then follow the below steps:

- In `config.py` file make the changes with the following contents:
```bash 
MONGO_URI = mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/assignment_portal
JWT_SECRET_KEY=`your-secret-key`
FLASK_DEBUG=False
```
- Replace `<username>`, `<password>`, and `<cluster-name>` with your actual MongoDB Atlas credentials.

5. Ensure your IP address is whitelisted in MongoDB Atlas.

6. Run the application:

```bash
python app.py
```

## Project Structure
```bash
    ASSIGNMENT_PORTAL/
    ├── models/
    │   ├── __pycache__/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── assignment.py
    │   └── user.py
    ├── resources/
    │   ├── __pycache__/
    │   ├── __init__.py
    │   ├── admin.py
    │   └── user.py
    ├── static/
    │   └── vue/
    │       ├── components/
    │       │   ├── about.js
    │       │   ├── adminhome.js
    │       │   ├── AdminLogin.js
    │       │   ├── AdminRegister.js
    │       │   ├── home.js
    │       │   ├── navbar.js
    │       │   ├── userhome.js
    │       │   ├── userlogin.js
    │       │   └── UserRegister.js
    │       ├── index.js
    │       └── router.js
    ├── templates/
    │   └── index.html
    ├── .gitignore
    ├── app.log
    ├── app.py
    ├── config.py
    ├── extensions.py
    ├── README.md
    ├── requirements.txt
    ├── schemas.py
    └── tests.py
```

## API Endpoints

### User Endpoints

- `POST /register`: Register a new user
  - Body: `{"username": "string", "password": "string"}`

- `POST /login`: User login
  - Body: `{"username": "string", "password": "string"}`

- `POST /upload`: Upload an assignment (requires authentication)
  - Body: `{"task": "string", "admin": "string"}`
  - Headers: `Authorization: Bearer <access_token>`

- `GET /admins`: Get list of admins (requires authentication)
  - Headers: `Authorization: Bearer <access_token>`

### Admin Endpoints

- `POST /admin/register`: Register a new admin
  - Body: `{"username": "string", "password": "string"}`

- `POST /admin/login`: Admin login
  - Body: `{"username": "string", "password": "string"}`

- `GET /assignments`: View assignments (admin only, requires authentication)
  - Headers: `Authorization: Bearer <access_token>`

- `POST /assignments/:id/accept`: Accept an assignment (admin only, requires authentication)
  - Headers: `Authorization: Bearer <access_token>`

- `POST /assignments/:id/reject`: Reject an assignment (admin only, requires authentication)
  - Headers: `Authorization: Bearer <access_token>`

## Running Tests

To run the unit tests:

1. Ensure you're in the project root directory and your virtual environment is activated.

2. Run the following command:

```bash
python -m unittest tests.py
```

This will run all the unit tests and display the results in the console.

## Logging

The application logs are stored in `app.log` in the root directory. The log file is rotated when it reaches 10,000 bytes, keeping a maximum of 3 backup files.

## Troubleshooting

If you're having trouble connecting to MongoDB Atlas:

1. Double-check your `config.py` file. Make sure your `MONGO_URI` is correctly formatted and all placeholders are replaced with your actual MongoDB Atlas credentials.

2. Ensure your IP address is whitelisted in MongoDB Atlas.

3. Check that your database user has the correct permissions.

4. Verify that your cluster is fully deployed and running in the Atlas dashboard.

5. If you're still having issues, check the `app.log` file for more detailed error messages.

## Security Considerations

- JWT tokens expire after 1 hour. For longer sessions, implement a refresh token mechanism.
- All passwords are hashed before being stored in the database.
- Sensitive information is stored in environment variables, not in the code.
- Input validation is performed on all user inputs to prevent injection attacks.

## Future Improvements

- Implement refresh tokens for prolonged sessions without requiring re-authentication.
- Add password reset functionality.
- Implement rate limiting to prevent abuse of the API.
- Add more detailed user profiles and assignment metadata.
- Implement file storage for assignment uploads (e.g., AWS S3).