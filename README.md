# Jenkins CI/CD Pipeline Demo

## Overview
Production-grade CI/CD pipeline using Jenkins that builds, tests, containerizes, and deploys a Flask web application to AWS EC2 with automatic webhook triggering.

## Architecture
- **Application**: Python Flask REST API
- **Testing**: pytest unit tests  
- **Containerization**: Docker
- **CI/CD**: Jenkins Pipeline (running on EC2)
- **Deployment**: AWS EC2 (Amazon Linux 2023)
- **Automation**: GitHub webhooks for instant build triggering

## Infrastructure Setup
- **Jenkins Location**: EC2 Instance (13.53.129.72:8080)
- **Application Deployment**: Same EC2 instance (port 80)
- **Docker Registry**: Docker Hub (jaluebo/jenkins-cicd-demo)

## Pipeline Stages
1. **Checkout**: Clone repository from GitHub
2. **Install**: Install Python dependencies
3. **Test**: Run pytest unit tests (quality gate)
4. **Build**: Create Docker image with build number tagging
5. **Push**: Push to Docker Hub registry
6. **Deploy**: SSH to EC2, pull image, deploy container

## Automated Deployment Flow
```
Developer pushes code → GitHub webhook → Jenkins (EC2) → Auto-build → Deploy
```
**Trigger time**: 3-5 seconds from push to build start  
**Total pipeline**: ~2-4 minutes from code push to live deployment

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
curl http://localhost:5000/info
```

## Jenkins Setup Requirements

### Plugins Installed
- Pipeline
- Git
- Docker Pipeline
- SSH Agent
- Credentials Binding
- GitHub Plugin

### Credentials Configured
- `dockerhub_credentials`: Docker Hub username/password
- `ec2_ssh_key`: EC2 SSH private key for deployment

### Pipeline Configuration
- **Build Triggers**: GitHub hook trigger for GITScm polling
- **Parameters**: `EC2_HOST` (13.53.129.72)
- **SCM**: Git (https://github.com/JoelAlumasa/amalitech-cicd-lab.git)

### GitHub Webhook
- **Payload URL**: `http://13.53.129.72:8080/github-webhook/`
- **Content type**: application/json
- **Events**: Push events
- **Active**: Yes

## Deployment Verification

**Application URL**: `http://13.53.129.72/`

**Expected Response**:
```json
{
  "message": "🎉 EC2 Jenkins + Webhook = PRODUCTION READY!",
  "status": "success",
  "version": "6.0",
  "author": "Joel Alumasa",
  "jenkins_location": "EC2 Instance"
}
```

## Production Architecture Highlights

### Why Jenkins on EC2?
- **Public IP**: GitHub can reach webhook endpoint directly
- **No tunneling needed**: Unlike localhost setup, no ngrok required
- **Production-ready**: Same architecture used by real companies
- **Cost-effective**: Single EC2 instance handles both Jenkins and app

### Security Considerations
- EC2 Security Group allows ports: 22 (SSH), 80 (HTTP), 8080 (Jenkins)
- SSH keys used for authentication (no passwords)
- Docker Hub credentials encrypted in Jenkins
- Jenkins access should be restricted to VPN in production

## Key Learning Outcomes
✅ End-to-end CI/CD pipeline implementation  
✅ Automated testing as quality gates  
✅ Docker containerization and registry management  
✅ GitHub webhook integration for instant deployment  
✅ Production-ready architecture on AWS  
✅ Infrastructure as Code (Jenkinsfile)

## Project Timeline
- Initial Setup: ~2 hours
- Jenkins Migration to EC2: ~30 minutes  
- Webhook Configuration: ~15 minutes
- Total: Production-ready CI/CD in ~3 hours

## Author
**Joel Alumasa**  
AmaliTech DevOps Apprenticeship  
Carnegie Mellon University Africa - MS in Information Technology

## Repository
https://github.com/JoelAlumasa/amalitech-cicd-lab
