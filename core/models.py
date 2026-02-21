from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict


class Message(BaseModel):
    id: int
    channel: str
    text: str
    normalized_text: str
    date: datetime
    tickers: List[str]
    fraud_signals: List[str] = []
    risk_score: int = 0
    sentiment_score: float = 0.0
    sentiment_label: str = "neutral"
    fraud_score: int = 0
    hype_intensity: Optional[float] = None


class TickerStats(BaseModel):
    symbol: str
    mentions: int
    recent_messages: List[Message]


class HealthResponse(BaseModel):
    status: str
    messages_count: int
    active_channels: int


class FraudAlert(BaseModel):
    high_risk_messages: List[Message]
    total_alerts: int
    top_suspicious_tickers: dict


class HypeIntensity(BaseModel):
    ticker: str
    hype_score: float
    risk_level: str
    breakdown: Dict
    metrics: Dict
    recent_messages: List[Message]


class RealityCheck(BaseModel):
    ticker: str
    safety_indicator: str  # RED/AMBER/GREEN
    risk_level: str
    risk_score: int
    why_explanation: str
    risk_factors: List[str]
    social_hype: float
    fraud_score: int
    fundamentals: Dict
    timestamp: str
