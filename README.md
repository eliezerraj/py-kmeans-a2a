# py-kmeans-a2a

py-kmeans-a2a

## Diagram

# create venv

    python3 -m venv .venv

# activate

    source .venv/bin/activate

# install requirements

    pip install -r requirements.txt

# run (root)

    uvicorn main:app --host 0.0.0.0 --port 8000 --no-access-log --log-level debug

## test Local

    export VERSION=0.1
    export ACCOUNT=aws:999999999
    export APP_NAME=ky-kmeans-a2a.localhost
    export HOST=127.0.0.1 
    export PORT=8001
    export SESSION_TIMEOUT=3000
    export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318/v1/traces
    export LOG_LEVEL=DEBUG 
    export OTEL_STDOUT_LOG_GROUP=True
    export LOG_GROUP=/mnt/c/Eliezer/log/ky-kmeans-a2a.log

## Endpoint    

    curl --location 'http://localhost:8000/.well-known/agent.json'

    curl --location 'http://localhost:8000/.well-known/agent.json'

    curl --location 'http://localhost:8000/a2a/message' \
        --header 'Content-Type: application/json' \
        --data '{
        "message_id": "123",
        "source_agent": "producer-agent",
        "target_agent": "stat-inference-agent",
        "message_type": "TPS_EVENT",
        "payload": {
            "id": "id-002",
            "tps": 3,
            "timestamp": "2026-01-29T21:01:00Z"
        },
        "timestamp": "2026-01-29T21:01:00Z"
        }'
