/**
 * AURAX Frontend - Backend API Client
 * Handles all communication with the FastAPI backend
 */

/* eslint-disable @typescript-eslint/no-explicit-any */

import {
  GenerateRequest,
  GenerateResponse,
  ScrapeRequest,
  ScrapeResponse,
  BatchScrapeRequest,
  RouteRequest,
  RouteResponse,
  SystemStatusResponse,
  HealthResponse,
} from '@/types/api';

// Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Error handling utility
class APIErrorHandler extends Error {
  status: number;
  details?: unknown;

  constructor(message: string, status: number, details?: unknown) {
    super(message);
    this.name = 'APIError';
    this.status = status;
    this.details = details;
  }
}

// Generic API request handler
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const defaultHeaders = {
    'Content-Type': 'application/json',
  };

  const config: RequestInit = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  };

  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
      let errorDetails = null;
      
      try {
        errorDetails = await response.json();
        errorMessage = errorDetails.detail || errorMessage;
      } catch {
        // If response is not JSON, use the status text
      }
      
      throw new APIErrorHandler(errorMessage, response.status, errorDetails);
    }
    
    const data = await response.json();
    return data as T;
  } catch (error) {
    if (error instanceof APIErrorHandler) {
      throw error;
    }
    
    // Network or other errors
    throw new APIErrorHandler(
      `Network error: ${error instanceof Error ? error.message : 'Unknown error'}`,
      0,
      error
    );
  }
}

// API Client Class
export class AuraxAPIClient {
  
  /**
   * Health check endpoint
   */
  static async healthCheck(): Promise<HealthResponse> {
    return apiRequest<HealthResponse>('/health');
  }

  /**
   * Generate text/code/image using multi-model system
   */
  static async generateText(request: GenerateRequest): Promise<GenerateResponse> {
    return apiRequest<GenerateResponse>('/generate', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * Test model routing for a query
   */
  static async routeQuery(request: RouteRequest): Promise<RouteResponse> {
    return apiRequest<RouteResponse>('/route', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * Get comprehensive system status
   */
  static async getSystemStatus(): Promise<SystemStatusResponse> {
    return apiRequest<SystemStatusResponse>('/system/status');
  }

  /**
   * Scrape a single URL and add to knowledge base
   */
  static async scrapeUrl(request: ScrapeRequest): Promise<ScrapeResponse> {
    return apiRequest<ScrapeResponse>('/scrape', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * Scrape multiple URLs in batch
   */
  static async scrapeBatch(request: BatchScrapeRequest): Promise<ScrapeResponse[]> {
    return apiRequest<ScrapeResponse[]>('/scrape/batch', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * Get scraping statistics
   */
  static async getScrapingStats(): Promise<unknown> {
    return apiRequest<unknown>('/scrape/stats');
  }

  /**
   * Add documents to knowledge base
   */
  static async addKnowledge(documents: Array<{ text: string; [key: string]: unknown }>): Promise<unknown> {
    return apiRequest<any>('/knowledge/add', {
      method: 'POST',
      body: JSON.stringify(documents),
    });
  }

  /**
   * Get RAG knowledge base info (legacy endpoint)
   */
  static async getRagInfo(): Promise<unknown> {
    return apiRequest<unknown>('/rag/info');
  }
}

// Convenience functions for easier usage
export const api = {
  health: AuraxAPIClient.healthCheck,
  generate: AuraxAPIClient.generateText,
  route: AuraxAPIClient.routeQuery,
  status: AuraxAPIClient.getSystemStatus,
  scrape: AuraxAPIClient.scrapeUrl,
  scrapeBatch: AuraxAPIClient.scrapeBatch,
  scrapeStats: AuraxAPIClient.getScrapingStats,
  addKnowledge: AuraxAPIClient.addKnowledge,
  ragInfo: AuraxAPIClient.getRagInfo,
};

export default api;

// Export error type for handling
export { APIErrorHandler as APIError };