# Django Project with Docker Compose

This is a Django project setup with Docker Compose for easy development and deployment.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Allexik/starnavi_test.git
    cd starnavi_test
    ```

   2. **Create a `.env` file for environment variables:**

       ```bash
       touch .env
       ```

       Add the following content to `.env` file:

       ```env
       GCP_PROJECT_ID=your-gcp-project-id
       GCP_MODELS_LOCATION=your-gcp-models-location
       GOOGLE_APPLICATION_CREDENTIALS_JSON=your-gcp-credentials-json
       ```

3. **Build and run the containers:**

    ```bash
    docker-compose up --build
    ```

4. **Apply migrations and create a superuser:**

    ```bash
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser
    ```

5. **Access the application:**

    Open your browser and go to `http://localhost:8000`.
