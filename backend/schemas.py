from pydantic import BaseModel, HttpUrl, Field
from typing import List, Dict, Optional
from datetime import datetime


class QuizRequest(BaseModel):
    """Request schema for quiz generation."""
    url: str = Field(..., description="Wikipedia article URL")
    force_regenerate: bool = Field(
        default=False,
        description="Force regeneration even if quiz exists in cache"
    )


class QuizQuestion(BaseModel):
    """Single quiz question schema."""
    question: str
    options: List[str]
    answer: str
    difficulty: str = Field(..., description="easy, medium, or hard")
    explanation: str


class KeyEntities(BaseModel):
    """Extracted entities from the article."""
    people: List[str] = []
    organizations: List[str] = []
    locations: List[str] = []


class QuizResponse(BaseModel):
    """Response schema for generated quiz."""
    id: int
    url: str
    title: str
    summary: str
    key_entities: Dict[str, List[str]]
    sections: List[str]
    quiz: List[QuizQuestion] = Field(..., validation_alias='quiz_questions', serialization_alias='quiz')
    related_topics: List[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class QuizListItem(BaseModel):
    """Schema for quiz list items in history view."""
    id: int
    url: str
    title: str
    summary: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
