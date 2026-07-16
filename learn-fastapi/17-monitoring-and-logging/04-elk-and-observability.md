# ELK Stack and Observability

## Table of Contents
1. [ELK Stack Setup](#elk)
2. [Filebeat](#filebeat)
3. [Logstash](#logstash)
4. [Kibana](#kibana)
5. [Distributed Tracing](#tracing)
6. [OpenTelemetry](#opentelemetry)
7. [Jaeger and Zipkin](#jaeger-zipkin)
8. [Correlation Across Services](#correlation)
9. [Trace Context Propagation](#propagation)

---

## ELK Stack Setup <a name="elk"></a>

ELK = Elasticsearch + Logstash + Kibana. A stack for collecting, processing, and visualizing logs.

### Docker Compose

```yaml
version: "3.9"

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.12.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms1g -Xmx1g"
    ports:
      - "9200:9200"
    volumes:
      - es_data:/usr/share/elasticsearch/data
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5

  logstash:
    image: docker.elastic.co/logstash/logstash:8.12.0
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline
    ports:
      - "5044:5044"    # Beats input
      - "9600:9600"    # Monitoring
    depends_on:
      elasticsearch:
        condition: service_healthy

  kibana:
    image: docker.elastic.co/kibana/kibana:8.12.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    depends_on:
      elasticsearch:
        condition: service_healthy

  filebeat:
    image: docker.elastic.co/beats/filebeat:8.12.0
    volumes:
      - ./filebeat/filebeat.yml:/usr/share/filebeat/filebeat.yml
      - /var/log:/var/log:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
    depends_on:
      - logstash

volumes:
  es_data:
```

### Logstash Pipeline

```ruby
# logstash/pipeline/logstash.conf
input {
  beats {
    port => 5044
  }

  tcp {
    port => 5000
    codec => json
  }
}

filter {
  # Parse JSON logs
  if [message] =~ /^\{/ {
    json {
      source => "message"
      target => "log"
    }
  }

  # Add fields
  mutate {
    add_field => { "service" => "fastapi-app" }
    add_field => { "environment" => "%{[env]}" }
  }

  # Parse timestamps
  date {
    match => [ "timestamp", "ISO8601" ]
    target => "@timestamp"
  }

  # Parse levels
  mutate {
    uppercase => [ "log.level" ]
  }

  # GeoIP for client IPs
  if [client_ip] {
    geoip {
      source => "client_ip"
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "fastapi-logs-%{+YYYY.MM.dd}"
  }
}
```

---

## Filebeat <a name="filebeat"></a>

Filebeat ships log files to Logstash or Elasticsearch.

```yaml
# filebeat/filebeat.yml
filebeat.inputs:
  # Application logs
  - type: container
    paths:
      - /var/lib/docker/containers/*/*.log
    processors:
      - add_docker_metadata:
          host: "unix:///var/run/docker.sock"
      - decode_json_fields:
          fields: ["message"]
          target: ""
          overwrite_keys: true

  # System logs
  - type: log
    paths:
      - /var/log/syslog
      - /var/log/auth.log

output.logstash:
  hosts: ["logstash:5044"]

# Processors
processors:
  - add_host_metadata:
      when.not.contains.tags: forwarded
  - add_cloud_metadata: ~

logging.level: info
logging.to_files: true
```

---

## Logstash <a name="logstash"></a>

### Processing Pipeline

```ruby
# logstash/pipeline/multi-service.conf
input {
  beats {
    port => 5044
  }
}

filter {
  # Parse FastAPI JSON logs
  json {
    source => "message"
    target => "fastapi"
  }

  # Extract request_id
  if [fastapi][request_id] {
    mutate {
      add_field => { "request_id" => "%{[fastapi][request_id]}" }
    }
  }

  # Parse duration
  if [fastapi][duration_ms] {
    mutate {
      convert => { "[fastapi][duration_ms]" => "float" }
    }
  }

  # Classify log levels
  if [fastapi][level] == "ERROR" {
    mutate { add_tag => ["error"] }
  } else if [fastapi][level] == "WARNING" {
    mutate { add_tag => ["warning"] }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "fastapi-%{+YYYY.MM.dd}"
  }
}
```

---

## Kibana <a name="kibana"></a>

### Index Pattern

```
# Create index pattern in Kibana
# Pattern: fastapi-*
# Time field: @timestamp
```

### Saved Searches

```json
{
  "title": "FastAPI Errors",
  "query": "fastapi.level: ERROR",
  "columns": ["@timestamp", "fastapi.request_id", "fastapi.message", "fastapi.endpoint"],
  "sort": [["@timestamp", "desc"]]
}
```

### Dashboard Panels

```json
{
  "title": "FastAPI Logs Dashboard",
  "panels": [
    {
      "title": "Log Volume by Level",
      "type": "histogram",
      "aggs": {
        "levels": {
          "terms": { "field": "fastapi.level.keyword" }
        }
      }
    },
    {
      "title": "Error Rate Over Time",
      "type": "line",
      "aggs": {
        "errors_over_time": {
          "date_histogram": { "field": "@timestamp", "fixed_interval": "5m" },
          "aggs": {
            "errors": {
              "filter": { "term": { "fastapi.level": "ERROR" } }
            }
          }
        }
      }
    },
    {
      "title": "Top Endpoints by Error Count",
      "type": "terms",
      "aggs": {
        "endpoints": {
          "terms": { "field": "fastapi.endpoint.keyword", "size": 10 }
        }
      }
    }
  ]
}
```

---

## Distributed Tracing <a name="tracing"></a>

Distributed tracing tracks requests across multiple services.

### Trace Components

```
Trace: Complete journey of a request through all services
Span: Single unit of work within a trace (e.g., HTTP call, DB query)
Trace ID: Unique identifier for the entire trace
Span ID: Unique identifier for a single span
Parent Span ID: Links spans together in a tree
```

### Trace Example

```
Trace ID: abc-123

Span 1: API Gateway (10ms)
  └── Span 2: FastAPI Service (50ms)
        ├── Span 3: PostgreSQL Query (20ms)
        ├── Span 4: Redis Cache Get (5ms)
        └── Span 5: Payment Service HTTP Call (25ms)
              └── Span 6: Stripe API Call (20ms)
```

---

## OpenTelemetry <a name="opentelemetry"></a>

OpenTelemetry is the standard for collecting traces, metrics, and logs.

### Installation

```bash
pip install opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation-fastapi opentelemetry-exporter-otlp
```

### Setup

```python
# app/telemetry.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

def setup_telemetry(app: FastAPI):
    # Resource identifies your service
    resource = Resource.create({
        "service.name": "fastapi-app",
        "service.version": "1.0.0",
        "deployment.environment": "production",
    })

    # Tracer provider
    provider = TracerProvider(resource=resource)

    # Exporter (sends to Jaeger, Zipkin, or OTLP collector)
    exporter = OTLPSpanExporter(
        endpoint="http://jaeger:4317",
        insecure=True,
    )

    # Batch processor (batches spans for efficiency)
    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)

    trace.set_tracer_provider(provider)

    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)

    return trace.get_tracer(__name__)
```

### Manual Spans

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    with tracer.start_as_current_span("get_user") as span:
        span.set_attribute("user.id", user_id)

        with tracer.start_as_current_span("db_query"):
            user = await db.fetch_one(
                "SELECT * FROM users WHERE id = $1", user_id
            )

        if not user:
            span.set_attribute("user.found", False)
            raise HTTPException(status_code=404)

        span.set_attribute("user.found", True)
        span.add_event("user_retrieved", {"email": user["email"]})

        return user
```

### Custom Span Attributes

```python
@router.post("/orders")
async def create_order(command: CreateOrderCommand):
    with tracer.start_as_current_span("create_order") as span:
        span.set_attribute("order.user_id", command.user_id)
        span.set_attribute("order.item_count", len(command.items))
        span.set_attribute("order.total", command.total)

        order = await order_service.create(command)

        span.set_attribute("order.id", order.id)
        span.add_event("order_created", {
            "order_id": order.id,
            "total": order.total,
        })

        return order
```

---

## Jaeger and Zipkin <a name="jaeger-zipkin"></a>

### Jaeger Setup

```yaml
# docker-compose.yml addition
services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"  # Jaeger UI
      - "4317:4317"    # OTLP gRPC
      - "4318:4318"    # OTLP HTTP
    environment:
      - COLLECTOR_OTLP_ENABLED=true
```

### Zipkin Setup

```yaml
services:
  zipkin:
    image: openzipkin/zipkin:latest
    ports:
      - "9411:9411"
    environment:
      - STORAGE_TYPE=elasticsearch
      - ES_HOSTS=http://elasticsearch:9200
```

### Viewing Traces

```
Jaeger UI: http://localhost:16686
  - Select service: fastapi-app
  - Click "Find Traces"
  - Click on a trace to see spans

Zipkin UI: http://localhost:9411
  - Select service: fastapi-app
  - Click "Find Traces"
  - Click on a trace to see the waterfall
```

---

## Correlation Across Services <a name="correlation"></a>

### Correlation ID Propagation

```python
# app/middleware/correlation.py
import uuid
from contextvars import ContextVar

correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="")

@app.middleware("http")
async def correlation_middleware(request: Request, call_next):
    # Extract or generate correlation ID
    cid = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    correlation_id_var.set(cid)

    response = await call_next(request)
    response.headers["X-Correlation-ID"] = cid
    return response

# Pass to downstream services
async def call_payment_service(order_id: int):
    cid = correlation_id_var.get()
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://payment-service/charge",
            json={"order_id": order_id},
            headers={"X-Correlation-ID": cid},
        )
    return response.json()
```

### Log Correlation

```python
import structlog

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    cid = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))

    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(correlation_id=cid)

    response = await call_next(request)
    return response

# All logs automatically include correlation_id
logger.info("processing_order", order_id=123)
# Output: {"event": "processing_order", "correlation_id": "abc-123", "order_id": 123}
```

---

## Trace Context Propagation <a name="propagation"></a>

### W3C Trace Context

```python
# OpenTelemetry automatically propagates trace context
# via W3C Trace Context headers:
# traceparent: 00-abc123-span456-01
# tracestate: vendor1=value1

# Service A → Service B automatically includes trace context
# Both services appear in the same trace

# Manual propagation (if not using auto-instrumentation)
from opentelemetry import propagate

@router.post("/orders")
async def create_order(command: CreateOrderCommand):
    # Inject trace context into outgoing headers
    headers = {}
    propagate.inject(headers)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://payment-service/charge",
            json={"amount": command.total},
            headers=headers,  # Trace context is propagated
        )
```

### Context Propagation Diagram

```
Client Request
    ↓ (traceparent header)
API Gateway
    ↓ (traceparent header)
FastAPI Service
    ↓ (traceparent header)
PostgreSQL (auto-instrumented)
    ↑ (traceparent header)
FastAPI Service
    ↓ (traceparent header)
Payment Service
    ↓ (traceparent header)
Stripe API

All services share the same trace ID
Each service creates its own spans
```

---

## Interview Questions

1. **What is the ELK stack and how does it work with FastAPI?**
ELK = Elasticsearch + Logstash + Kibana. FastAPI writes JSON logs → Filebeat ships logs → Logstash processes/enriches → Elasticsearch stores → Kibana visualizes. Provides centralized logging, search, and dashboards.

2. **What is distributed tracing and why is it needed?**
Distributed tracking tracks a request across multiple services. Each service creates spans. A trace ID links all spans. Essential for debugging latency, identifying bottlenecks, and understanding request flow in microservices.

3. **What is OpenTelemetry?**
OpenTelemetry is a vendor-neutral standard for collecting traces, metrics, and logs. It provides SDKs for most languages and integrates with FastAPI via `opentelemetry-instrumentation-fastapi`. Export to Jaeger, Zipkin, Datadog, etc.

4. **How do you propagate trace context across services?**
Use W3C Trace Context headers (`traceparent`). OpenTelemetry auto-injects these headers when making HTTP calls. Receiving services extract the headers to continue the trace. All services share the same trace ID.

5. **What is the difference between Jaeger and Zipkin?**
Both are distributed tracing systems. Jaeger is CNCF-backed, supports OpenTelemetry natively, has better query capabilities. Zipkin is older, simpler, lighter weight. Both provide UI for viewing traces. Choose based on ecosystem and team familiarity.
