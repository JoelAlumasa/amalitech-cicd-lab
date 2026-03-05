# Project 6: Full Observability & Security Solution

**Extends Project 5 CI/CD** with complete monitoring stack.

## Architecture
- Flask app with `/metrics` endpoint (Prometheus exporter)
- Prometheus scraping Flask + Node Exporter
- Grafana dashboards for visualization
- CloudWatch Logs integration
- CloudTrail for audit logging
- GuardDuty for threat detection

## Monitoring Stack
- **Prometheus**: `http://13.61.2.79:9090`
- **Grafana**: `http://13.61.2.79:3000` (admin/admin)
- **Node Exporter**: System metrics

## AWS Services
- CloudWatch Logs: `/aws/ecs/flask-app`
- CloudTrail: Account activity monitoring
- GuardDuty: Threat detection enabled

## Files
- `monitoring/docker-compose.yml` - Monitoring stack
- `monitoring/prometheus/prometheus.yml` - Scrape config
- `app/app.py` - Flask app with metrics endpoint

