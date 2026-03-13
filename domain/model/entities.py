from pydantic import BaseModel
from typing import Optional


class FitRequest(BaseModel):
    feature_01: float
    feature_02: float
    feature_03: float


class Response(BaseModel):
    id: str
    message: Optional[str] = None
    data: Optional['Data'] = None
    cluster: Optional['Cluster'] = None


class Data(BaseModel):
    feature_01: Optional[float] = None
    feature_02: Optional[float] = None
    feature_03: Optional[float] = None


class Cluster(BaseModel):
    id: Optional[str] = None
    model: Optional[str] = None
    members: Optional[dict] = None
    centroid: Optional[list[float]] = None


class MessageResponse(BaseModel):
    message: str