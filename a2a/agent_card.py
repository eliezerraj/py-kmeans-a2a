
from infrastructure.config.config import settings

AGENT_CARD = {
    "name": settings.APP_NAME,
    "description": "Performs K-Means clustering on multi-dimensional features.",
    "version": settings.VERSION,
    "provider": {
        "organization": "eliezer-junior",
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
            "inputSchema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "feature_01": { "type": "number" , "description": "First numeric feature for clustering" },
                        "feature_02": { "type": "number" , "description": "Second numeric feature for clustering" },
                        "feature_03": { "type": "number" , "description": "Third numeric feature for clustering" }
                    },
                    "required": ["feature_01", "feature_02", "feature_03"]
                }
            },
            "examples": [
                {"feature_01": 1.2, "feature_02": 3.4, "feature_03": 5.6}, 
                {"feature_01": 1.5, "feature_02": 3.1, "feature_03": 4.8}, 
                {"feature_01": 8.2, "feature_02": 9.4, "feature_03": 7.1}
            ],
            "inputModes": ["application/json"],
            "outputModes": ["application/json"],
        },
        {
            "id": "CLUSTER_DATA",
            "name": "Cluster Data",
            "description": "Assigns a feature object to a cluster using the trained K-Means model.",
            "tags": ["clustering", "classification", "kmeans"],
            "inputSchema": {
                "type": "object",
                "properties": {
                    "feature_01": { "type": "number" , "description": "First numeric feature for clustering" },
                    "feature_02": { "type": "number" , "description": "Second numeric feature for clustering" },
                    "feature_03": { "type": "number" , "description": "Third numeric feature for clustering" }
                },
                "required": ["feature_01", "feature_02", "feature_03"]
            },
            "examples":{"feature_01": 2.1, 
                        "feature_02": 3.7, 
                        "feature_03": 4.5,
                    },
            "inputModes": ["application/json"],
            "outputModes": ["application/json"],
        }
    ]
}
