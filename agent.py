import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import StatusCode, Status 

from config.config import settings
from exception.exceptions import A2ARouterError

from a2a.router import A2ARouter
from a2a.envelope import A2AEnvelope

#---------------------------------
# Configure logging
#---------------------------------
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

# -----------------------------------------
class ClusteringAgent:

    NAME = settings.APP_NAME
    VERSION = settings.VERSION

    def __init__(self):
        self.router = A2ARouter()
        
    def receive(self, envelope: A2AEnvelope) -> A2AEnvelope:
        with tracer.start_as_current_span("agent.receive") as span:
            logger.info("def.receive()") 
            logger.debug("envelope: %s", envelope)

            try:
                result = self.router.route(envelope)
                
                return A2AEnvelope.create(
                    source=self.NAME,
                    target=envelope.source_agent,
                    msg_type="CLUSTER_RESULT",
                    payload=result
                )
            
            except A2ARouterError:
                # Propagate known router errors so controller can return 400
                raise
            except Exception as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                logger.error(f"Error processing envelope: {e}")
                raise e