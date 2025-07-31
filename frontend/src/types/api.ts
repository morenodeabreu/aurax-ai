/**
 * AURAX Frontend - API Types
 * TypeScript definitions for backend API communication
 */

// Request Types
export interface GenerateRequest {
  prompt: string;
  max_tokens?: number;
  model?: string;
  context_threshold?: number;
  routing_metadata?: Record<string, unknown>;
}

export interface ScrapeRequest {
  url: string;
  metadata?: Record<string, unknown>;
}

export interface BatchScrapeRequest {
  urls: string[];
  metadata?: Record<string, unknown>;
}

export interface RouteRequest {
  query: string;
  metadata?: Record<string, unknown>;
}

// Response Types
export interface GenerateResponse {
  success: boolean;
  query: string;
  context: Array<{
    text: string;
    score: number;
    [key: string]: unknown;
  }>;
  response: unknown; // Can be text, image data, etc.
  response_type?: 'text' | 'code' | 'image' | 'error';
  metadata?: {
    context_docs_count?: number;
    model_used?: string;
    prompt_length?: number;
    routing?: unknown;
  };
  routing_info?: {
    model_type: string;
    confidence: number;
    reasoning?: string;
    suggested_parameters?: Record<string, unknown>;
  };
  error?: string;
}

export interface ScrapeResponse {
  success: boolean;
  url: string;
  title?: string;
  chunks_created?: number;
  chunks_added_to_rag?: number;
  content_length?: number;
  error?: string;
  timestamp?: string;
}

export interface RouteResponse {
  success: boolean;
  query: string;
  routing: {
    model_type: string;
    confidence: number;
    reasoning: string;
    suggested_parameters?: Record<string, unknown>;
  };
}

export interface SystemStatusResponse {
  success: boolean;
  components: {
    llm: {
      available: boolean;
      service: string;
      base_url: string;
      default_model: string;
      available_models: string[];
    };
    rag: {
      available: boolean;
      knowledge_base: {
        total_points?: number;
        indexed_vectors_count?: number;
        collection_name?: string;
        [key: string]: unknown;
      };
    };
  };
  error?: string;
}

export interface HealthResponse {
  status: string;
  version: string;
}

// Message Types for Chat Interface
export interface ChatMessage {
  id: string;
  type: 'user' | 'assistant' | 'system' | 'error';
  content: string;
  timestamp: Date;
  metadata?: unknown;
}

// API Error Type
export interface APIError {
  message: string;
  status: number;
  details?: unknown;
}