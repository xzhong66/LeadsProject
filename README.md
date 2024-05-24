# Leads Management Application

This is a Lead Management application built with FastAPI and SQLite. It allows you to create, retrieve, and update leads through a RESTful API.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- SendGrid API key

### Create API key
1. Sign up for a SendGrid account:
Go to the SendGrid website (https://sendgrid.com) and sign up for an account.
2. Create an API key:
- After signing up and logging in to your SendGrid account, navigate to the "Settings" section.
- Click on "API Keys" in the left sidebar.
- Click on the "Create API Key" button.
- Set your API key name and permissions.
- Click on "Create & View" to generate the API key.
- Copy the generated API key and store it securely.

## Installation

1. Clone the repository
2. Navigate to the project directory
3. Create a virtual environment if you want to: `python3 -m venv venv`
4. Activate the virtual environment: `source venv/bin/activate`
5. Install the required dependencies: `pip install -r requirements.txt`
6. Create a new file named `.env` in the project root directory. Open the `.env` file and add the following code:`SENDGRID_API_KEY=<your-sendgrid-api-key>`
7. In `email.py`, replace the sender email to your SendGrid account.

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
- `GET leads/resumes/{resume_filename}`: Get the resume by file name.

## Testing the API Endpoints
I use Postman to test the APIs.

### Create a lead
1. Set the URL to `http://localhost:8000/leads`.
2. Select the "Body" tab and choose the "form-data" format.
3. Add four key-value pairs: "first_name" with the value, "last_name" with the value, "email" with the value and "resume" with a file upload. 
4. Select `File` as the field type for "resume" then upload the file you choose.
5. Send the **POST** request and verify that you receive a 201 Created response with the created lead data.
6. Additionally, you should expect to see the email sending status code to be 202 and receive an email in a while.

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

### Get resume by file name
1. Set the URL to `http://localhost:8000/leads/resumes/{resume_filename}`, replacing {resume_filename} with the actual filename of a resume you want to retrieve. Make sure that the file name exists in `resumes` directory.
2. Select the "Authorization" tab and choose "Bearer Token" from the dropdown menu.
3. Paste the JWT token in the "Token" field.
4. Send the **GET** request and verify that you now receive a 200 OK response along with the resume file.
5. P.S. To avoid duplicating resume file names, I added UUID prefix for each file uploaded.

## Email Notification
The application is currently configured to use Twilio's SendGrid for email sending activity. The email delivery will take some time as SendGrid process the request.
As I tested so far, I'm able to see all the email related activities from SendGrid's dashboard. 