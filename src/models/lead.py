from dataclasses import dataclass
from typing import Optional


@dataclass
class Lead:
    company_name: str
    industry: str
    city: str
    state: str

    website: Optional[str] = None
    phone: Optional[str] = None

    rating: Optional[float] = None
    review_count: Optional[int] = None

    decision_maker: Optional[str] = None
    decision_maker_role: Optional[str] = None
    email: Optional[str] = None

    website_quality: Optional[int] = None
    opportunity_score: Optional[int] = None

    pain_point: Optional[str] = None
    recommended_service: Optional[str] = None

    status: str = "new"