from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "🎉 EC2 Jenkins + Webhook = PRODUCTION READY!",
        "status": "success",
        "version": "6.0",
        "author": "Joel Alumasa",
        "jenkins_location": "EC2 Instance"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/info')
def info():
    return jsonify({
        "app": "Jenkins CI/CD Demo",
        "environment": os.getenv("ENV", "production"),
        "deployed_by": "Jenkins on EC2",
        "auto_triggered": "GitHub Webhook"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
