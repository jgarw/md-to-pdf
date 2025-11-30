# Markdown-to-PDF Converter

A web application for converting Markdown files to PDF with email delivery. Built with FastAPI and deployed using Kubernetes.

## Overview

This project converts Markdown files to PDF using Pandoc and LaTeX. It includes a web interface, email delivery with QR codes, and can be deployed locally with Docker or to a Kubernetes cluster.

I built this to learn Kubernetes deployment patterns and container orchestration. The K8s configuration is functional but represents a learning project rather than production expertise.

## Features

- Markdown to PDF conversion via Pandoc
- Web interface for file uploads
- Email delivery with QR code links
- RESTful API with FastAPI
- Docker containerization
- Kubernetes deployment configuration

## Tech Stack

- Python 3.13
- FastAPI
- Pandoc, LaTeX (XeTeX)
- Docker
- Kubernetes (tested with minikube)

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your SMTP settings

# Run
uvicorn src.app:app --reload --port 8080
```

Access at http://localhost:8080

## Docker

```bash
# Build
docker build -t md-to-pdf -f ./docker/dockerfile .

# Run
docker run -p 8080:8080 --env-file .env md-to-pdf
```

Or use the pre-built image:

```bash
docker pull jgarw/md-to-pdf:latest
docker run -p 8080:8080 --env-file .env jgarw/md-to-pdf:latest
```

## Kubernetes Deployment

This is my first Kubernetes deployment. The configuration works but may not follow all best practices.

```bash
# Start minikube
minikube start --driver=qemu

# Create secrets
kubectl create secret generic md-to-pdf-secrets --from-env-file=.env

# Deploy
kubectl apply -f k8s/deployment.yaml

# Check status
kubectl get pods

# Access locally
kubectl port-forward service/md-to-pdf-service 8080:8080
```

## Configuration

Required environment variables in `.env`:

```
SMTP_SERVER=smtp.email.com
SMTP_PORT=###
FROM_ADDRESS=your-actual-email@email.com
SMTP_PASSWORD=your-password-here
```

For Gmail, you need an App Password (requires 2FA enabled).

## API

### POST /convert/
Upload a Markdown file for conversion.

Parameters:
- `file`: Markdown file
- `email` (optional): Send download link to this address

Returns the PDF file.

### GET /download/{file_id}
Download a previously converted PDF by its ID.

### GET /
Web interface for uploads.

Interactive API docs available at `/docs`

## Project Structure

```
md-to-pdf/
├── src/
│   ├── app.py              # Main FastAPI application
│   ├── converter.py        # Markdown to PDF logic
│   ├── qr_generator.py     # QR code generation
│   └── mail.py             # Email delivery
├── static/
│   └── index.html          # Web interface
├── k8s/
│   ├── deployment.yaml     # Kubernetes deployment config
│   ├── secrets.yaml.example
├── docker
│   ├── dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## Notes

- Files are stored temporarily using UUID-based naming
- Uploads and outputs use ephemeral storage in Kubernetes (emptyDir volumes)
- The K8s deployment uses a single replica by default
- Email functionality requires SMTP credentials

## License

MIT