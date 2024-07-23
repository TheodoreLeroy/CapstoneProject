# System Architecture

## Overview
The face recognition attendance system consists of two main components: the backend and the frontend. The backend is responsible for handling the image processing, face recognition, and database interactions. The frontend provides a user interface for uploading images and viewing attendance data.

## Backend
The backend is built using Flask, a lightweight WSGI web application framework. It includes endpoints for image upload and face recognition processing.

## Frontend
The frontend is built using React, a JavaScript library for building user interfaces. It includes components for uploading images and displaying results.

## Database
The system uses SQLite as the database to store student information and embeddings.
Here's a detailed structure of a production-ready face recognition attendance system project, with an endpoint to receive images from a backend server every 5 minutes. The project is structured for maintainability, scalability, and clarity.

### Project Structure

