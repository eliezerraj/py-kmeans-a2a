import logging
import os
import time

from log.logger import setup_logger
from tracing.tracer import setup_tracer

from agent import ClusteringAgent
from a2a.agent_card import AGENT_CARD
from a2a.envelope import A2AEnvelope
from config.config import settings
from exception.exceptions import A2ARouterError, KmeansError

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import status

from contextlib import asynccontextmanager

from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

#---------------------------------
# Initialize tracing
#---------------------------------
VERSION = os.getenv("VERSION")
ACCOUNT = os.getenv("ACCOUNT")
APP_NAME = os.getenv("APP_NAME")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT")) 
OTEL_EXPORTER_OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
OTEL_STDOUT_LOG_GROUP = os.getenv("OTEL_STDOUT_LOG_GROUP", "false").lower() == "true"
LOG_GROUP = os.getenv("LOG_GROUP")

print("---" * 15)
print(f"VERSION: {VERSION}")
print(f"ACCOUNT: {ACCOUNT}")
print(f"APP_NAME: {APP_NAME}")
print(f"HOST: {HOST}")
print(f"PORT: {PORT}")
print(f"SESSION_TIMEOUT: {SESSION_TIMEOUT}")
print(f"OTEL_EXPORTER_OTLP_ENDPOINT: {OTEL_EXPORTER_OTLP_ENDPOINT}")
print(f"LOG_LEVEL: {LOG_LEVEL}")
print(f"OTEL_STDOUT_LOG_GROUP: {OTEL_STDOUT_LOG_GROUP}")
print(f"LOG_GROUP: {LOG_GROUP}")
print("---" * 15)

#---------------------------------
# Configure logging
#---------------------------------
setup_logger(LOG_LEVEL, APP_NAME, OTEL_STDOUT_LOG_GROUP, LOG_GROUP)
logger = logging.getLogger(__name__)

# ---------------------------------
# Lifespan (startup/shutdown)
# ---------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Load the ML model """
    logger.info(" **** Starting up the application...")
    yield
    logger.info(" **** Shutting down the application...")
    logger.info(" **** Closing resources (5 seconds)...")
    time.sleep(0)
    logger.info(" **** Resources Closed...")
    logger.info(" **** Shutting down complete, bye ...")

# ---------------------------------
# Create FastAPI instance
# ---------------------------------
app = FastAPI(
    title="Stat Inference API",
    version="1.0.0",
    lifespan=lifespan
)

#---------------------------------
# Configure tracer
#---------------------------------
setup_tracer(APP_NAME, OTEL_EXPORTER_OTLP_ENDPOINT)
tracer = trace.get_tracer(__name__)

# Instrument FastAPI + requests
FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()

agent = ClusteringAgent()

# ---------------------------------------------------------------
# methods to handle API requests
# ---------------------------------------------------------------
@app.get("/info")
def get_info():
    with tracer.start_as_current_span("controller.get_info"):
        """Get application settings information."""
        logger.info("func.get_info()")

        return settings

@app.get("/.well-known/agent.json")
def agent_card():
    with tracer.start_as_current_span("controller.get_agent_card"):
        """Get application agent card information."""
        logger.info("func.get_agent_card()")
        
        return AGENT_CARD
    
@app.post("/a2a/message")
def handle_message(envelope: A2AEnvelope):
    with tracer.start_as_current_span("controller.handle_message") as span:
        """Handle an A2A message."""
        logger.info("func.handle_message()")
    
        try:
            result = agent.receive(envelope)
            span.set_status(Status(StatusCode.OK))
            return result

        except KmeansError as e:
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, str(e)))
            logger.error(f"Error handling message: {e}")
            return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except A2ARouterError as e:
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, str(e)))
            logger.warning(f"Bad request: {e}")
            return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, str(e)))
            logger.error(f"Error handling message: {e}")
            return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)