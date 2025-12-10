import pytest
from fastapi.testclient import TestClient
from main import app
from datetime import datetime

client = TestClient(app)


def test_summary_with_more_than_10_words():
    """
    Test that the endpoint returns exactly 10 words in summary 
    when the input has more than 10 words.
    """
    # Create text with more than 10 words
    text = "one two three four five six seven eight nine ten eleven twelve thirteen"
    
    response = client.post("/summaries", json={"text": text})
    
    assert response.status_code == 200
    data = response.json()
    
    # Check that summary exists
    assert "summary" in data
    
    # Check that summary contains exactly 10 words
    summary_words = data["summary"].split()
    assert len(summary_words) == 10
    
    # Verify it's the first 10 words
    expected_words = text.split()[:10]
    assert summary_words == expected_words


def test_summary_with_less_than_10_words():
    """
    Test that the endpoint handles text with fewer than 10 words.
    """
    text = "one two three"
    
    response = client.post("/summaries", json={"text": text})
    
    assert response.status_code == 200
    data = response.json()
    
    assert "summary" in data
    summary_words = data["summary"].split()
    assert len(summary_words) == 3
    assert data["summary"] == text


def test_timestamp_field_present():
    """
    Test that a timestamp field is present in the response.
    """
    text = "This is a test text with multiple words to check the timestamp"
    
    response = client.post("/summaries", json={"text": text})
    
    assert response.status_code == 200
    data = response.json()
    
    # Check that timestamp field exists
    assert "timestamp" in data
    
    # Check that timestamp is a valid ISO format string
    timestamp = data["timestamp"]
    assert isinstance(timestamp, str)
    
    # Try to parse it as ISO format datetime
    try:
        datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    except ValueError:
        pytest.fail(f"Timestamp '{timestamp}' is not in valid ISO format")


def test_summary_with_exactly_10_words():
    """
    Test that the endpoint handles text with exactly 10 words.
    """
    text = "one two three four five six seven eight nine ten"
    
    response = client.post("/summaries", json={"text": text})
    
    assert response.status_code == 200
    data = response.json()
    
    summary_words = data["summary"].split()
    assert len(summary_words) == 10
    assert data["summary"] == text


def test_summary_with_empty_text():
    """
    Test that the endpoint handles empty text.
    """
    text = ""
    
    response = client.post("/summaries", json={"text": text})
    
    assert response.status_code == 200
    data = response.json()
    
    assert "summary" in data
    assert data["summary"] == ""
    assert "timestamp" in data

