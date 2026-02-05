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
            random_state=0,
            max_iter=300,
            init='k-means++',
            n_init=10
        )
        self.is_fitted = False

    def cluster_data(self, data) -> Tenant:
        with tracer.start_as_current_span("service.cluster_data"):
            logger.info("func.cluster_data()")

            logger.debug("data: %s", data)

            if not self.is_fitted:
                raise KmeansError("KMeans agent is not fitted")
        
            data_cluster = Cluster()

            features = np.array([[
                data.data.mean,
                data.data.mad,
                data.data.n_slope
            ]])
            
            logger.debug("features: %s", features)

            features_scaled = self.scaler.transform(features)

            logger.debug("features_scaled: %s", features_scaled)

            result_kmeans = int(self.kmeans.predict(features_scaled)[0])

            data_cluster.id = str(result_kmeans)
            data_cluster.model = "kmeans"
            data_cluster.centroid = float(self.kmeans.cluster_centers_[result_kmeans][0])
            
            data_cluster = Tenant(
                id=data.id,
                message="clustering data successfully",
                data = data.data,
                cluster = data_cluster
            )

            return data_cluster

    def fit(self, historical_stats: list[dict]):
        with tracer.start_as_current_span("use_case.kmeans_clustering"):
            logger.info("func.fit()") 

            logger.debug("historical_stats: %s", historical_stats)

            X = np.array([
                [s["mean"], s["mad"], s["n_slope"]]
                for s in historical_stats
            ])

            X_scaled = self.scaler.fit_transform(X)
            knn = self.kmeans.fit(X_scaled)
            y_means = knn.fit_predict(X_scaled)

            # Attach predicted cluster labels back into historical_stats
            for idx, label in enumerate(y_means):
                historical_stats[idx]["cluster"] = int(label)

            logger.debug("historical_stats_with_clusters: %s", historical_stats)

            self.is_fitted = True

            return historical_stats
