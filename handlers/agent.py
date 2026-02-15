import logging
from model.entities import Response
from opentelemetry import trace
from opentelemetry.sdk.trace import StatusCode, Status 

from service.clustering import ClusteringService

#---------------------------------
# Configure logging
#---------------------------------
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

# Initialize Clustering Service
CLUSTER_SIZE = 3
cluster_service = ClusteringService(cluster_size=CLUSTER_SIZE)

# Handlers
def handler_cluster_data(payload: dict) -> dict:
    with tracer.start_as_current_span("handler.cluster_data") as span:
        logger.info("def.handler_cluster_data()")  
        logger.debug("payload: %s", payload)

        try:
            response = Response.parse_obj(payload)
            result = cluster_service.cluster_data(data=response)
            return result

        except Exception as e:
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, str(e)))
            logger.error("Error clustering data", exc_info=e)
            raise e

def handler_fit(payload: dict) -> dict:
    with tracer.start_as_current_span("handler.fit") as span:
        logger.info("def.handler_fit()")  
        logger.debug("payload: %s", payload)

        try:
            result = cluster_service.fit(historical_stats=payload)
            return {
                "message": "clustering fitted successfully",
                "data": result
            }

        except Exception as e:
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, str(e)))
            logger.error("Error fitting clustering service", exc_info=e)
            raise e
