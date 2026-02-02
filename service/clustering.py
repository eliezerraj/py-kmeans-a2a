import logging
from opentelemetry import trace

from exception.exceptions import KmeansError
from model.entities import Tenant, Cluster

import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

#---------------------------------
# Configure logging
#---------------------------------
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

#---------------------------------
# Compute Clustering

class ClusteringService:

    def __init__(self, cluster_size: int):
        self.scaler = StandardScaler()
        self.kmeans = KMeans(
            n_clusters=cluster_size,
            random_state=42,
            n_init="auto"
        )
        self.is_fitted = False

    def cluster_data(self, data: Tenant) -> Tenant:
        with tracer.start_as_current_span("service.cluster_data"):
            logger.info("func.cluster_data()")

            logger.debug("data: %s", data)

            if not self.is_fitted:
                raise KmeansError("KMeans agent is not fitted")
        
            data_cluster = Cluster()

            features = np.array([[
                data.stat.mean,
                data.stat.std,
                data.stat.max
            ]])
            
            logger.debug("features: %s", features)

            features_scaled = self.scaler.transform(features)

            logger.debug("features_scaled: %s", features_scaled)

            cluster = int(self.kmeans.predict(features_scaled)[0])

            data_cluster.id = str(cluster)
            data_cluster.model = "kmeans"
            data_cluster.centroid = float(self.kmeans.cluster_centers_[cluster][0])
            
            data_cluster = Tenant(
                id=data.id,
                message="clustering data successfully",
                stat = data.stat,
                cluster = data_cluster
            )

            return data_cluster

    def fit(self, historical_stats: list[dict]):
        with tracer.start_as_current_span("use_case.kmeans_clustering"):
            logger.info("func.fit()") 

            logger.debug("historical_stats: %s", historical_stats)

            X = np.array([
                [s["mean"], s["std"], s["max"]]
                for s in historical_stats
            ])

            X_scaled = self.scaler.fit_transform(X)
            self.kmeans.fit(X_scaled)

            self.is_fitted = True
