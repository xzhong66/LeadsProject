# Leads Management Application

This is a Lead Management application built with FastAPI and SQLite. It allows you to create, retrieve, and update leads through a RESTful API.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository
2. Navigate to the project directory
3. Create a virtual environment if you want to: `python3 -m venv venv`
4. Activate the virtual environment: `source venv/bin/activate`
5. Install the required dependencies: `pip install -r requirements.txt`

## Running the Application
To run the application, use the following command:
`uvicorn app.main:app --reload`

The application will start running at http://localhost:8000.

## API Endpoints
- `POST /leads`: Create a new lead
- `GET /leads`: Retrieve all leads (requires authentication).
- `GET /leads/{lead_id}`: Retrieve a specific lead by ID (requires authentication).
- `PATCH /leads/{lead_id}`: Update the state of a lead (requires authentication).
- `POST /leads/login`: Generate a JWT token for authentication.

## Testing the API Endpoints
I use Postman to test the APIs.

### Create a lead
1. Set the URL to `http://localhost:8000/leads`.
2. Select the "Body" tab and choose the "raw" format.
3. Set the content type to "JSON" in the dropdown menu.
4. Enter the following JSON payload in the request body:
``` json
{
    "first_name": "your firsr name",
    "last_name": "your last name",
    "email": "your email",
    "resume": "your resume contents"
}
```
5. Send the **POST** request and verify that you receive a 201 Created response with the created lead data.

### Log in
1. Set URL to `http://localhost:8000/leads/login`.
2. Select the "Body" tab and choose the "form-data" format. Add two key-value pairs: "username" with the value "attorney@company.com" and "password" with the value "password".
I hard coded these values in the code. It should be improved with a sign-up mechanism.
3. Send the **POST** request and verify that you receive a 200 OK response with the JWT token.
4. Copy the JWT token from the response. Keep it somewhere, it will expire after 30 minutes.

### Get all leads
1. Set the URL to `http://localhost:8000/leads`.
2. Select the "Authorization" tab and choose "Bearer Token" from the dropdown menu.
3. Paste the JWT token in the "Token" field.
4. Send the **GET** request and verify that you now receive a 200 OK response with a list of leads you created before.

### Get a specific lead by ID
1. Set the URL to `http://localhost:8000/leads/{lead_id}`, replacing {lead_id} with the actual ID of a lead you want to retrieve.
2. The remaining steps are the same with steps in **Get all leads** section.

### Update lead state
1. Set the URL to `http://localhost:8000/leads/{lead_id}`, replacing {lead_id} with the actual ID of a lead you want to retrieve.
2. Select the "Authorization" tab and choose "Bearer Token" from the dropdown menu.
3. Paste the JWT token in the "Token" field.
4. Select the "Body" tab and choose the "raw" format. Set the content type to "JSON" in the dropdown menu.
5. Enter the following JSON payload in the request body:
``` json
{
    "state": "REACHED_OUT"
}
```
6. Send the **PATCH** request and verify that you receive a 200 OK response with the updated lead data.

## Fake email sending
The application is currently configured to use fake email sending, which means that instead of sending real emails, it will print the email details in the console.
To view the email logs, check the console output when creating a new lead. For real world implementations, we can leverage third party email services like Twilio's SendGrid.
