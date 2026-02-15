
from config.config import settings

AGENT_CARD = {
    "name": settings.APP_NAME,
    "version": settings.VERSION,
    "url": settings.URL_AGENT,
    "protocol": "a2a/1.0",
    "description": "Performs K-Means clustering on multi-dimensional features.",
    "maintainer": {
        "contact": "eliezerral@gmail.com",
        "organization": "MLOps"
    },
    "capabilities": [
        {
            "intent": "DATA_CLASSIFICATION",
            "consumes": ["CLUSTER_FIT", "CLUSTER_DATA"],
            "produces": ["CLUSTER_FIT_RESULT","CLUSTER_DATA_RESULT"],
            "input_modes": ["application/json"],
            "output_modes": ["application/json"],            
            "schema": {
                "CLUSTER_DATA":{
                    "type": "object",
                    "required": ["id", "data"],
                    "properties": {
                        "id": { "type": "string" },
                        "data": { 
                            "type": "object", 
                            "additionalProperties": { "type": "number" } 
                        }
                    },
                },
                "CLUSTER_FIT": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": { "type": "number" }
                    },
                    "minItems": 3
                },
            },        
        },
    ],
    "skills": {
        "compute_cluster": "Compute which cluster the data from a given features",
        "fit_cluster": "Training the model using from the given features",
    },
    "endpoints": {
        "message": "/a2a/message",
        "health": "/info",
    },
    "security": {
        "type": "none", 
        "description": "Localhost testing mode"
    }    
}
