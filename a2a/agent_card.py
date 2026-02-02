AGENT_CARD = {
    "name": "clustering-agent",
    "version": "v1",
    "protocol": "a2a/1.0",
    "description": "Clustering agent for processing TPS events and producing cluster results.",
    "capabilities": [
        {
            "consumes": ["CLUSTER_FIT", "CLUSTER_DATA"],
            "produces": ["CLUSTER_RESULT"]
        }
    ],
    "endpoints": {
        "message": "/a2a/message"
    }
}
