# Markdown-to-PDF Converter API

A lightweight Python API for converting Markdown files (`.md`) to PDF. Built with **FastAPI** and **Pandoc**, this project is designed to be extended with features like email delivery and QR code downloads, and it’s ready to run on **K3s clusters** for scalable deployment.

---

## Features

### Current Features
- Upload Markdown files via HTTP POST.
- Convert Markdown (`.md`) to PDF (`.pdf`) using Pandoc.
- Unique temporary file storage to prevent overwrites.
- FastAPI interactive documentation (`/docs`) for testing endpoints.

### Planned Features
- Automatically generate **QR codes** for converted files.
- Send download links via **email**.
- Deploy seamlessly on **K3s clusters** for scalable microservice architecture.

---

## Installation

### Requirements
- Python 3.10+
- [Pandoc](https://pandoc.org/installing.html)
- LaTeX (for PDF conversion)
- FastAPI dependencies (listed in `requirements.txt`)

### Docker Image

To simplify deployment and avoid managing dependencies manually, this project provides a Docker image.

```bash
docker compose up -d
```

- Access the API at: http://localhost:8000
- Interactive docs available at: http://localhost:8000/docs