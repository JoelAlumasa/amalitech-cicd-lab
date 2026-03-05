# Project 6: Full Observability & Security Solution
## Implementation Report

**Author:** Joel Alumasa  
**Date:** March 5, 2026  
**Instance:** AWS EC2 t3.small (eu-north-1)

---

## Executive Summary

Successfully implemented a complete observability and security monitoring stack extending the existing CI/CD Flask application. The solution provides real-time metrics collection, visualization, log aggregation, and security monitoring using industry-standard tools.

---

## Architecture Overview

### Components Deployed
1. **Application Layer**: Flask REST API with Prometheus metrics endpoint
2. **Metrics Collection**: Prometheus server scraping application and system metrics
3. **Visualization**: Grafana dashboards for monitoring
4. **System Monitoring**: Node Exporter for OS-level metrics
5. **AWS Integration**: CloudWatch Logs, CloudTrail, GuardDuty

### Network Architecture
- **Flask App**: Port 80 (HTTP)
- **Prometheus**: Port 9090 (metrics collection)
- **Grafana**: Port 3000 (dashboards)
- **Node Exporter**: Port 9100 (system metrics)

All services running on single EC2 instance with Docker containers.

---

## Implementation Details

### 1. Application Instrumentation

Added Prometheus metrics to Flask app using `prometheus-flask-exporter`:
- HTTP request counters
- Request duration histograms
- Error rate tracking
- Custom application metrics

**Key Metrics Exposed:**
- `flask_http_request_total`: Total requests by method/status
- `flask_http_request_duration_seconds`: Request latency
- `python_gc_*`: Garbage collection stats
- `process_*`: Process-level metrics (CPU, memory)

### 2. Prometheus Configuration

Configured 3 scrape targets:
- **flask-app** (172.17.0.5:5000): Application metrics
- **node-exporter** (172.17.0.4:9100): System metrics  
- **prometheus** (localhost:9090): Self-monitoring

Scrape interval: 15 seconds  
All targets verified as UP and collecting data.

### 3. Grafana Dashboards

Created custom dashboard "Flask App Monitoring" with panels:
- **HTTP Requests Per Second**: Shows traffic patterns over time
- **System CPU Usage**: Node Exporter CPU metrics
- **Available Memory**: System memory monitoring

Dashboard provides real-time visibility into application performance and system health.

### 4. AWS CloudWatch Logs

Configured Docker awslogs driver to stream container logs to CloudWatch:
- Log Group: `/aws/ecs/flask-app`
- Region: eu-north-1
- IAM Role: EC2-CloudWatch-Role (CloudWatchLogsFullAccess)

Successfully streaming Flask application logs for centralized log management and analysis.

### 5. AWS CloudTrail

Enabled CloudTrail for account activity monitoring:
- Trail Name: monitoring-trail
- S3 Storage: Encrypted bucket with lifecycle policies
- Captures API calls and resource changes

Provides audit trail for security and compliance.

### 6. AWS GuardDuty

Enabled GuardDuty for threat detection:
- Continuously monitors for malicious activity
- Analyzes CloudTrail, VPC Flow Logs, DNS logs
- Provides automated security findings

---

## Key Insights & Learnings

### Technical Challenges Resolved
1. **Docker Networking**: Initially used container names for Prometheus targets, but required container IP addresses (172.17.0.x) for proper connectivity
2. **IAM Permissions**: EC2 instance required IAM role with CloudWatch permissions for log streaming
3. **Resource Constraints**: Upgraded from t3.micro (1GB RAM) to t3.small (2GB RAM) to accommodate monitoring stack alongside Jenkins

### Performance Observations
- Prometheus scraping adds minimal overhead (<1% CPU)
- Grafana uses ~150MB RAM at baseline
- CloudWatch log streaming has negligible performance impact
- All services running stably for 24+ hours

### Security Insights
- GuardDuty provides proactive threat detection without configuration
- CloudTrail captures all AWS API activity for audit purposes
- Container logs in CloudWatch enable security incident investigation
- Metrics exposed on `/metrics` endpoint should be restricted in production

---

## Monitoring Capabilities Achieved

### Real-Time Visibility
- Request rate and latency tracking
- Error rate monitoring (500 status codes)
- System resource utilization (CPU, memory, disk)
- Container health status

### Alerting Foundation
- Prometheus configured for alert rule evaluation
- Alert conditions defined (attempted: error rate >5%)
- Integration points established for notification channels

### Log Aggregation
- Centralized logging via CloudWatch
- Searchable logs with timestamps
- Retention policies configurable
- Integration with AWS security services

### Security Monitoring
- GuardDuty threat intelligence
- CloudTrail audit logging
- IAM activity tracking
- Network traffic analysis

---

## Production Recommendations

1. **High Availability**: Deploy Prometheus and Grafana with persistent storage and backup
2. **Authentication**: Enable OAuth for Grafana, restrict Prometheus access
3. **Alerting**: Configure AlertManager for PagerDuty/Slack notifications
4. **Scaling**: Consider Thanos or Cortex for long-term metrics storage
5. **Security**: Implement network segmentation, enable GuardDuty findings automation
6. **Cost Optimization**: Configure CloudWatch log retention, use S3 lifecycle policies

---

## Conclusion

Successfully implemented enterprise-grade observability covering metrics, logs, and security monitoring. The solution provides comprehensive visibility into application and infrastructure health while integrating AWS-native security services. All components verified operational and collecting data.

**Repository:** https://github.com/JoelAlumasa/amalitech-cicd-lab/tree/project6-observability

---

## Appendix: Access Information

- **Prometheus**: http://13.61.2.79:9090
- **Grafana**: http://13.61.2.79:3000 (admin/admin)
- **Flask App**: http://13.61.2.79
- **Metrics Endpoint**: http://13.61.2.79/metrics
- **CloudWatch Logs**: /aws/ecs/flask-app

