# Leads Management Application - Design Document

## System Architecture
The application simulates the backend behaviours of leads management system. Users can interact with the backend server through HTTP requests and receives responses in JSON format. The server is built using the FastAPI framework, which is speed-oriented and has a good performance.

## Database Design
The application uses SQLite as the database backend. SQLite is simple and easy to set up. It's good for demo purpose applications. The main database table is `leads`, which stores information about each lead, including their first name, last name, email, resume file path, state, and creation timestamp. 
And the resume files are stored separately in a directory called `resumes` which simulates the file storage system. 

There are some benefits of storing leads metadata and file objects separately:
1. Separation makes it easier to manage and scale metadata database and file storage system independently
2. Storing files in file system can provide better performance than storing metadata and file object together in one database
3. Based on requirements and data volume, this separation allows flexibility to choose different file storage systems like AWS S3, Google Cloud Storage etc.
4. Data backup and recovery can be more efficient


The `Lead` model is defined using SQLAlchemy which is an Object-Relational Mapping (ORM) library that allows for easy interaction with the database using Python objects. The model includes constraints such as non-nullable fields and a unique constraint on the email field to ensure data integrity.
Furthermore, when storing files to the file system, to avoid duplicate file names, I leveraged UUID to address this issue by adding a UUID prefix to every file uploaded.


As the data volume grows in the future, the data layer should be moved to other RDBMS like MySQL or PostgreSQL.

## API Design
The API endpoints are designed to follow REST principles and to fulfill all the requirements. The main endpoints are introduced in README.

These APIs use appropriate HTTP methods (POST, GET, PATCH) to achieve the desired actions and follows standard HTTP status codes to indicate the success or failure of requests.

## Authentication and Authorization
The application implements authentication and authorization using JSON Web Tokens (JWT). When a user sends valid credentials (username and password) to the `/leads/login` endpoint, the server generates a JWT token that includes the user's email as the subject claim. The token is signed using a secret key and a specified algorithm (HS256). HS256 is more efficient. However, RS256 is also highly viable.

For protected endpoints (`/leads`, `/leads/{lead_id}`), the user must include the JWT token in the `Authorization` header of the request. The server verifies the token's signature and extracts the user's email from the token's payload. If the token is valid and the user is authorized, the request is allowed to proceed.

## Email Notification
The application support the functionality of sending email notifications when a new lead is created. The `send_email` function in the `email.py` file is responsible for sending emails.

I chose Twilio's SendGrid service to achieve this requirement as it's one of the most reputable and stable third party email services available on markets.

## Error Handling
The application includes error handling mechanisms to provide feedback to users when errors occur. The application is able to handle errors such as validation errors and database integrity errors.

For example, when a user tries to create a lead with an email that already exists in the database, the application raises an `HTTPException` with a status code of 400 (Bad Request) and an appropriate error message. Or when a user fails to log in, an `HTTPException` with 401 status code will be raised. This helps users understand the reason for the failure and take appropriate action.

## Conclusion
This application is simple and lightweight. Due to time constraint, some of the features like sign in and sign up are hard coded.

The application can be further enhanced by adding more features, such as pagination for lead retrieval, filtering and sorting options, and migration to MySQL or PostgreSQL. However, the current design meets the basic requirements and can be easily extended and adapted to fulfill advanced features.