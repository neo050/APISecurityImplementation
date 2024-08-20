# API Security Implementation
 
## Overview

This project is focused on implementing a secure RESTful API using Flask, with JWT-based authentication and authorization. The API ensures that only authorized users can access protected resources, providing a robust foundation for secure web applications.

## Features

- **JWT Authentication:** Users can log in and receive a JWT token that is used to authenticate subsequent requests.
- **Protected Routes:** Only users with a valid JWT token can access certain API endpoints.
- **Environment Configuration:** Sensitive information, such as the secret key, is stored in environment variables.

## Prerequisites

Before you can run this project, ensure you have the following installed:

- **Python 3.7+**
- **pip** (Python package installer)
- **Virtualenv** (optional but recommended)

## Installation

### Step 1: Clone the Repository

First, clone the repository to your local machine:

bash
git clone https://github.com/neo050/APISecurityImplementation.git 

cd APISecurityImplementation

### Step 2: Set Up the Virtual Environment
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
### Step 3: Install Dependencies
pip install -r requirements.txt
### Step 4: Set Up Environment Variables
### Step 5: Run the Flask Application
python api_security_project/run.py
The application will start running at http://127.0.0.1:5000/.

Using the API
1. Obtain a JWT Token
To interact with the API, you must first obtain a JWT token by logging in:

Endpoint: POST /api/login
Request Body:
{
    "user_id": "example_user"
}
Response:
{
    "token": "your_jwt_token"
}
Copy the token from the response. This will be used to authenticate requests to protected routes.

2. Access a Protected Route
Once you have the JWT token, you can access protected routes by including the token in the Authorization header:

Endpoint: GET /api/protected
Headers:
Authorization: Bearer your_jwt_token
Response:
{
    "message": "Hello, user example_user"
}
3. Example Requests Using Postman
Login:

Method: POST
URL: http://127.0.0.1:5000/api/signup
Body (JSON):
{
    "user_id": "example_user" 
}
Access Protected Route:

Method: GET
URL: http://127.0.0.1:5000/api/login
Headers:
Authorization: Bearer your_jwt_token

Troubleshooting
    Token is Invalid: Ensure that the Authorization header is correctly formatted as Bearer your_jwt_token and that the token has not expired.
    Token is Missing: Make sure the Authorization header is included in the request when accessing protected routes.