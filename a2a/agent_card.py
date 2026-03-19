
from infrastructure.config.config import settings

AGENT_CARD = {
    "name": settings.APP_NAME,
    "description": "Performs K-Means clustering on multi-dimensional features.",
    "version": settings.VERSION,
    "provider": {
        "organization": "MLOps",
        "url": settings.URL_AGENT,
    },
    "documentationUrl": f"{settings.URL_AGENT}/info",
    "supportedInterfaces": [
        {
            "url": f"{settings.URL_AGENT}/a2a/message",
            "protocolBinding": "HTTP+JSON",
            "protocolVersion": "1.0",
        }
    ],
    "capabilities": {
        "streaming": False,
        "pushNotifications": False,
        "stateTransitionHistory": False,
        "extendedAgentCard": False,
    },
    "defaultInputModes": ["application/json"],
    "defaultOutputModes": ["application/json"],
    "skills": [
        {
            "id": "CLUSTER_FIT",
            "name": "Cluster Fit",
            "description": "Trains the K-Means model using a list of numeric feature objects.",
            "tags": ["clustering", "training", "kmeans"],
            "examples": [
                '[{"feature_a": 1.2, "feature_b": 3.4}, {"feature_a": 1.5, "feature_b": 3.1}, {"feature_a": 8.2, "feature_b": 9.4}]'
            ],
            "inputModes": ["application/json"],
            "outputModes": ["application/json"],
        },
        {
            "id": "CLUSTER_DATA",
            "name": "Cluster Data",
            "description": "Assigns a feature object to a cluster using the trained K-Means model.",
            "tags": ["clustering", "classification", "kmeans"],
            "examples": [
                '{"id": "sample-1", "data": {"feature_a": 2.1, "feature_b": 3.7}}'
            ],
            "inputModes": ["application/json"],
            "outputModes": ["application/json"],
        }
    ]
}
