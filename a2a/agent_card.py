
from config.config import settings

AGENT_CARD = {
    "name": settings.APP_NAME,
    "version": settings.VERSION,
    "url": settings.URL_AGENT,
    "protocol": "a2a/1.0",
    "description": "Clustering agent for processing TPS and producing cluster results.",
    "capabilities": [
        {
            "consumes": ["CLUSTER_FIT", "CLUSTER_DATA"],
            "produces": ["CLUSTER_FIT_RESULT","CLUSTER_DATA_RESULT"]
        }
    ],
    "skills": {
        "compute_cluster": "Compute which cluster the data from a given features",
        "fit_cluster": "Training the model using from the given features",
    },
    "endpoints": {
        "message": "/a2a/message"
    }
}
