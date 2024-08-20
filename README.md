# Flask Microservices with MongoDB

This project is a microservices-based architecture using Flask, Docker, and MongoDB. It includes three main services: `user_service`, `patient_service`, and `appointment_service`. Each service is containerized using Docker and connected to a shared MongoDB instance.

## Services Overview

### 1. **User Service (`user_service`)**
   - Handles user authentication and management.
   - Provides endpoints for user registration, login, and profile management.

### 2. **Patient Service (`patient_service`)**
   - Manages patient data and operations.
   - Provides CRUD operations for patient records.

### 3. **Appointment Service (`appointment_service`)**
   - Manages appointments between users and patients.
   - Provides endpoints for creating, retrieving, updating, and deleting appointments.

*** Make sure you have the docker environment variable set up by setting up the bin folder in the path variable***

## Architecture

- Each service runs in its own Docker container.
- MongoDB is used as the database for all services and is also containerized.
- Services communicate with the MongoDB instance via the network defined in the Docker Compose file.

## Prerequisites

- [Docker](https://www.docker.com/) installed on your machine.
- [Docker Compose](https://docs.docker.com/compose/) for orchestrating the services.

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/blitzster/Hospital-Management-Flask-Microservice.git
cd Hospital-Management-Flask-Microservice


### Build and Run the Services

1. **Build the Docker images:**

   ```bash
   docker-compose build

2. **Start the compose**
   docker-compose up
This command will start all the services (user_service, patient_service, appointment_service) along with the MongoDB container.

3. Access the services:

- User Service: http://localhost:5001
- Patient Service: http://localhost:5002
- Appointment Service: http://localhost:5003
