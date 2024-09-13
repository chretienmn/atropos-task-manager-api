# Atropos Task Manager API

This API manages long-running tasks using AWS Glue, built using the Falcon framework. It provides REST endpoints for task management, including starting tasks, checking task status, and retrieving task results. It also features OpenAPI documentation with `spectree` and utilizes `moto` to mock AWS services for local testing.

## Features

- **Create Tasks**: Start an AWS Glue job using a task ID.
- **Check Task Status**: Get real-time task status.
- **Retrieve Task Results**: Fetch task results from S3.
- **OpenAPI Documentation**: Automatically generated OpenAPI documentation using `spectree`.
- **Mocked AWS Services**: Uses `moto` for mocking AWS Glue and S3, allowing local testing without AWS account access.

## Getting Started

### Prerequisites

- Python 3.9+
- `virtualenv` for creating isolated Python environments
- Docker (optional, for containerized deployment)

### Running Locally

#### 1. Clone the Repository

```bash
git clone https://github.com/chretienmn/atropos-task-manager-api.git
cd atropos-task-manager-api
```

#### 2. Set Up Virtual Environment

It’s recommended to use virtualenv to create an isolated Python environment for the project:
```bash
# Install virtualenv if not installed
pip install virtualenv

# Create a virtual environment
virtualenv .venv

# Activate the virtual environment
# On Debian/Ubuntu:
. .venv/bin/activate
# On macOS/Linux:
source .venv/bin/activate
```

#### 3. Install Dependencies

Once the virtual environment is activated, install the required dependencies:
```bash
pip install -r requirements.txt
```
#### 4 Set Environment Variables

Add AWS mock credentials:
```bash
ENV AWS_ACCESS_KEY_ID=testing
ENV AWS_SECRET_ACCESS_KEY=testing
ENV AWS_DEFAULT_REGION=us-east-1
```

#### 5. Run the Application

Now that the environment is set up and dependencies are installed, you can run the app:
```bash
gunicorn app:api --reload
```
This will start the Falcon API server, accessible at `http://localhost:8000`.

#### 6. Access the OpenAPI Documentation

You can view the OpenAPI documentation in the `openapi.json` file.

### Running Tests

Unit tests are written using `unittest` and `falcon.testing`

To run the tests:
```bash
python -m unittest discover
```
This will automatically discover and run all tests in the project.


### Running with Docker

To run the service inside a Docker container, follow the steps below:

#### First option: Build the Docker Image

Build the Docker image using the provided Dockerfile and run it, exposing the app on port 8000:

```bash
docker build -t task-manager-api .
docker run -d -p 8000:8000 task-manager-api
```

#### Second option: Pull from Docker Hub

Once logged in, pull the Docker container from Docker hub and run it, exposing the app on port 8000:

```bash
docker pull chretienmn/atropos-task-manager-api:latest
docker run -d -p 8000:8000 chretienmn/atropos-task-manager-api
```

Now the API will be available at `http://localhost:8000` in your browser.


## License

This project is licensed under the MIT License.
