Social Media API
Project Overview
This project is a Social Media API built using Django and Django REST Framework (DRF). The API allows users to create, update, delete posts, follow other users, and view a feed of posts from the users they follow. The application is designed to simulate a real-world social media environment with user relationships, CRUD operations, and API design, providing a full-stack backend experience.
Features
   Post Management (CRUD)
Users can create, read, update, and delete posts.
Each post includes:
Content (Text)
User (Author)
Timestamp (When the post was created)
Optional Media (Image URLs)
Users can only update or delete their own posts.
User Management (CRUD)
Users can create, read, update, and delete their profiles.
User profiles include:
Username
Email
Password
Bio (Optional)
Profile Picture (Optional)
Follow System
Users can follow and unfollow other users.
Follower and following relationships are stored and managed in the database.
Users cannot follow themselves.
Feed of Posts
Users can view a feed of posts from the users they follow.
The feed displays posts in reverse chronological order.
Optionally, users can filter the feed by date or search for posts by keyword.
Technical Requirements
Database
The application uses Django’s built-in ORM to manage the database.
Models for Users, Posts, and Followers are defined and handled via Django’s ORM.
Authentication
User authentication is handled using Django's built-in authentication system.
JWT token-based authentication is implemented for secure API access.
Only authenticated users can create, update, or delete posts, follow other users, or view their feed.
API Design
The API is designed following RESTful principles.
GET: Retrieve data (e.g., user feed, individual posts).
POST: Create new data (e.g., create a post, follow a user).
PUT/PATCH: Update existing data (e.g., edit a post).
DELETE: Remove data (e.g., delete a post, unfollow a user).
API endpoints include:
User Management: Register, login, update, delete.
Post Management: Create, read, update, delete posts.
Follow Management: Follow/unfollow users.
Feed: View posts from followed users.
Pagination and Sorting
The feed includes pagination to handle large datasets effectively.
Posts can be sorted by date or popularity (e.g., likes, comments).
Deployment
The application is deployed on Heroku (or PythonAnywhere) for easy access and testing.
The API is secured with HTTPS for secure communication between the server and clients.
Installation
1. Clone the Repository
bash
Copy code
git clone https://github.com/jihanmout7 /social-media-api.git
cd social-media-api

2. Install Dependencies
Create a virtual environment and install the required dependencies.
bash
Copy code
python -m venv venv
source venv/bin/activate  # For Linux/MacOS
venv\Scripts\activate     # For Windows
pip install -r requirements.txt

3. Apply Migrations
bash
Copy code
python manage.py migrate

4. Create a Superuser (For Admin Panel)
bash
Copy code
python manage.py createsuperuser

5. Run the Development Server
bash
Copy code
python manage.py runserver

Visit http://127.0.0.1:8000 to start interacting with the API.
Usage
Authentication
You can register a new user via the /register/ endpoint.
Login with /login/ to get a JWT token for authentication.
Use the token in the Authorization header to access protected endpoints.
API Endpoints
User Endpoints
POST /users/register/ - Register a new user.
POST /users/login/ - Login and get a JWT token.
GET /users/me/ - Retrieve the current authenticated user's profile.
PUT /users/me/ - Update the current user's profile.
Post Endpoints
POST /posts/ - Create a new post.
GET /posts/ - Retrieve a list of posts (with optional filters for feed).
GET /posts/{id}/ - Retrieve a specific post.
PUT /posts/{id}/ - Update a post (only if you are the author).
DELETE /posts/{id}/ - Delete a post (only if you are the author).
Follow Endpoints
POST /follow/{user_id}/ - Follow a user.
DELETE /follow/{user_id}/ - Unfollow a user.
Feed Endpoints
GET /feed/ - Retrieve the posts from users the authenticated user follows (with pagination and sorting options).
Technologies Used
Django - Backend framework.
Django REST Framework - API design and implementation.
JWT - Token-based authentication.
MySQL - Database (or any relational database supported by Django).
Heroku/PythonAnywhere - Deployment.


