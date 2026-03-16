import logging
import threading
from pathlib import Path
import numpy as np
import joblib

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from shared.exception.exceptions import KmeansError, KmeansNotFittedError
from domain.model.entities import Response, Cluster

from opentelemetry import trace
from opentelemetry.sdk.trace import StatusCode, Status 

#---------------------------------
# Configure logging
#---------------------------------
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)
ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets"

#---------------------------------
# Compute Clustering

class ClusteringService:

    # Initialize KMeans model with specified cluster size
    def __init__(self, cluster_size: int):
        self._lock = threading.Lock()
        self.scaler = StandardScaler()
        self.kmeans = KMeans(
            n_clusters=cluster_size,
            random_state=0,
            max_iter=600,
            init='k-means++',
            n_init=10
        )
        self.is_fitted = False
        self.historical_stats = None

    # Cluster incoming data and return cluster assignment.
    def cluster_data(self, data) -> Response:
        with tracer.start_as_current_span("service.cluster_data"):
            logger.info("func.cluster_data()")

            logger.debug("data: %s", data)

            with self._lock:
                if not self.is_fitted:
                    raise KmeansNotFittedError("KMeans model is not fitted. Send CLUSTER_FIT first.")

                feature_values = [v for _, v in sorted(data.data.model_dump().items()) if v is not None]
                features = np.array([feature_values])

                logger.debug("features: %s", features)

                features_scaled = self.scaler.transform(features)

                logger.debug("features_scaled: %s", features_scaled)

                result_kmeans = int(self.kmeans.predict(features_scaled)[0])

                data_cluster = Cluster(
                    id=str(result_kmeans),
                    model="kmeans",
                    centroid=self.kmeans.cluster_centers_[result_kmeans].tolist(),
                    #members=self.get_members(),
                )

                return Response(
                    id=data.id,
                    message="clustering data successfully",
                    data=data.data,
                    cluster=data_cluster,
                )

    # Fit KMeans model with historical stats
    def fit(self, historical_stats: list[dict]):
        with tracer.start_as_current_span("use_case.kmeans_clustering"):
            logger.info("func.fit()") 

            logger.debug("historical_stats: %s", historical_stats)

            with self._lock:
                feature_keys = sorted(k for k in historical_stats[0].keys() if k.startswith("feature_"))
                X = np.array([[s[k] for k in feature_keys] for s in historical_stats])

                X_scaled = self.scaler.fit_transform(X)
                y_means = self.kmeans.fit_predict(X_scaled)

                # Attach predicted cluster labels back into historical_stats
                for idx, label in enumerate(y_means):
                    historical_stats[idx]["cluster"] = int(label)

                logger.debug("historical_stats_with_clusters: %s", historical_stats)

                self.is_fitted = True
                self.historical_stats = historical_stats

                self.save_cluster_assets(
                    model=self.kmeans,
                    scaler=self.scaler,
                    label_map=self.get_members(),
                    features_used=feature_keys,
                )
                
                return historical_stats

    # Return all members of each cluster
    def get_members(self) -> dict:
        with tracer.start_as_current_span("service.get_members"):
            logger.info("func.get_members()")

            if not self.is_fitted:
                raise KmeansNotFittedError("KMeans agent is not fitted")

            clusters = {}
            for item in self.historical_stats:
                cluster_id = item.get("cluster")
                if cluster_id is not None:
                    if cluster_id not in clusters:
                        clusters[cluster_id] = []
                    clusters[cluster_id].append(item)
            
            return clusters

    # Save model and label map to disk for later use
    @staticmethod
    def save_cluster_assets(model, scaler, label_map, version="v1", features_used=None):
        with tracer.start_as_current_span("service.save_cluster_assets") as span:
            logger.info("func.save_cluster_assets()")
            
            assets = {
                "model": model,
                "scaler": scaler,
                "label_map": label_map,
                "features_used": features_used or ["feature_01", "feature_02", "feature_03"],
            }

            try:
                ASSETS_DIR.mkdir(parents=True, exist_ok=True)
                output_path = ASSETS_DIR / f"cluster_agent_{version}.joblib"
                joblib.dump(assets, output_path)
                logger.info("cluster assets saved to %s", output_path)
            except Exception as exc:
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR, str(exc)))

                raise KmeansError(f"Failed to persist cluster assets: {exc}") from exc

    # Load model and label map from disk
    def load_cluster_assets(self, version="v1"):
        with tracer.start_as_current_span("service.load_cluster_assets") as span:
            logger.info("func.load_cluster_assets()")

            try:
                assets_path = ASSETS_DIR / f"cluster_agent_{version}.joblib"
                assets = joblib.load(assets_path)

                self.kmeans = assets["model"]
                label_map = assets.get("label_map", {})
                features_used = assets.get(
                    "features_used",
                    ["feature_01", "feature_02", "feature_03"],
                )
                self.historical_stats = [item for members in label_map.values() for item in members]

                # Backward compatibility: older assets may not include scaler.
                scaler = assets.get("scaler")
                if scaler is None:
                    if self.historical_stats and all(
                        feature in self.historical_stats[0] for feature in features_used
                    ):
                        X = np.array([[s[feature] for feature in features_used] for s in self.historical_stats])
                        scaler = StandardScaler().fit(X)
                        logger.warning(
                            "Loaded legacy cluster assets without scaler; rebuilt scaler from historical stats."
                        )
                    else:
                        raise KmeansError(
                            "Cluster assets are missing scaler metadata and cannot be reconstructed. "
                            "Run CLUSTER_FIT to regenerate assets."
                        )

                self.scaler = scaler
                self.is_fitted = True

                return self.kmeans, label_map, features_used
            
            except FileNotFoundError as exc:
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR, str(exc)))
                raise KmeansError(f"Cluster assets for version '{version}' not found.") from exc