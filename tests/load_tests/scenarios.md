# AURAX Load Testing Scenarios

## Test User Classes

### 1. AuraxLoadTestUser (Default)
**Purpose**: Simulates normal user behavior patterns
- **Wait time**: 1-3 seconds between requests
- **Distribution**: 
  - 50% text generation
  - 30% code generation
  - 10% image generation
  - 10% system monitoring

### 2. AuraxBurstUser
**Purpose**: Tests system behavior under sudden load spikes
- **Wait time**: 0.1-0.5 seconds (high frequency)
- **Focus**: Simple, fast requests to test scaling

### 3. AuraxPeakHourUser
**Purpose**: Simulates peak usage periods
- **Wait time**: 0.5-2 seconds (medium frequency)
- **Distribution**: 80% text, 20% code (realistic peak patterns)

## Recommended Test Configurations

### Light Load Testing
```bash
locust -f locustfile.py --host=http://localhost:8000 --users 5 --spawn-rate 1 --run-time 120s
```

### Medium Load Testing
```bash
locust -f locustfile.py --host=http://localhost:8000 --users 25 --spawn-rate 3 --run-time 300s
```

### Heavy Load Testing
```bash
locust -f locustfile.py --host=http://localhost:8000 --users 100 --spawn-rate 10 --run-time 600s
```

### Burst Testing
```bash
locust -f locustfile.py --host=http://localhost:8000 -u AuraxBurstUser --users 50 --spawn-rate 25 --run-time 180s
```

### Peak Hour Simulation
```bash
locust -f locustfile.py --host=http://localhost:8000 -u AuraxPeakHourUser --users 75 --spawn-rate 5 --run-time 900s
```

## Performance Metrics to Monitor

### Response Time Targets
- **Health check**: < 50ms
- **System status**: < 200ms
- **Text generation**: < 5s
- **Code generation**: < 8s
- **Image generation**: < 15s
- **Route testing**: < 100ms

### Throughput Targets
- **Minimum**: 10 requests/second
- **Target**: 50 requests/second
- **Peak**: 100+ requests/second

### Error Rate Targets
- **Normal operations**: < 1%
- **Peak load**: < 5%
- **Burst scenarios**: < 10%

## Key Test Scenarios

### 1. Gradual Ramp-Up
Test how the system handles increasing load over time.

### 2. Sudden Spike
Test system resilience to sudden traffic increases.

### 3. Sustained Load
Verify system stability under constant high load.

### 4. Mixed Workload
Test realistic combinations of different request types.

### 5. Resource Exhaustion
Push system to limits to identify breaking points.

## Monitoring During Tests

1. **Grafana Dashboard**: Watch real-time metrics
2. **Resource Usage**: CPU, Memory, Disk I/O
3. **Response Times**: P50, P95, P99 percentiles
4. **Error Rates**: By endpoint and status code
5. **Model Performance**: Usage distribution across models

## Post-Test Analysis

1. **Performance Bottlenecks**: Identify slowest endpoints
2. **Resource Constraints**: CPU/Memory limitations
3. **Scaling Opportunities**: Auto-scaling triggers
4. **Error Patterns**: Common failure modes
5. **Optimization Targets**: Priority improvements