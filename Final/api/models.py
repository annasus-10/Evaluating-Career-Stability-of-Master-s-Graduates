from pydantic import BaseModel
from typing import Optional, List

class CareerRecommendation(BaseModel):
    career_match: str
    similarity: float
    GCSI: float
    GCSI_imputed: bool
    hybrid_score: float
    A_MEDIAN: Optional[float]
    automation_probability: Optional[float]
    top_skills: Optional[List[str]]
    technology_items: Optional[int]
    hot_tech_items: Optional[int]

class RecommendationResponse(BaseModel):
    program_name: str
    program_type: str
    broad_field: str
    degree_norm: str
    total_candidates: int
    recommendations: List[CareerRecommendation]

class FieldOverview(BaseModel):
    broad_field: str
    program_count: int
    avg_gcsi: float
    avg_salary: Optional[float]
    avg_automation_risk: float
    top_careers: List[str]

class CareerDetail(BaseModel):
    career_match: str
    SOC6: Optional[str]
    GCSI: float
    income_strength: Optional[float]
    employment_scale: Optional[float]
    wage_stability: Optional[float]
    automation_safety: Optional[float]
    A_MEDIAN: Optional[float]
    TOT_EMP: Optional[float]
    automation_probability: Optional[float]
    top_skills: Optional[List[str]]
    technology_items: Optional[int]
    hot_tech_items: Optional[int]
    in_demand_items: Optional[int]

class DropdownField(BaseModel):
    broad_field: str
    program_count: int

class DropdownProgram(BaseModel):
    program_name: str
    program_type: str
    degree_norm: str