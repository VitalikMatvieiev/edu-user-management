# User Management System

## Overview
This Django-based User Management System is designed to manage user profiles and instructor ratings. It integrates JWT authentication from an external Identity Service, providing a secure and scalable solution for user management.

## Features
- **User Profiles**: Management of user profiles with fields like full name, date of birth, and unique identity ID linked to an external Identity Service.
- **Instructor Ratings**: Allows for the rating of instructors including numeric ratings and textual reviews.
- **JWT Authentication**: Integration with an external Identity Service using JWT tokens for secure authentication.
- **Role-Based Access Control**: Permissions and access control based on user claims included in the JWT token.

## Technologies
- **Backend Framework**: Django
- **Database**: [Add your database, e.g., PostgreSQL, SQLite]
- **Authentication**: JWT (JSON Web Tokens)

## Setup and Installation
1. **Clone the Repository**:  
   `git clone https://github.com/VitalikMatvieiev/edu-user-management.git`

2. **Set Up a Virtual Environment** (Optional but recommended):  
   ```bash
   python -m venv venv
   source venv/bin/activate # Linux/Mac
   venv\Scripts\activate # Windows
3. **Install Dependencies**:
   `pip install -r requirements.txt`
4. **Run the Development Server**:
   `python manage.py runserver`
5. **Access the Application**:
Open your web browser and go to `http://127.0.0.1:8000/`


## API Endpoints

- **User Profiles**: `api/userprofiles/`  
  Supports GET, POST, PUT, DELETE methods for managing user profiles.

- **Instructor Rates**: `api/instructorrates/`  
  Supports GET, POST, PUT, DELETE methods for managing instructor rates.

## Testing

Run unit tests using the following command:  
```bash
python manage.py test
```

## Contributing
   Contributions to this project are welcome. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature.
3. Add your changes and write appropriate tests.
4. Submit a pull request with a detailed description of your changes.