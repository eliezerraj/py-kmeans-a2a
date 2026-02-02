import logging
from opentelemetry import trace

from pydantic import BaseModel

from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4
from typing import Any

#---------------------------------
# Configure logging
#---------------------------------
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

class A2AEnvelope(BaseModel):
    message_id: str
    source_agent: str
    target_agent: str
    message_type: str
    timestamp: str
    payload: Any

    @staticmethod
    def create(source, target, msg_type, payload):
        with tracer.start_as_current_span("a2a.create_envelope"):    
            logger.info("def.create()") 

            return A2AEnvelope(
                message_id=str(uuid4()),
                source_agent=source,
                target_agent=target,
                message_type=msg_type,
                timestamp=datetime.utcnow().isoformat(),
                payload=payload,
            )
