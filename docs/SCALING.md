# AURAX Auto-Scaling Strategy - Sprint 4

## Overview

Este documento descreve as estratégias de auto-scaling para o sistema AURAX, considerando diferentes ambientes de deployment (desenvolvimento, staging, produção) e plataformas (RunPod Serverless, Kubernetes, Docker).

## 🚀 RunPod Serverless Auto-Scaling

### Configuração Nativa
RunPod oferece auto-scaling automático baseado em demanda de requisições:

```python
# Configuração exemplo para deploy RunPod
{
    "worker_count": {
        "min": 1,
        "max": 10,
        "target_utilization": 0.7
    },
    "scaling_policy": {
        "scale_up_threshold": 5,      # requisições em fila
        "scale_down_delay": 300,      # 5 minutos
        "cold_start_timeout": 60      # 1 minuto
    }
}
```

### Métricas de Scaling
- **Scale Up**: Quando > 5 requisições estão em fila
- **Scale Down**: Após 5 minutos de baixa utilização
- **Cold Start**: Tolerância de 60s para novos containers

### Custos por Scaling
| Workers | Cost/hour | Use Case |
|---------|-----------|----------|
| 1 worker | $0.20 | Desenvolvimento |
| 3-5 workers | $0.60-1.00 | Produção normal |
| 10+ workers | $2.00+ | Picos de tráfego |

## 🐳 Docker Compose Auto-Scaling

### Limitações
Docker Compose não oferece auto-scaling nativo, mas podemos:

1. **Usar docker-compose scale** (manual):
```bash
# Escalar para 3 instâncias do backend
docker-compose up --scale aurax-backend=3
```

2. **Implementar health checks**:
```yaml
# docker-compose.yml
services:
  aurax-backend:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

3. **Load Balancer com NGINX**:
```nginx
upstream aurax_backend {
    server aurax-backend-1:8000;
    server aurax-backend-2:8000;
    server aurax-backend-3:8000;
}
```

### Migração para Kubernetes
Para auto-scaling real, recomenda-se migrar para Kubernetes:

```yaml
# kubernetes/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: aurax-backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: aurax-backend
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## 📊 Métricas-Chave para Auto-Scaling

### 1. Request Metrics
```prometheus
# Taxa de requisições por segundo
rate(fastapi_requests_total[5m])

# Latência P95
histogram_quantile(0.95, rate(fastapi_request_duration_seconds_bucket[5m]))

# Requisições em fila
aurax_inprogress_requests
```

### 2. Resource Metrics
```prometheus
# Uso de CPU
process_cpu_seconds_total

# Uso de memória
process_resident_memory_bytes

# Uso de GPU (se aplicável)
nvidia_gpu_utilization_percent
```

### 3. Application Metrics
```prometheus
# Requests por modelo
aurax_model_requests_total{model_type="qwen3:coder"}

# Taxa de erro por endpoint
rate(fastapi_requests_total{status_code!~"2.."}[5m])

# Tempo de processamento por modelo
aurax_model_processing_duration_seconds
```

## 🎯 Thresholds de Scaling

### Scale Up Triggers
| Métrica | Threshold | Ação |
|---------|-----------|------|
| CPU Usage | > 80% por 2min | +1 instance |
| Memory Usage | > 85% por 2min | +1 instance |
| Queue Depth | > 10 requests | +2 instances |
| Response Time P95 | > 10s por 1min | +1 instance |
| Error Rate | > 5% por 30s | +1 instance |

### Scale Down Triggers
| Métrica | Threshold | Ação |
|---------|-----------|------|
| CPU Usage | < 30% por 10min | -1 instance |
| Memory Usage | < 40% por 10min | -1 instance |
| Queue Depth | 0 por 15min | -1 instance |
| Response Time P95 | < 2s por 15min | Considerar -1 |

## 🔧 Implementação por Ambiente

### Desenvolvimento
```yaml
# docker-compose.dev.yml
services:
  aurax-backend:
    deploy:
      replicas: 1
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
```

### Staging
```yaml
# docker-compose.staging.yml
services:
  aurax-backend:
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 4G
          cpus: '2.0'
```

### Produção (RunPod)
```python
# runpod_config.py
SCALING_CONFIG = {
    "min_workers": 2,
    "max_workers": 50,
    "target_concurrency": 10,
    "scale_up_threshold": 0.8,
    "scale_down_threshold": 0.3,
    "cooldown_period": 60
}
```

## 🚨 Alerting Rules

### Critical Alerts
```yaml
# prometheus/alerts.yml
groups:
- name: aurax.scaling
  rules:
  - alert: HighCPUUsage
    expr: process_cpu_seconds_total > 0.9
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: "AURAX high CPU usage"
      
  - alert: HighMemoryUsage
    expr: process_resident_memory_bytes > 4GB
    for: 2m
    labels:
      severity: warning
      
  - alert: HighErrorRate
    expr: rate(fastapi_requests_total{status_code!~"2.."}[5m]) > 0.1
    for: 1m
    labels:
      severity: critical
```

## 📈 Performance Optimization

### 1. Code-Level Optimizations
- **Async/await**: Maximize I/O concurrency
- **Connection pooling**: RAG database connections
- **Caching**: Model responses and embeddings
- **Batch processing**: Multiple requests together

### 2. Infrastructure Optimizations
- **GPU acceleration**: For model inference
- **SSD storage**: Fast model loading
- **CDN**: Static assets and common responses
- **Load balancing**: Distribute requests evenly

### 3. Database Scaling
```python
# Qdrant scaling configuration
QDRANT_CONFIG = {
    "collection_config": {
        "replication_factor": 2,
        "write_consistency_factor": 1,
        "shard_number": 4
    }
}
```

## 📋 Monitoring Dashboard Recommendations

### Key Panels for Scaling Decisions
1. **Request Rate**: Requests/second over time
2. **Response Time**: P50, P95, P99 percentiles
3. **Error Rate**: Percentage of failed requests
4. **Resource Usage**: CPU, Memory, GPU utilization
5. **Queue Depth**: Pending requests
6. **Active Instances**: Current scaling level

### Scaling History Tracking
```prometheus
# Track scaling events
aurax_scaling_events_total{direction="up|down", reason="cpu|memory|queue|manual"}

# Instance count over time
aurax_active_instances
```

## 🔮 Future Enhancements

### 1. Predictive Scaling
- Machine learning models para prever demanda
- Scaling proativo baseado em padrões históricos
- Integração com calendário de eventos

### 2. Cost Optimization
- Spot instances em períodos de baixa demanda
- Mixed instance types baseados em workload
- Scaling schedule para padrões previsíveis

### 3. Multi-Region Scaling
- Geographic load distribution
- Disaster recovery com auto-failover
- Edge computing para latência reduzida

## 📚 Referencias

- [RunPod Serverless Documentation](https://docs.runpod.io/serverless/overview)
- [Kubernetes HPA Guide](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
- [Prometheus Monitoring Best Practices](https://prometheus.io/docs/practices/naming/)
- [FastAPI Performance Tips](https://fastapi.tiangolo.com/deployment/concepts/)