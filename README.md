# Jenkins CI/CD Pipeline Demo

## Overview
Complete CI/CD pipeline using Jenkins that builds, tests, containerizes, and deploys a Flask web application to EC2.

## Architecture
- **Application**: Python Flask REST API
- **Testing**: pytest unit tests
- **Containerization**: Docker
- **CI/CD**: Jenkins Pipeline
- **Deployment**: AWS EC2 (Amazon Linux 2)

## Pipeline Stages
1. **Checkout**: Clone repository
2. **Install**: Install Python dependencies
3. **Test**: Run pytest unit tests
4. **Build**: Create Docker image
5. **Push**: Push to Docker Hub
6. **Deploy**: SSH to EC2 and run container

## Local Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Build Docker image
docker build -t jenkins-cicd-demo .

# Run locally
docker run -p 5000:5000 jenkins-cicd-demo

# Test endpoints
curl http://localhost:5000/
curl http://localhost:5000/health
```

## Jenkins Setup Requirements
- Jenkins plugins: Pipeline, Git, Docker, SSH Agent, Credentials Binding
- Credentials needed:
  - `dockerhub_credentials`: Docker Hub username/password
  - `ec2_ssh_key`: EC2 SSH private key
- Environment variable: `EC2_HOST` (EC2 public IP/DNS)

## Deployment Verification
After pipeline runs, verify at: `http://<EC2_PUBLIC_IP>/`

## Author
Joel Alumasa - AmaliTech DevOps Apprenticeship
