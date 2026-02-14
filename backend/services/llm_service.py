import os
from typing import Dict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import json

load_dotenv()


class QuizQuestionSchema(BaseModel):
    """Schema for a single quiz question."""
    question: str = Field(description="The quiz question text")
    options: List[str] = Field(description="Four answer options (A-D)")
    answer: str = Field(description="The correct answer from the options")
    difficulty: str = Field(description="Difficulty level: easy, medium, or hard")
    explanation: str = Field(description="Short explanation of the answer")


class QuizGenerationSchema(BaseModel):
    """Schema for complete quiz generation output."""
    quiz: List[QuizQuestionSchema] = Field(description="List of 5-10 quiz questions")
    related_topics: List[str] = Field(description="3-5 related Wikipedia topics")


class LLMQuizGenerator:
    """
    Generates quizzes from Wikipedia article content using Google Gemini LLM.
    """
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY", "")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        # Initialize Gemini model (free tier)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=self.api_key,
            temperature=0.7,
            max_tokens=2048
        )
        
        # Setup parser
        self.parser = PydanticOutputParser(pydantic_object=QuizGenerationSchema)
        
        # Quiz generation prompt template
        self.quiz_prompt = PromptTemplate(
            template="""You are an expert quiz creator. Based on the Wikipedia article provided, create a comprehensive and educational quiz.

ARTICLE TITLE: {title}

ARTICLE SUMMARY: {summary}

ARTICLE SECTIONS: {sections}

FULL ARTICLE CONTENT:
{content}

INSTRUCTIONS:
1. Generate 7-10 high-quality multiple-choice questions based STRICTLY on the article content
2. Questions should:
   - Be factually accurate and directly answerable from the article
   - Cover different sections and aspects of the topic
   - Have varying difficulty levels (easy, medium, hard)
   - Be clear and unambiguous
3. Each question must have:
   - Four distinct options (A-D)
   - One correct answer
   - A brief explanation citing where in the article the answer can be found
4. Difficulty levels:
   - Easy: Basic facts, dates, simple definitions
   - Medium: Requires understanding connections between concepts
   - Hard: Deep comprehension, analysis, or inference
5. NO HALLUCINATION: Only use information explicitly stated in the article
6. Also suggest 3-5 related Wikipedia topics for further reading (topics that would logically connect to this article)

{format_instructions}

Generate the quiz now:""",
            input_variables=["title", "summary", "sections", "content"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
    
    def generate_quiz(
        self,
        title: str,
        summary: str,
        content: str,
        sections: List[str]
    ) -> Dict:
        """
        Generate quiz questions and related topics using LLM.
        
        Args:
            title: Article title
            summary: Article summary
            content: Full article text
            sections: List of section titles
            
        Returns:
            Dictionary containing quiz questions and related topics
        """
        try:
            # Format sections as a readable list
            sections_text = ", ".join(sections) if sections else "No sections"
            
            # Generate the prompt
            prompt = self.quiz_prompt.format(
                title=title,
                summary=summary,
                sections=sections_text,
                content=content
            )
            
            # Get LLM response
            response = self.llm.invoke(prompt)
            
            # Parse response
            try:
                parsed_output = self.parser.parse(response.content)
                return {
                    'quiz': [q.dict() for q in parsed_output.quiz],
                    'related_topics': parsed_output.related_topics
                }
            except Exception as parse_error:
                # Fallback parsing if structured output fails
                print(f"Parsing error: {parse_error}")
                return self._fallback_parse(response.content, title)
                
        except Exception as e:
            print(f"Error generating quiz: {e}")
            # Return a minimal valid response
            return {
                'quiz': self._generate_fallback_quiz(title, summary),
                'related_topics': self._generate_fallback_topics(title)
            }
    
    def _fallback_parse(self, response_text: str, title: str) -> Dict:
        """Attempt to extract quiz data from unstructured response."""
        try:
            # Try to find JSON in the response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                if 'quiz' in data and 'related_topics' in data:
                    return data
        except:
            pass
        
        # If all else fails, return minimal quiz
        return {
            'quiz': self._generate_fallback_quiz(title, "Generated from article"),
            'related_topics': self._generate_fallback_topics(title)
        }
    
    def _generate_fallback_quiz(self, title: str, summary: str) -> List[Dict]:
        """Generate a basic fallback quiz if LLM fails."""
        return [
            {
                "question": f"What is the main topic of this article?",
                "options": [title, "Unknown Topic", "General Knowledge", "History"],
                "answer": title,
                "difficulty": "easy",
                "explanation": "The article title indicates the main topic."
            },
            {
                "question": "This article provides information about:",
                "options": [
                    f"{title} and related concepts",
                    "Unrelated topics",
                    "Generic information",
                    "Abstract concepts"
                ],
                "answer": f"{title} and related concepts",
                "difficulty": "easy",
                "explanation": "Based on the article summary."
            }
        ]
    
    def _generate_fallback_topics(self, title: str) -> List[str]:
        """Generate basic related topics if LLM fails."""
        return [f"{title} - Overview", "Related Concepts", "Historical Context"]
