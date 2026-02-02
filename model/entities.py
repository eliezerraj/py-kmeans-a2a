from pydantic import BaseModel
from typing import Optional

class Tenant(BaseModel):
    id: str
    tps: int
    timestamp: Optional[str] = None
    message: Optional[str] = None
    stat: Optional['Stat'] = None
    cluster: Optional['Cluster'] = None

class Stat(BaseModel):
    distribution_type: Optional[str] = None
    confidence: Optional[float] = None
    std: Optional[float] = None
    mean: Optional[float] = None
    variance: Optional[float] = None
    max: Optional[float] = None
    min: Optional[float] = None
    population: Optional[float] = None

class Cluster(BaseModel):
    id: Optional[str] = None
    model: Optional[str] = None
    members: Optional[list[str]] = None
    centroid: Optional[float] = None

class HistoricalData(BaseModel):
    mean: Optional[float] = None
    std: Optional[float] = None
    max: Optional[float] = None

class MessageResponse(BaseModel):
    message: str