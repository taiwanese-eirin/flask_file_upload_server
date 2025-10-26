# Flask File Upload Server

This is a simple Flask file upload server, containerized with Docker for easy development and deployment.

## Getting started

Ensure you have Docker and Docker Compose installed on your system.

1.  **Set Up Environment Variables**

    Copy the example environment file and edit it as needed.
    ```bash
    cp .env.example .env
    ```

2.  **Changing the Docker Port**

    The application runs internally on port `8000` within the container. If you need to change the port accessible on your host machine (e.g., to run on port `8080` instead of `8000`), edit the ports section in `docker-compose.yml`:
    ```yaml
    ports:
      - "HOST_PORT:8000"
    ```

2.  **Build and Run the Service**

    Use `docker compose` to build the image and start the container in the background.
    ```bash
    docker compose up --build -d
    ```

3.  **Check the Service Status**

    You can view the service logs with the following command.
    ```bash
    docker compose logs -f web
    ```

4.  **Stop the Service**

    To gracefully stop and remove the containers and network defined in `docker-compose.yml`, run:
    ```bash
    docker compose down
    ```

5.  **Delete Uploded Files**

    To stop the service and permanently remove the Docker volumes (including the uploaded files), run:
    ```bash
    docker compose down -v
    ```

## Standalone Execution (Without Docker Compose)

You can also run this project without Docker Compose, either directly on your local machine for development or using a `docker run` command.

### 1. Local Development (Without Docker)

This method is suitable for quick testing and development directly on your machine.

1.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Changing the default port:**

    The default port for the application is `8000`. To change this, modify the following line in `app.py`:
    ```python
    app.run(host='0.0.0.0', port=XXXX)
    ```

4.  **Run the application:**
    The application will create an `uploads` directory in your project folder.
    ```bash
    python app.py
    ```
    The server will be available at `http://localhost:XXXX`.

### 2. Using `docker run`

This method is suitable for production-like environments where you want to run the application as a standalone container.

1.  **Build the Docker image:**
    ```bash
    docker build -t flask_file_upload_server:latest .
    ```

2.  **Run the container:**
    This command starts the container, maps port 8000, and creates a named volume `my_uploads` to persist uploaded files.
    ```bash
    docker run -d --name my-flask-app -p 8000:8000 -v my_uploads:/data/uploads --restart unless-stopped flask_file_upload_server:latest
    ```

### Deploying with Systemd

You can use the templates in the `deploy/systemd/` directory to run the application as a systemd service for automatic startup and process management.

**Example: Using the `docker-compose` based systemd service**

1.  **Copy the Service File**
    ```bash
    sudo cp deploy/systemd/flask_upload_compose.service /etc/systemd/system/
    ```

2.  **Modify the Service Configuration**
    Edit `/etc/systemd/system/flask_upload_compose.service` and set `WorkingDirectory` to the absolute path of your deployed project. (Default: `/srv/uploads`)

3.  **Set Up Environment Variables**

    In `WorkingDirectory`, prepare the `docker compose` environments:

    - Copy the example environment:
    ```bash
    cp .env.example .env
    ```

    - Edit `docker-compose.yml` port:
    ```yaml
    ports:
      - "HOST_PORT:8000"
    ```
    
4.  **Enable and Start the Service**
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable --now flask_upload_compose.service
    ```

4.  **View Service Logs**
    ```bash
    journalctl -u flask_upload_compose.service -f
    ```

#### **Note:** It is recommended to use a reverse proxy (such as *Nginx*) in front of the application container to handle SSL/TLS termination and serve static files.
