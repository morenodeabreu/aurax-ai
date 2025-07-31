"""
AURAX Sprint 4 - Load Testing with Locust
Comprehensive load testing scenarios for AURAX backend API
"""

import json
import random
from locust import HttpUser, task, between
from typing import Dict, Any, List


class AuraxLoadTestUser(HttpUser):
    """
    Simulates realistic user behavior for AURAX API load testing
    """
    
    # Wait time between requests (1-3 seconds)
    wait_time = between(1, 3)
    
    # Base URL configuration
    host = "http://localhost:8000"
    
    def on_start(self):
        """Initialize test user - check system health"""
        with self.client.get("/health", catch_response=True) as response:
            if response.status_code != 200:
                response.failure("Health check failed")
                
    @task(5)  # High frequency task - 50% of requests
    def test_generate_text(self):
        """Test text generation endpoint with various prompts"""
        
        text_prompts = [
            "Explain quantum computing in simple terms",
            "What are the benefits of renewable energy?",
            "How does machine learning work?",
            "Describe the process of photosynthesis",
            "What is the history of artificial intelligence?",
            "Explain blockchain technology",
            "How do vaccines work in the human body?",
            "What are the main causes of climate change?",
        ]
        
        payload = {
            "prompt": random.choice(text_prompts),
            "max_tokens": random.randint(500, 1500),
            "context_threshold": round(random.uniform(0.3, 0.8), 2)
        }
        
        with self.client.post(
            "/generate",
            json=payload,
            headers={"Content-Type": "application/json"},
            catch_response=True,
            name="generate_text"
        ) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if not result.get("success", False):
                        response.failure(f"Generation failed: {result.get('error', 'Unknown error')}")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"HTTP {response.status_code}")
    
    @task(3)  # Medium frequency task - 30% of requests
    def test_generate_code(self):
        """Test code generation with programming prompts"""
        
        code_prompts = [
            "Write a Python function to sort a list of dictionaries by a key",
            "Create a JavaScript function to validate email addresses",
            "Implement a binary search algorithm in Python",
            "Write a SQL query to find duplicate records",
            "Create a REST API endpoint in FastAPI",
            "Write a React component for user authentication",
            "Implement a simple caching mechanism in Python",
            "Create a function to calculate fibonacci numbers",
        ]
        
        payload = {
            "prompt": random.choice(code_prompts),
            "model": "qwen3:coder",
            "max_tokens": random.randint(800, 2000),
            "context_threshold": 0.3,
            "routing_metadata": {"preferred_model": "code"}
        }
        
        with self.client.post(
            "/generate",
            json=payload,
            headers={"Content-Type": "application/json"},
            catch_response=True,
            name="generate_code"
        ) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if not result.get("success", False):
                        response.failure(f"Code generation failed: {result.get('error', 'Unknown error')}")
                    elif result.get("response_type") != "code":
                        response.failure("Expected code response type")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"HTTP {response.status_code}")
    
    @task(1)  # Low frequency task - 10% of requests
    def test_generate_image(self):
        """Test image generation requests"""
        
        image_prompts = [
            "A beautiful sunset over mountains",
            "A futuristic cityscape with flying cars",
            "A peaceful forest with a small stream",
            "An abstract painting with vibrant colors",
            "A modern office workspace",
            "A vintage car on a country road",
            "A space station orbiting Earth",
            "A cozy library with old books",
        ]
        
        payload = {
            "prompt": f"Create an image of: {random.choice(image_prompts)}",
            "routing_metadata": {"preferred_model": "image"}
        }
        
        with self.client.post(
            "/generate",
            json=payload,
            headers={"Content-Type": "application/json"},
            catch_response=True,
            name="generate_image"
        ) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if not result.get("success", False):
                        response.failure(f"Image generation failed: {result.get('error', 'Unknown error')}")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"HTTP {response.status_code}")
    
    @task(1)  # Low frequency task - 10% of requests  
    def test_model_routing(self):
        """Test model routing endpoint"""
        
        test_queries = [
            "Write a Python function",
            "Create an image of a cat",
            "Explain machine learning",
            "Debug this JavaScript code",
            "Generate a landscape photo",
            "What is quantum physics?",
        ]
        
        payload = {
            "query": random.choice(test_queries),
            "metadata": {"test": True}
        }
        
        with self.client.post(
            "/route",
            json=payload,
            headers={"Content-Type": "application/json"},
            catch_response=True,
            name="test_routing"
        ) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if not result.get("success", False):
                        response.failure("Routing test failed")
                    elif "routing" not in result:
                        response.failure("Missing routing information")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"HTTP {response.status_code}")
    
    @task(1)  # System monitoring task
    def test_system_status(self):
        """Test system status endpoint"""
        
        with self.client.get(
            "/system/status",
            catch_response=True,
            name="system_status"
        ) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if not result.get("success", False):
                        response.failure("System status check failed")
                    elif "components" not in result:
                        response.failure("Missing components information")
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"HTTP {response.status_code}")
    
    # Uncomment this if you want to test scraping endpoints
    # @task(1) 
    # def test_web_scraping(self):
    #     """Test web scraping functionality"""
    #     
    #     test_urls = [
    #         "https://example.com",
    #         "https://httpbin.org/html",
    #         "https://jsonplaceholder.typicode.com",
    #     ]
    #     
    #     payload = {
    #         "url": random.choice(test_urls),
    #         "metadata": {"test_scraping": True}
    #     }
    #     
    #     with self.client.post(
    #         "/scrape",
    #         json=payload,
    #         headers={"Content-Type": "application/json"},
    #         catch_response=True,
    #         name="test_scraping"
    #     ) as response:
    #         if response.status_code == 200:
    #             try:
    #                 result = response.json()
    #                 if not result.get("success", False):
    #                     response.failure(f"Scraping failed: {result.get('error', 'Unknown error')}")
    #             except json.JSONDecodeError:
    #                 response.failure("Invalid JSON response")
    #         else:
    #             response.failure(f"HTTP {response.status_code}")


class AuraxBurstUser(AuraxLoadTestUser):
    """
    Heavy load user for burst testing scenarios
    Simulates periods of high activity
    """
    
    wait_time = between(0.1, 0.5)  # Much faster requests
    
    @task(10)
    def burst_generate_requests(self):
        """Generate burst of requests to test scaling"""
        
        simple_prompts = [
            "Hello",
            "Test",
            "Quick response",
            "Fast query",
            "Simple question",
        ]
        
        payload = {
            "prompt": random.choice(simple_prompts),
            "max_tokens": 100,
            "context_threshold": 0.5
        }
        
        with self.client.post(
            "/generate",
            json=payload,
            headers={"Content-Type": "application/json"},
            catch_response=True,
            name="burst_request"
        ) as response:
            if response.status_code != 200:
                response.failure(f"HTTP {response.status_code}")


# Custom test scenarios for different load patterns
class AuraxPeakHourUser(AuraxLoadTestUser):
    """Simulates peak hour usage patterns"""
    
    wait_time = between(0.5, 2)
    
    @task(8)
    def peak_generate_text(self):
        self.test_generate_text()
    
    @task(2)
    def peak_generate_code(self):
        self.test_generate_code()


# Example usage:
# Run with: locust -f locustfile.py --host=http://localhost:8000
# Web UI: http://localhost:8089
# 
# Command line examples:
# locust -f locustfile.py --host=http://localhost:8000 --users 10 --spawn-rate 2 --run-time 60s --headless
# locust -f locustfile.py --host=http://localhost:8000 --users 50 --spawn-rate 5 --run-time 300s --html=report.html