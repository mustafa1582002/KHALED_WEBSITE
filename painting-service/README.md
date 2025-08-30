# Painting Service Project

This project is a web application for a painting and decoration service. It allows users to view various painting projects and provides an admin panel for managing these projects.

## Project Structure

```
painting-service
├── app
│   ├── __init__.py
│   ├── models
│   │   ├── __init__.py
│   │   └── project.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   └── main.py
│   ├── static
│   │   ├── css
│   │   │   └── style.css
│   │   └── js
│   │       └── main.js
│   └── templates
│       ├── admin
│       │   ├── dashboard.html
│       │   ├── login.html
│       │   └── project_edit.html
│       ├── base.html
│       ├── home.html
│       └── projects.html
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

## Features

- **User Interface**: A modern and clean design for showcasing painting projects.
- **Admin Panel**: Secure login for administrators to manage projects, including adding, editing, and deleting projects.
- **Database Integration**: Utilizes a database to store project details, ensuring data persistence.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd painting-service
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the Application**:
   Update the `config.py` file with your database connection details.

4. **Run the Application**:
   ```bash
   python run.py
   ```

5. **Access the Application**:
   Open your web browser and navigate to `http://localhost:5000` to view the application.

## Usage

- Users can browse through various painting projects on the home page.
- Admins can log in to manage projects through the admin dashboard.

## License

This project is licensed under the MIT License.