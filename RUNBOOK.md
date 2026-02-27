# Jenkins CI/CD Pipeline - Runbook

## Project Overview
Complete end-to-end CI/CD pipeline that automatically builds, tests, containerizes, and deploys a Flask web application to AWS EC2 using Jenkins.

**Author:** Joel Alumasa  
**Date:** February 27, 2026  
**GitHub:** https://github.com/JoelAlumasa/amalitech-cicd-lab

---

## Architecture
```
Developer → GitHub → Jenkins → Docker Hub → AWS EC2 → Live Application
```

**Components:**
- **Application:** Python Flask REST API
- **Testing:** pytest unit tests  
- **CI/CD Engine:** Jenkins (WSL)
- **Containerization:** Docker
- **Registry:** Docker Hub
- **Deployment Target:** AWS EC2 (Amazon Linux 2023)

---

## Prerequisites

### Required Accounts
- [x] GitHub account
- [x] Docker Hub account (https://hub.docker.com)
- [x] AWS account with EC2 access

### Required Tools
- [x] WSL2 (Ubuntu) or Linux environment
- [x] Docker Desktop (with WSL integration)
- [x] Git
- [x] SSH client

---

## Setup Instructions

### Phase 1: Application Setup (10 minutes)

#### 1.1 Clone the Repository
```bash
git clone https://github.com/JoelAlumasa/amalitech-cicd-lab.git
cd amalitech-cicd-lab
```

#### 1.2 Verify Application Files
```bash
tree
# Should show:
# ├── app/
# │   └── app.py
# ├── tests/
# │   └── test_app.py
# ├── Dockerfile
# ├── Jenkinsfile
# ├── requirements.txt
# └── README.md
```

#### 1.3 Test Locally (Optional)
```bash
pip3 install -r requirements.txt
python3 -m pytest tests/ -v
# All tests should PASS
```

---

### Phase 2: AWS EC2 Setup (15 minutes)

#### 2.1 Launch EC2 Instance
1. Go to AWS Console → EC2 → Launch Instance
2. Configure:
   - **Name:** jenkins-cicd-demo
   - **AMI:** Amazon Linux 2023
   - **Instance Type:** t3.micro (free tier)
   - **Key Pair:** Create new (download .pem file)
   - **Security Group:**
     - SSH (22) - My IP
     - HTTP (80) - Anywhere (0.0.0.0/0)
     - Custom TCP (8080) - My IP (for Jenkins)

3. Launch and note the **Public IPv4 address**

#### 2.2 Install Docker on EC2
```bash
# SSH to EC2
chmod 400 your-keypair.pem
ssh -i your-keypair.pem ec2-user@<EC2_PUBLIC_IP>

# Install Docker
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -aG docker ec2-user
sudo systemctl enable docker

# Exit and reconnect for group changes
exit
ssh -i your-keypair.pem ec2-user@<EC2_PUBLIC_IP>

# Verify Docker works
docker ps
# Should show empty list (no containers yet)
```

---

### Phase 3: Jenkins Setup (20 minutes)

#### 3.1 Install Jenkins (on WSL/Linux)
```bash
# Install Java
sudo apt update
sudo apt install -y openjdk-17-jdk

# Add Jenkins repository
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | \
  sudo gpg --dearmor -o /usr/share/keyrings/jenkins-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.gpg] \
  https://pkg.jenkins.io/debian-stable binary/" | \
  sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

# Install Jenkins
sudo apt update
sudo apt install -y jenkins

# Start Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins

# Get initial admin password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

#### 3.2 Initial Jenkins Configuration
1. Open browser: `http://localhost:8080`
2. Paste initial admin password
3. Choose **"Install suggested plugins"**
4. Create admin user (save credentials!)
5. Keep default URL: `http://localhost:8080/`

#### 3.3 Install Required Plugins
1. Go to: **Manage Jenkins → Plugins → Available plugins**
2. Search and install:
   - Docker Pipeline
   - SSH Agent
   - Credentials Binding (should already be installed)
3. Check **"Restart Jenkins when installation is complete"**
4. Wait for restart (~30 seconds)

#### 3.4 Add Jenkins to Docker Group
```bash
# Allow Jenkins to run Docker commands
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins

# Wait 20 seconds for restart
sleep 20
```

---

### Phase 4: Credentials Configuration (10 minutes)

#### 4.1 Add Docker Hub Credentials
1. Go to: **Dashboard → Manage Jenkins → Credentials**
2. Click: **System → Global credentials (unrestricted)**
3. Click: **+ Add Credentials**
4. Configure:
   - **Kind:** Username with password
   - **Username:** [your Docker Hub username]
   - **Password:** [your Docker Hub password]
   - **ID:** `dockerhub_credentials`
   - **Description:** Docker Hub Login
5. Click **"Create"**

#### 4.2 Add EC2 SSH Key
1. Click: **+ Add Credentials** again
2. Configure:
   - **Kind:** SSH Username with private key
   - **ID:** `ec2_ssh_key`
   - **Description:** EC2 SSH Key
   - **Username:** `ec2-user`
   - **Private Key:** Click "Enter directly"
3. Copy your .pem file contents:
```bash
   cat your-keypair.pem
```
4. Paste entire key (including BEGIN/END lines)
5. Click **"Create"**

---

### Phase 5: Pipeline Creation (5 minutes)

#### 5.1 Create Pipeline Job
1. Dashboard → **New Item**
2. Name: `jenkins-cicd-demo`
3. Type: **Pipeline**
4. Click **"OK"**

#### 5.2 Configure Pipeline
**General Section:**
- Check **"This project is parameterized"**
- Add Parameter: **String Parameter**
  - Name: `EC2_HOST`
  - Default Value: `<your EC2 public IP>`
  - Description: EC2 instance public IP address

**Pipeline Section:**
- Definition: **Pipeline script from SCM**
- SCM: **Git**
- Repository URL: `https://github.com/JoelAlumasa/amalitech-cicd-lab.git`
- Credentials: **- none -** (public repo)
- Branch: `*/main`
- Script Path: `Jenkinsfile`

Click **"Save"**

---

## Running the Pipeline

### First Build
1. Go to pipeline: **jenkins-cicd-demo**
2. Click: **Build with Parameters**
3. Verify `EC2_HOST` is correct
4. Click: **Build**

### Monitor Progress
1. Click on build number (e.g., **#1**)
2. Click: **Console Output**
3. Watch each stage execute:
   - ✅ Checkout
   - ✅ Install Dependencies
   - ✅ Run Tests
   - ✅ Build Docker Image
   - ✅ Push to Registry
   - ✅ Deploy to EC2

**Expected Duration:** 2-4 minutes (first build may take longer)

---

## Verification

### 1. Check Jenkins Build Status
- Build should show **green checkmark** ✅
- Console output should end with: `Finished: SUCCESS`

### 2. Verify Application is Live
Open browser and test endpoints:
```bash
# Main endpoint
curl http://<EC2_PUBLIC_IP>/
# Expected: {"message":"Hello from CI/CD Pipeline!","status":"success","version":"1.0"}

# Health check
curl http://<EC2_PUBLIC_IP>/health
# Expected: {"status":"healthy"}

# Info endpoint
curl http://<EC2_PUBLIC_IP>/info
# Expected: {"app":"Jenkins CI/CD Demo","environment":"development"}
```

### 3. Check Docker Hub
Visit: `https://hub.docker.com/r/<your-username>/jenkins-cicd-demo`
- Should see pushed image with tags: `latest` and `1` (or current build number)

### 4. Check EC2 Container
```bash
ssh -i your-keypair.pem ec2-user@<EC2_PUBLIC_IP>
docker ps
# Should show jenkins-app container running on port 80
```

---

## Making Changes (Testing CI/CD Automation)

### Update Application Code
```bash
# Edit app/app.py
nano app/app.py

# Commit and push
git add app/app.py
git commit -m "Update application message"
git push origin main
```

### Trigger New Build
1. In Jenkins, click **Build with Parameters**
2. Click **Build**
3. Watch automated deployment
4. Refresh browser - see updated app!

---

## Troubleshooting

### Issue: Jenkins can't access Docker
**Symptom:** `docker: command not found` in console output

**Fix:**
```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### Issue: Can't SSH to EC2
**Symptom:** `Connection refused` or `Permission denied`

**Fixes:**
1. Check security group allows SSH from your IP
2. Verify key file permissions: `chmod 400 keypair.pem`
3. Confirm username is `ec2-user` for Amazon Linux 2023
4. Test SSH manually: `ssh -i keypair.pem ec2-user@<IP>`

### Issue: Docker login fails
**Symptom:** `unauthorized: incorrect username or password`

**Fix:**
1. Verify Docker Hub credentials in Jenkins
2. Check credential ID is exactly: `dockerhub_credentials`
3. Ensure Docker Hub password is correct

### Issue: Tests fail
**Symptom:** Build stops at "Run Tests" stage

**Fix:**
1. Run tests locally: `pytest tests/ -v`
2. Check test output for specific failures
3. Fix code issues before pushing

### Issue: App not accessible on EC2
**Symptom:** Browser can't reach `http://<EC2_IP>`

**Fixes:**
1. Check security group allows HTTP (port 80) from 0.0.0.0/0
2. Verify container is running: `docker ps`
3. Check container logs: `docker logs jenkins-app`
4. Restart container:
```bash
   docker restart jenkins-app
```

### Issue: Port 80 already in use
**Symptom:** `port is already allocated`

**Fix:**
```bash
# Stop old container
docker stop jenkins-app
docker rm jenkins-app

# Pull and run new one
docker pull <your-username>/jenkins-cicd-demo:latest
docker run -d --name jenkins-app -p 80:5000 <your-username>/jenkins-cicd-demo:latest
```

---

## Pipeline Stages Explained

### 1. Checkout
- Clones GitHub repository
- Checks out specified branch (main)
- Sets up workspace

### 2. Install Dependencies
- Runs: `pip install -r requirements.txt`
- Installs Flask, pytest, werkzeug

### 3. Run Tests
- Executes: `pytest tests/ -v`
- Tests must pass or pipeline stops
- Quality gate: prevents bad code from deploying

### 4. Build Docker Image
- Creates container image from Dockerfile
- Tags with build number and 'latest'
- Image size: ~90MB

### 5. Push to Registry
- Authenticates with Docker Hub
- Uploads image to registry
- Makes image available for EC2 to pull

### 6. Deploy to EC2
- SSHs to EC2 instance
- Stops old container
- Pulls latest image
- Starts new container
- Cleans up old images

---

## Maintenance

### Update EC2 IP Address
If EC2 IP changes:
1. Go to pipeline **Configure**
2. Update `EC2_HOST` default value
3. Save

### Rotate Credentials
**Docker Hub:**
1. Update password in Docker Hub
2. Update Jenkins credential: `dockerhub_credentials`

**EC2 SSH Key:**
1. Create new key pair in AWS
2. Update Jenkins credential: `ec2_ssh_key`

### Clean Up Old Docker Images
```bash
# On EC2
ssh -i keypair.pem ec2-user@<EC2_IP>
docker image prune -af
```

---

## Cost Considerations

### AWS EC2
- **t3.micro:** Free tier eligible (750 hours/month)
- After free tier: ~$0.0104/hour (~$7.49/month)
- **Stop instance when not in use** to save costs

### Docker Hub
- Free tier: Unlimited public repos
- Rate limits: 200 pulls/6 hours (usually sufficient)

---

## Security Best Practices

✅ **Implemented:**
- SSH keys (not passwords)
- Credentials stored in Jenkins (encrypted)
- Security groups restrict access
- Dockerfile uses non-root user (could be added)

⚠️ **For Production (not in lab):**
- Use HTTPS (SSL/TLS certificates)
- Enable Jenkins authentication
- Restrict Jenkins to VPN only
- Scan Docker images for vulnerabilities
- Use private Docker registry

---

## Cleanup (When Done)

### Stop Resources
```bash
# Stop Jenkins
sudo systemctl stop jenkins

# Stop EC2 (AWS Console)
# EC2 → Instances → Select instance → Instance state → Stop
```

### Delete Everything
```bash
# Terminate EC2 (AWS Console)
# EC2 → Instances → Select instance → Instance state → Terminate

# Delete Docker Hub repo
# hub.docker.com → Repositories → jenkins-cicd-demo → Settings → Delete

# Uninstall Jenkins (optional)
sudo systemctl stop jenkins
sudo apt remove -y jenkins
sudo rm -rf /var/lib/jenkins
```

---

## Additional Resources

- **Jenkins Documentation:** https://www.jenkins.io/doc/
- **Docker Documentation:** https://docs.docker.com/
- **Flask Documentation:** https://flask.palletsprojects.com/
- **AWS EC2 Guide:** https://docs.aws.amazon.com/ec2/

---

## Success Criteria

Your pipeline is working correctly when:
- ✅ Jenkins build shows green checkmark
- ✅ All 6 stages pass in console output
- ✅ App responds at `http://<EC2_IP>/`
- ✅ Docker Hub shows pushed image
- ✅ EC2 shows running container (`docker ps`)
- ✅ Making code changes triggers automatic redeployment

---

**Congratulations! You've built a production-grade CI/CD pipeline!** 🎉
