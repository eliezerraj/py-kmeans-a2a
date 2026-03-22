import logging

from pydantic import ValidationError

from domain.model.entities import Response, FitRequest
from domain.service.cluster_service import ClusterService
from shared.exception.exceptions import A2ARequestError, KmeansError

from opentelemetry import trace
from opentelemetry.sdk.trace import StatusCode, Status 

from infrastructure.config.config import settings

#---------------------------------
# Configure logging
#---------------------------------
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

# Initialize Clustering Service
CLUSTER_SIZE = settings.CLUSTER_SIZE
cluster_service = ClusterService(cluster_size=CLUSTER_SIZE)

try:
    logger.info("loading cluster assets at startup...") 
    #cluster_service.load_cluster_assets("v1")
except KmeansError as exc:
    logger.warning("Cluster assets unavailable at startup: %s", exc)

# Handlers
def handler_cluster_data(payload: dict) -> dict:
    with tracer.start_as_current_span("handler.cluster_data") as span:
        logger.info("def.handler_cluster_data()")  

        try:
            try:
                response = FitRequest.model_validate(payload)
            except (ValidationError, TypeError, ValueError) as exc:
                raise A2ARequestError(
                    "CLUSTER_DATA payload must be an object with 'id' and 'data' fields."
                ) from exc
                
            result = cluster_service.cluster_data(data=response)

            return {
                "message": "clustering data successfully",
                "cluster": result,
            }

        except A2ARequestError:
            raise
        except Exception as e:
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, str(e)))
            logger.error("Error clustering data", exc_info=e)
            raise e

def handler_fit(payload: dict) -> dict:
    with tracer.start_as_current_span("handler.fit") as span:
        logger.info("def.handler_fit()")  

        try:
            if not isinstance(payload, list):
                raise A2ARequestError("CLUSTER_FIT payload must be a JSON array of feature objects.")
            try:
                items = [FitRequest.model_validate(item) for item in payload]
            except (ValidationError, TypeError, ValueError) as exc:
                raise A2ARequestError(
                    "CLUSTER_FIT items must contain numeric feature_01, feature_02, feature_03 fields."
                ) from exc
            result = cluster_service.fit(historical_stats=[item.model_dump() for item in items])
            
            return {
                "message": "clustering fitted successfully",
                "data": result
            }

        except A2ARequestError:
            raise
        except Exception as e:
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, str(e)))
            logger.error("Error fitting clustering service", exc_info=e)
            raise e
