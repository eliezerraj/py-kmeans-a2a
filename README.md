# py-kmeans-a2a

py-kmeans-a2a

## Features

### Simple / Robust

    [ mean, std, slope ]

Feature	Meaning in TPS

    mean:	Average load level
    std:	Volatility / jitter
    slope:	Trend (ramping up or down)

    | Scenario           | mean | std  | slope |
    | ------------------ | ---- | ---- | ----- |
    | Stable low traffic | low  | low  | ~0    |
    | Healthy high load  | high | low  | ~0    |
    | Sudden growth      | mid  | low  | +     |
    | Degrading service  | mid  | high | −     |


### Rate-Limit / Saturation Focused

    [ mean, std, p95 ]

Feature	Meaning in TPS

    mean:	Typical throughput
    std:	Variability
    p95:	Near-peak pressure

    | Scenario       | mean | std | p95      |
    | -------------- | ---- | --- | -------- |
    | Stable system  | 8    | 0.4 | 9        |
    | Bursty traffic | 8    | 1.2 | 14       |
    | Saturated      | 10   | 0.3 | 15 (cap) |
    | Throttled      | 7    | 2.0 | 15       |

### Advanced / Research

    [ mean, std, slope, autocorr ]

Feature	Meaning in TPS

    mean:	Load level
    std:	Noise
    slope:	Direction
    autocorr:	Temporal dependency

    Autocorr	Interpretation
    ~1.0	Strong inertia / throttling
    ~0.0	Random traffic
    <0	    Oscillation / instability

    | Scenario      | mean | std  | slope | autocorr  |
    | ------------- | ---- | ---- | ----- | --------- |
    | Smooth growth | mid  | low  | +     | high      |
    | Bursty random | mid  | high | ~0    | low       |
    | Rate-limited  | high | low  | ~0    | very high |
    | Unstable      | mid  | high | ±     | negative  |


## Diagram

## create venv

    python3 -m venv .venv

## activate

    source .venv/bin/activate

## install requirements

    pip install -r requirements.txt

## run (root)

    uvicorn main:app --host 0.0.0.0 --port 8001 --no-access-log --log-level debug

## test Local

    export VERSION=0.1
    export ACCOUNT=aws:999999999
    export APP_NAME=ky-kmeans-a2a.localhost
    export HOST=127.0.0.1 
    export URL_AGENT=http://127.0.0.1:8001 
    export PORT=8001
    export SESSION_TIMEOUT=3000
    export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318/v1/traces
    export LOG_LEVEL=DEBUG 
    export OTEL_STDOUT_LOG_GROUP=True
    export LOG_GROUP=/mnt/c/Eliezer/log/ky-kmeans-a2a.log

## Endpoint    

    curl --location 'http://localhost:8000/.well-known/agent.json'

    curl --location 'http://localhost:8000/.well-known/agent.json'

    curl --location 'http://localhost:8001/a2a/message' \
        --header 'Content-Type: application/json' \
        --data '{
        "message_id":"123",
        "source_agent":"producer-agent",
        "target_agent":"cluster-agent",
        "message_type":"CLUSTER_DATA",
        "timestamp":"2026-01-29T21:01:00Z",
        "payload":{
            "id":"id-002",
            "stat":{
                "mean":11,
                "std":8,
                "max":38
            }
        }
    }'

    curl --location 'http://localhost:8001/a2a/message' \
        --header 'Content-Type: application/json' \
        --data '{
        "message_id": "123",
        "source_agent": "producer-agent",
        "target_agent": "cluster-agent",
        "message_type": "CLUSTER_FIT",
        "payload": [
            {"mean": 13, "std": 9, "max": 36},
            {"mean": 9, "std": 7, "max": 32},
            {"mean": 14, "std": 10, "max": 50},
            {"mean": 21, "std": 10, "max": 48},
            {"mean": 18, "std": 9, "max": 45},
            {"mean": 25, "std": 10, "max": 50},
            {"mean": 31, "std": 9, "max": 50},
            {"mean": 30, "std": 11, "max": 50},
            {"mean": 35, "std": 9, "max": 50}              
        ],
        "timestamp": "2026-01-29T21:01:00Z"
    }'