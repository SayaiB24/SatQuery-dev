import type { AnalyzeResponse } from '../types/satquery';

const API_BASE = 'http://127.0.0.1:8000';

export async function analyzeRaster(
  query: string,
  files: File[] = [],
  sessionOptions?: Record<string, unknown>
): Promise<AnalyzeResponse> {
  const formData = new FormData();
  formData.append('query', query);

  for (const file of files) {
    formData.append('files', file);
  }

  if (sessionOptions) {
    formData.append('session_options', JSON.stringify(sessionOptions));
  }

  const response = await fetch(`${API_BASE}/v1/analyze`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errText = await response.text();
    throw new Error(`API error (${response.status}): ${errText}`);
  }

  return response.json();
}

export async function getSession(sessionId: string): Promise<AnalyzeResponse> {
  const response = await fetch(`${API_BASE}/v1/session/${sessionId}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch session (${response.status})`);
  }
  return response.json();
}

export async function getHealth(): Promise<{ status: string; service: string }> {
  const response = await fetch(`${API_BASE}/v1/health`);
  return response.json();
}

export async function getRegistry(): Promise<unknown> {
  const response = await fetch(`${API_BASE}/v1/registry`);
  return response.json();
}
