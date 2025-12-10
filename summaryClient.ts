export interface SummaryRequest {
  text: string;
}

export interface SummaryResponse {
  summary: string;
  timestamp: string;
  wordCount: number;
}

/**
 * Creates a summary by calling the FastAPI /summaries endpoint.
 * 
 * @param baseUrl - The base URL of the API (e.g., "http://localhost:8000")
 * @param payload - The request payload containing the text to summarize
 * @returns A Promise that resolves to a SummaryResponse with summary, timestamp, and wordCount
 * @throws Error if the response status is not 2xx
 */
export async function createSummary(
  baseUrl: string,
  payload: SummaryRequest
): Promise<SummaryResponse> {
  const url = `${baseUrl}/summaries`;
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    // Check if response is not 2xx
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(
        `API request failed with status ${response.status} ${response.statusText}: ${errorText}`
      );
    }

    // Parse the JSON response
    const data = await response.json();
    
    // Compute wordCount from summary
    const wordCount = data.summary.trim() === '' 
      ? 0 
      : data.summary.trim().split(/\s+/).length;

    // Return typed response with computed wordCount
    return {
      summary: data.summary,
      timestamp: data.timestamp,
      wordCount: wordCount,
    };
  } catch (error) {
    // Re-throw if it's already an Error, otherwise wrap it
    if (error instanceof Error) {
      throw error;
    }
    throw new Error(`Failed to create summary: ${String(error)}`);
  }
}

