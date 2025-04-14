[![Docker Image CI](https://github.com/thanhtrungnguyen/mlops-project-webapp/actions/workflows/docker-image.yml/badge.svg)](https://github.com/thanhtrungnguyen/mlops-project-webapp/actions/workflows/docker-image.yml)

# MLOps Project WebApp

This repository contains a Flask web application that downloads a model from the Hugging Face Hub and serves predictions through a simple user interface.

## Project Structure

- `app/`: Contains the Flask application code, including:
    - `app.py`: The main Flask entry point.
    - `templates/`: Directory for HTML templates.
    - `static/`: Directory for CSS, JS, and other static files.
- `.github/workflows/`: Contains GitHub Actions workflow for CI/CD (`main.yml`).
- `Dockerfile`: Used to build the Docker image.

## Getting Started

1. **Install Dependencies** (Locally):
   ```bash
   pip install -r requirements.txt
