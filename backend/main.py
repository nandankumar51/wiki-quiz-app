from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn
import os

from database import SessionLocal, engine
import models
import schemas
from services.scraper import WikipediaScraper
from services.llm_service import LLMQuizGenerator

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Wiki Quiz API",
    description="Generate quizzes from Wikipedia articles using LLM",
    version="1.0.0"
)

# CORS middleware - Allow all origins for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Wiki Quiz API is running", "version": "1.0.0"}


@app.post("/api/generate-quiz", response_model=schemas.QuizResponse)
async def generate_quiz(request: schemas.QuizRequest, db: Session = Depends(get_db)):
    """
    Generate a quiz from a Wikipedia article URL.
    
    - Scrapes the Wikipedia page
    - Extracts key information
    - Generates quiz questions using LLM
    - Stores everything in database
    """
    try:
        # Check if URL already exists (caching)
        existing_quiz = db.query(models.Quiz).filter(
            models.Quiz.url == request.url
        ).first()
        
        if existing_quiz and not request.force_regenerate:
            # Return cached quiz
            return schemas.QuizResponse.from_orm(existing_quiz)
        
        # Scrape Wikipedia article
        scraper = WikipediaScraper()
        article_data = scraper.scrape_article(request.url)
        
        if not article_data:
            raise HTTPException(status_code=400, detail="Failed to scrape Wikipedia article")
        
        # Generate quiz using LLM
        llm_generator = LLMQuizGenerator()
        quiz_data = llm_generator.generate_quiz(
            title=article_data['title'],
            summary=article_data['summary'],
            content=article_data['full_text'],
            sections=article_data['sections']
        )
        
        # Create or update database entry
        if existing_quiz:
            # Update existing quiz
            existing_quiz.title = article_data['title']
            existing_quiz.summary = article_data['summary']
            existing_quiz.raw_html = article_data.get('raw_html', '')
            existing_quiz.key_entities = article_data['key_entities']
            existing_quiz.sections = article_data['sections']
            existing_quiz.quiz_questions = quiz_data['quiz']
            existing_quiz.related_topics = quiz_data['related_topics']
            db.commit()
            db.refresh(existing_quiz)
            return schemas.QuizResponse.from_orm(existing_quiz)
        else:
            # Create new quiz entry
            db_quiz = models.Quiz(
                url=request.url,
                title=article_data['title'],
                summary=article_data['summary'],
                raw_html=article_data.get('raw_html', ''),
                key_entities=article_data['key_entities'],
                sections=article_data['sections'],
                quiz_questions=quiz_data['quiz'],
                related_topics=quiz_data['related_topics']
            )
            db.add(db_quiz)
            db.commit()
            db.refresh(db_quiz)
            return schemas.QuizResponse.from_orm(db_quiz)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")


@app.get("/api/quizzes", response_model=List[schemas.QuizListItem])
async def get_all_quizzes(db: Session = Depends(get_db)):
    """
    Get all quizzes from history (for Tab 2).
    """
    quizzes = db.query(models.Quiz).order_by(models.Quiz.created_at.desc()).all()
    return quizzes


@app.get("/api/quizzes/{quiz_id}", response_model=schemas.QuizResponse)
async def get_quiz_by_id(quiz_id: int, db: Session = Depends(get_db)):
    """
    Get a specific quiz by ID (for viewing details).
    """
    quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


@app.delete("/api/quizzes/{quiz_id}")
async def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    """
    Delete a quiz from history.
    """
    quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    db.delete(quiz)
    db.commit()
    return {"message": "Quiz deleted successfully"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
