# LangChain Prompt Templates Used in Wiki Quiz Generator

## Quiz Generation Prompt

This is the main prompt template used to generate quiz questions from Wikipedia articles using Google Gemini LLM.

### Template Structure

```python
template = """You are an expert quiz creator. Based on the Wikipedia article provided, create a comprehensive and educational quiz.

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

Generate the quiz now:"""
```

### Input Variables

- **title**: The title of the Wikipedia article
- **summary**: A brief summary (first paragraph) of the article
- **sections**: A comma-separated list of main section headings from the article
- **content**: The full text content of the article (limited to ~8000 characters)
- **format_instructions**: Pydantic schema instructions for structured output

### Output Schema

The LLM is instructed to return a structured JSON response following this Pydantic schema:

```python
class QuizQuestionSchema(BaseModel):
    question: str  # The quiz question text
    options: List[str]  # Four answer options
    answer: str  # The correct answer
    difficulty: str  # "easy", "medium", or "hard"
    explanation: str  # Short explanation of the answer

class QuizGenerationSchema(BaseModel):
    quiz: List[QuizQuestionSchema]  # 5-10 quiz questions
    related_topics: List[str]  # 3-5 related Wikipedia topics
```

## Key Design Decisions

### 1. Grounding in Article Content

The prompt explicitly instructs the LLM to:
- Only use information **explicitly stated** in the article
- Include explanations that **cite specific sections**
- Avoid hallucination by emphasizing "NO HALLUCINATION: Only use information explicitly stated in the article"

This ensures quiz questions are factually accurate and verifiable against the source material.

### 2. Difficulty Stratification

Questions are categorized into three levels:
- **Easy**: Basic recall (dates, names, simple facts)
- **Medium**: Conceptual understanding (connections, relationships)
- **Hard**: Deep analysis (implications, complex reasoning)

This provides a balanced quiz that tests different cognitive levels.

### 3. Comprehensive Coverage

By providing:
- Article summary (context)
- Section headings (structure)
- Full content (details)

The LLM can generate questions that span the entire article rather than focusing on just the introduction.

### 4. Structured Output

Using Pydantic schemas ensures:
- Consistent JSON format
- Type validation
- Easy integration with the database and frontend

### 5. Related Topics Generation

The prompt asks for related Wikipedia topics, which:
- Encourages further learning
- Provides natural navigation paths
- Enriches the educational experience

## Fallback Mechanisms

The implementation includes fallback parsing for cases where the LLM doesn't return perfectly structured output:

1. **JSON extraction**: Attempts to find and parse JSON within unstructured text
2. **Minimal quiz generation**: Creates basic questions if LLM completely fails
3. **Error handling**: Gracefully degrades rather than crashing

## Temperature and Model Settings

```python
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # Free tier model
    temperature=0.7,  # Balanced creativity and consistency
    max_tokens=2048  # Enough for 10 questions + explanations
)
```

- **Temperature 0.7**: Provides some creativity in question phrasing while maintaining factual accuracy
- **Max tokens 2048**: Sufficient for complete quiz generation
- **Model**: Gemini 1.5 Flash (fast, free, and capable)

## Optimization Tips

1. **Token Management**: Content is limited to ~8000 characters to avoid exceeding context limits
2. **Caching**: Quiz results are stored in database to avoid regenerating for the same URL
3. **Retry Logic**: Implemented in the service layer to handle temporary API failures
4. **Validation**: Pydantic schemas ensure output quality before saving to database

## Example Generated Output

```json
{
  "quiz": [
    {
      "question": "Where did Alan Turing study?",
      "options": [
        "Harvard University",
        "Cambridge University",
        "Oxford University",
        "Princeton University"
      ],
      "answer": "Cambridge University",
      "difficulty": "easy",
      "explanation": "Mentioned in the 'Early life' section as King's College, Cambridge."
    }
  ],
  "related_topics": [
    "Cryptography",
    "Enigma machine",
    "Computer science history"
  ]
}
```

---

**File Location**: `backend/services/llm_service.py`

**LangChain Version**: 0.1.6

**LLM Provider**: Google (Gemini 1.5 Flash via LangChain)
