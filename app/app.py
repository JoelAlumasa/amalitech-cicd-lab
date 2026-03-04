from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import os
import time
import random

app = Flask(__name__)

# Initialize Prometheus metrics
metrics = PrometheusMetrics(app)

# Add custom metrics
metrics.info('app_info', 'Application info', version='8.0')

@app.route('/')
def home():
    # Simulate variable latency
    time.sleep(random.uniform(0.01, 0.1))
    return jsonify({
        "message": "🚀 Full Observability Stack - Prometheus + Grafana Ready!",
        "status": "success",
        "version": "8.0",
        "author": "Joel Alumasa",
        "jenkins_location": "EC2 Instance",
        "monitoring": "enabled"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/info')
def info():
    return jsonify({
        "app": "Jenkins CI/CD + Observability Demo",
        "environment": os.getenv("ENV", "production"),
        "deployed_by": "Jenkins on EC2",
        "auto_triggered": "GitHub Webhook",
        "observability": "Prometheus + Grafana"
    })

@app.route('/error')
def error():
    """Endpoint to test error alerts"""
    return jsonify({"error": "Intentional error for testing alerts"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
