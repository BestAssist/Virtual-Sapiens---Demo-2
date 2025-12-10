from fastapi import FastAPI, Request
from datetime import datetime, timezone
from middleware import LoggingMiddleware
from pydantic import BaseModel

app = FastAPI()

# Add custom middleware
app.add_middleware(LoggingMiddleware)


class TextRequest(BaseModel):
    text: str


class SummaryResponse(BaseModel):
    summary: str
    timestamp: str


@app.post("/summaries", response_model=SummaryResponse)
async def create_summary(request: TextRequest):
    """
    Create a summary by taking the first 10 words from the input text.
    """
    # Split text into words by whitespace
    words = request.text.split()
    
    # Take the first 10 words (or fewer if there aren't 10)
    first_10_words = words[:10]
    
    # Join them back into a string
    summary = " ".join(first_10_words)
    
    # Get UTC timestamp
    timestamp = datetime.now(timezone.utc).isoformat()
    
    return SummaryResponse(summary=summary, timestamp=timestamp)

