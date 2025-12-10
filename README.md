# Virtual Sapiens Demo Project

A professional FastAPI application with a TypeScript client for extracting the first 10 words from text input with timestamp tracking.

## Project Structure

```
.
├── main.py              # FastAPI application with /summaries endpoint
├── middleware.py        # Custom logging middleware
├── test_main.py         # Pytest tests
├── summaryClient.ts     # TypeScript client for the API
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Features

### Backend (FastAPI)
- **POST /summaries** endpoint that:
  - Accepts text input
  - Returns the first 10 words (or fewer) as a summary
  - Includes UTC timestamp
- Custom middleware that logs:
  - Request path
  - Execution time
  - Status code

### Frontend (TypeScript)
- TypeScript client with proper typing
- Computes word count on the client side
- Error handling for non-2xx responses

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Node.js and npm (optional, for TypeScript compilation if needed)

## Installation

### Backend Setup

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - **Windows (PowerShell):**
     ```powershell
     venv\Scripts\Activate.ps1
     ```
     If you get an execution policy error, run:
     ```powershell
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
     ```
   - **Windows (Command Prompt):**
     ```cmd
     venv\Scripts\activate.bat
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Frontend Setup (TypeScript)

The TypeScript client (`summaryClient.ts`) can be used directly in:
- Node.js projects (with TypeScript support)
- Browser environments (with a bundler like webpack, vite, etc.)
- Deno
- Any TypeScript-compatible environment

If you need to compile TypeScript, install TypeScript globally:
```bash
npm install -g typescript
```

Or add it to your project:
```bash
npm init -y
npm install --save-dev typescript @types/node
```

## Running the Server

Start the FastAPI development server:

```bash
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`

### API Documentation

Once the server is running, you can access:
- **Interactive API docs (Swagger UI):** http://localhost:8000/docs
- **Alternative API docs (ReDoc):** http://localhost:8000/redoc

## Testing

### Backend Tests

**Important:** Make sure your virtual environment is activated before running tests.

Run the pytest test suite:

**Bash/Linux/macOS:**
```bash
pytest test_main.py -v
```

**PowerShell (Windows):**
```powershell
python -m pytest test_main.py -v
```

For more detailed output:

**Bash/Linux/macOS:**
```bash
pytest test_main.py -v --tb=short
```

**PowerShell (Windows):**
```powershell
python -m pytest test_main.py -v --tb=short
```

**Note:** If you get a "pytest is not recognized" error in PowerShell, either:
- Activate your virtual environment first: `venv\Scripts\Activate.ps1`
- Or use: `python -m pytest` instead of just `pytest`

### Manual API Testing

You can test the endpoint using curl (bash/Git Bash):

```bash
curl -X POST "http://localhost:8000/summaries" \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a sample text with more than ten words to test the summary endpoint functionality"}'
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/summaries" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"text": "This is a sample text with more than ten words to test the summary endpoint functionality"}'
```

**Or using Invoke-WebRequest:**
```powershell
$body = @{
    text = "This is a sample text with more than ten words to test the summary endpoint functionality"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/summaries" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body | Select-Object -ExpandProperty Content
```

Expected response:
```json
{
  "summary": "This is a sample text with more than ten words",
  "timestamp": "2024-01-01T12:00:00.000000+00:00"
}
```

### TypeScript Client Usage

Example usage of the TypeScript client:

```typescript
import { createSummary, SummaryRequest } from './summaryClient';

async function example() {
  const payload: SummaryRequest = {
    text: "This is a sample text with more than ten words to test the summary endpoint functionality"
  };

  try {
    const result = await createSummary("http://localhost:8000", payload);
    console.log(`Summary: ${result.summary}`);
    console.log(`Word Count: ${result.wordCount}`);
    console.log(`Timestamp: ${result.timestamp}`);
  } catch (error) {
    console.error('Error:', error.message);
  }
}

example();
```

## API Endpoint

### POST /summaries

**Request Body:**
```json
{
  "text": "string"
}
```

**Response:**
```json
{
  "summary": "string",
  "timestamp": "string"
}
```

**Description:**
- Splits the input text by whitespace
- Returns the first 10 words (or fewer if the text has less than 10 words)
- Includes a UTC timestamp in ISO format

## Development

### Running with Auto-reload

The server runs with `--reload` flag by default, which automatically restarts when code changes are detected.

### Viewing Logs

The custom middleware logs each request to the console with:
- Request path
- Execution time (in seconds)
- Status code

Example log output:
```
INFO:__main__:Path: /summaries | Execution Time: 0.0012s | Status Code: 200
```

## License

This is a demo project for Virtual Sapiens.

