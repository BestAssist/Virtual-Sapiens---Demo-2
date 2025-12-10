"""
FastAPI application with /summaries endpoint.

This module provides a POST endpoint that processes text input,
extracts the first 10 words, and returns a summary with timestamp.
"""

from datetime import datetime, timezone
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

from middleware import LoggingMiddleware

app = FastAPI(
    title="Text Summarization API",
    description="API for extracting first 10 words from text with timestamp",
    version="1.0.0",
)

# Add CORS middleware for client integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom logging middleware
app.add_middleware(LoggingMiddleware)


class SummaryRequest(BaseModel):
    """Request model for summary endpoint."""

    text: str = Field(..., min_length=1, description="Text to summarize")

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        """Validate that text is not empty after stripping."""
        if not v.strip():
            raise ValueError("Text cannot be empty or only whitespace")
        return v


class SummaryResponse(BaseModel):
    """Response model for summary endpoint."""

    summary: str = Field(..., description="First 10 words (or fewer) from input text")
    timestamp: str = Field(..., description="UTC timestamp in ISO format")


def extract_words(text: str) -> List[str]:
    """
    Extract words from text by splitting on whitespace.

    Args:
        text: Input text string

    Returns:
        List of words (non-empty strings)
    """
    return [word for word in text.split() if word]


def get_first_n_words(words: List[str], n: int = 10) -> List[str]:
    """
    Get first n words from a list of words.

    Args:
        words: List of words
        n: Number of words to extract (default: 10)

    Returns:
        First n words (or fewer if list is shorter)
    """
    return words[:n]


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Text Summarization API",
        "version": "1.0.0",
    }


@app.get("/health")
async def health():
    """Health check endpoint for monitoring."""
    return {"status": "ok"}


@app.post("/summaries", response_model=SummaryResponse)
async def create_summary(request: SummaryRequest) -> SummaryResponse:
    """
    Create a summary by extracting the first 10 words from input text.

    This endpoint:
    1. Splits the input text into words by whitespace
    2. Takes the first 10 words (or fewer if text has less than 10 words)

    Args:
        request: SummaryRequest containing the text to process

    Returns:
        SummaryResponse with summary and timestamp

    Raises:
        HTTPException: If text processing fails
    """
    try:
        # Split text into words by whitespace
        words = extract_words(request.text)

        # Take first 10 words (or fewer if there aren't 10)
        first_words = get_first_n_words(words, n=10)

        # Join words back into summary string
        summary = " ".join(first_words)

        # Generate UTC timestamp in ISO format
        timestamp = datetime.now(timezone.utc).isoformat()


        return SummaryResponse(
            summary=summary,
            timestamp=timestamp,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing text: {str(e)}",
        )

