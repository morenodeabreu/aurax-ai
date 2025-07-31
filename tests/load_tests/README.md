# AURAX Load Testing Guide

## Overview

This directory contains load testing configurations for the AURAX backend using [Locust](https://locust.io/), a modern load testing framework written in Python.

## Quick Start

### Prerequisites

1. Install Locust:
```bash
pip install locust
```

2. Ensure the AURAX backend is running:
```bash
cd backend
python main.py
```

### Running Tests

#### Web UI Mode (Interactive)
```bash
# Start Locust web interface
locust -f locustfile.py --host=http://localhost:8000

# Access the web UI at http://localhost:8089
# Configure number of users and spawn rate through the web interface
```

#### Headless Mode (Automated)
```bash
# Basic load test
locust -f locustfile.py --host=http://localhost:8000 --users 10 --spawn-rate 2 --run-time 60s --headless

# Generate HTML report
locust -f locustfile.py --host=http://localhost:8000 --users 50 --spawn-rate 5 --run-time 300s --html=report.html

# Save CSV results
locust -f locustfile.py --host=http://localhost:8000 --users 100 --spawn-rate 10 --run-time 600s --headless --csv=aurax_load_test
```

## Test Scenarios

### 1. Regular User (`AuraxLoadTestUser`)
- **Frequency**: 70% of traffic
- **Behavior**: Realistic user patterns with 1-3 second delays
- **Tasks**:
  - Text generation (50%)
  - Code generation (30%)
  - Image generation (10%)
  - Model routing tests (10%)

### 2. Burst User (`AuraxBurstUser`)
- **Frequency**: 20% of traffic
- **Behavior**: High-frequency requests (0.1-0.5s delays)
- **Use Case**: Testing system under stress/spike conditions

### 3. Peak Hour User (`AuraxPeakHourUser`)
- **Frequency**: 10% of traffic
- **Behavior**: Medium frequency (0.5-2s delays)
- **Use Case**: Simulating production peak loads

## Available Tags

Use tags to run specific test scenarios:

```bash
# Run only health checks
locust -f locustfile.py --host=http://localhost:8000 --tags health

# Run generation tests
locust -f locustfile.py --host=http://localhost:8000 --tags generate

# Run routing tests
locust -f locustfile.py --host=http://localhost:8000 --tags routing

# Exclude scraping tests
locust -f locustfile.py --host=http://localhost:8000 --exclude-tags scrape
```

## Test Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LOCUST_HOST` | Target host URL | `http://localhost:8000` |
| `LOCUST_USERS` | Number of concurrent users | `10` |
| `LOCUST_SPAWN_RATE` | Users spawned per second | `2` |
| `LOCUST_RUN_TIME` | Test duration | `60s` |

### Custom Configurations

Create a `locust.conf` file for reusable settings:

```ini
# locust.conf
host = http://localhost:8000
users = 50
spawn-rate = 5
run-time = 300s
headless = true
html = report.html
csv = results
```

## Performance Benchmarks

### Expected Performance (Local Development)

| Metric | Target | Notes |
|--------|--------|-------|
| **Response Time (p95)** | < 2s | For text/code generation |
| **Response Time (p99)** | < 5s | For complex queries |
| **Throughput** | > 10 req/s | Sustained load |
| **Error Rate** | < 1% | HTTP 5xx errors |
| **Success Rate** | > 95% | Valid responses |

### Monitoring During Tests

1. **Backend Metrics**: Available at http://localhost:8000/metrics
2. **Prometheus**: http://localhost:9090 (if running)
3. **Grafana**: http://localhost:3000 (if running)

## Advanced Usage

### Custom Load Patterns

```bash
# Gradual ramp-up test
locust -f locustfile.py --host=http://localhost:8000 --users 100 --spawn-rate 1 --run-time 600s

# Spike test
locust -f locustfile.py --host=http://localhost:8000 --users 1000 --spawn-rate 100 --run-time 30s

# Endurance test
locust -f locustfile.py --host=http://localhost:8000 --users 50 --spawn-rate 5 --run-time 3600s
```

### Docker Testing

```bash
# Run tests against Dockerized backend
docker-compose up -d
locust -f locustfile.py --host=http://localhost:8000 --users 100 --spawn-rate 10 --run-time 300s
```

### Distributed Testing

```bash
# Master node
locust -f locustfile.py --master --host=http://localhost:8000

# Worker nodes (run on separate machines)
locust -f locustfile.py --worker --master-host=master-ip
```

## Interpreting Results

### Key Metrics to Monitor

1. **Response Times**
   - p50 (median): Should be consistent
   - p95: Shows performance under load
   - p99: Identifies worst-case scenarios

2. **Throughput**
   - Requests per second (RPS)
   - Requests per minute (RPM)

3. **Error Analysis**
   - HTTP status codes
   - Error types and messages
   - Failure patterns

4. **Resource Utilization**
   - CPU usage
   - Memory consumption
   - Network I/O

### Sample Report Analysis

```
Type     Name              # reqs      # fails |    Avg     Min     Max    Med |   req/s
--------|-----------------|-------|-----------|-------|-------|-------|-------|--------
POST     /generate         1000        5(0.50%) |  1200    500    5000   1100 |   16.7
GET      /health           200         0(0.00%) |    50     10     200     45 |    3.3
POST     /route            100         2(2.00%) |   800    300    2000    750 |    1.7
```

## Troubleshooting

### Common Issues

1. **Connection Errors**
   - Ensure backend is running on correct port
   - Check firewall settings
   - Verify network connectivity

2. **High Response Times**
   - Monitor backend resource usage
   - Check if models are properly loaded
   - Verify database/RAG system performance

3. **Memory Issues**
   - Reduce number of concurrent users
   - Monitor memory usage during tests
   - Consider model unloading strategies

### Debug Mode

```bash
# Enable debug logging
locust -f locustfile.py --host=http://localhost:8000 --loglevel=DEBUG

# Verbose output
locust -f locustfile.py --host=http://localhost:8000 --print-stats
```

## Integration with CI/CD

### GitHub Actions Example

```yaml
# .github/workflows/load-test.yml
name: Load Test
on: [push, pull_request]

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install Locust
        run: pip install locust
      - name: Start Backend
        run: |
          cd backend
          python main.py &
          sleep 30
      - name: Run Load Test
        run: |
          cd tests/load_tests
          locust -f locustfile.py --host=http://localhost:8000 --users 50 --spawn-rate 5 --run-time 120s --headless --csv=results
```

## Next Steps

1. **Performance Tuning**: Use results to optimize backend
2. **Scaling Tests**: Test with increasing user loads
3. **Production Testing**: Validate against staging environment
4. **Auto-scaling**: Test dynamic scaling capabilities
5. **Monitoring Integration**: Correlate load test results with system metrics