import os
from typing import Dict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import json
import re

load_dotenv()


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
            max_tokens=4096
        )
        
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
2. Questions should cover different sections and have varying difficulty levels (easy, medium, hard)
3. Each question must have four distinct options, one correct answer, and a brief explanation
4. NO HALLUCINATION: Only use information explicitly stated in the article
5. Also suggest 3-5 related Wikipedia topics for further reading

You MUST respond with ONLY valid JSON in exactly this format, no other text:
{{
  "quiz": [
    {{
      "question": "Question text here",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "The correct option text",
      "difficulty": "easy",
      "explanation": "Brief explanation"
    }}
  ],
  "related_topics": ["Topic 1", "Topic 2", "Topic 3"]
}}

Generate the quiz now:""",
            input_variables=["title", "summary", "sections", "content"]
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
            
            # Truncate content to avoid token limits
            max_content_length = 8000
            truncated_content = content[:max_content_length] if len(content) > max_content_length else content
            
            # Generate the prompt
            prompt = self.quiz_prompt.format(
                title=title,
                summary=summary,
                sections=sections_text,
                content=truncated_content
            )
            
            # Get LLM response
            response = self.llm.invoke(prompt)
            
            # Parse JSON from response
            response_text = response.content
            
            # Try to extract JSON from the response
            # Remove markdown code blocks if present
            response_text = re.sub(r'```json\s*', '', response_text)
            response_text = re.sub(r'```\s*', '', response_text)
            response_text = response_text.strip()
            
            # Find JSON object in response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                if 'quiz' in data and 'related_topics' in data:
                    # Validate quiz structure
                    validated_quiz = []
                    for q in data['quiz']:
                        if all(k in q for k in ['question', 'options', 'answer', 'difficulty', 'explanation']):
                            validated_quiz.append({
                                'question': str(q['question']),
                                'options': [str(o) for o in q['options'][:4]],
                                'answer': str(q['answer']),
                                'difficulty': str(q.get('difficulty', 'medium')),
                                'explanation': str(q.get('explanation', ''))
                            })
                    
                    if validated_quiz:
                        return {
                            'quiz': validated_quiz,
                            'related_topics': [str(t) for t in data.get('related_topics', [])]
                        }
            
            # If JSON parsing failed, use fallback
            print(f"Could not parse JSON from LLM response")
            return {
                'quiz': self._generate_fallback_quiz(title, summary),
                'related_topics': self._generate_fallback_topics(title)
            }
                
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
