"""
Security module for the Book RAG System
Provides security utilities and hardening measures
"""
import secrets
import hashlib
from typing import Optional
from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import time
import logging
from .config import settings


security_logger = logging.getLogger(__name__)


class SecurityUtils:
    """Utility class for security-related functions"""

    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """Generate a cryptographically secure random token"""
        return secrets.token_urlsafe(length)

    @staticmethod
    def hash_sensitive_data(data: str, salt: Optional[str] = None) -> str:
        """Hash sensitive data with optional salt"""
        if salt:
            data_to_hash = data + salt
        else:
            data_to_hash = data

        return hashlib.sha256(data_to_hash.encode()).hexdigest()

    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """Validate an API key against known valid keys"""
        # In a real implementation, this would check against a database of valid keys
        # For this implementation, we'll just verify it's not empty and has proper format
        if not api_key:
            return False

        # Basic validation: API key should be at least 20 characters
        if len(api_key) < 20:
            security_logger.warning("Invalid API key length")
            return False

        # Additional checks could be implemented based on your API key format
        return True


class RateLimiter:
    """Simple rate limiter to prevent abuse"""
    def __init__(self, max_requests: int = 100, window_size: int = 3600):  # 100 requests per hour
        self.max_requests = max_requests
        self.window_size = window_size
        self.requests = {}  # ip -> [(timestamp, count), ...]

    def is_allowed(self, identifier: str) -> bool:
        """Check if a request from the identifier is allowed"""
        current_time = time.time()

        # Clean old entries
        if identifier in self.requests:
            self.requests[identifier] = [
                (timestamp, count) for timestamp, count in self.requests[identifier]
                if current_time - timestamp < self.window_size
            ]
        else:
            self.requests[identifier] = []

        # Calculate total requests in the window
        total_requests = sum(count for _, count in self.requests[identifier])

        if total_requests >= self.max_requests:
            security_logger.warning(f"Rate limit exceeded for {identifier}")
            return False

        # Add the current request
        if self.requests[identifier] and self.requests[identifier][-1][0] == int(current_time):
            # Same second, increment count
            self.requests[identifier][-1] = (int(current_time), self.requests[identifier][-1][1] + 1)
        else:
            # New second, add new entry
            self.requests[identifier].append((int(current_time), 1))

        return True


# Initialize rate limiter
rate_limiter = RateLimiter(max_requests=settings.MAX_CONCURRENT_USERS * 2, window_size=3600)


class SecurityMiddleware:
    """Security middleware for the application"""

    @staticmethod
    async def check_rate_limit(request: Request) -> bool:
        """Check if the request is within rate limits"""
        # Get client IP (considering potential proxy headers)
        client_ip = (
            request.headers.get("x-forwarded-for", request.client.host).split(",")[0].strip()
            or request.client.host
        )

        return rate_limiter.is_allowed(client_ip)

    @staticmethod
    async def validate_input(request: Request, data: str, max_length: int = 10000) -> bool:
        """Validate input for common security issues"""
        if len(data) > max_length:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Input too long"
            )

        # Check for potential SQL injection patterns (basic check)
        sql_patterns = ["'", "\"", ";", "--", "/*", "*/", "xp_", "sp_"]
        for pattern in sql_patterns:
            if pattern.lower() in data.lower():
                security_logger.warning(f"Potential SQL injection pattern detected: {pattern}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid input detected"
                )

        # Check for potential XSS patterns (basic check)
        xss_patterns = ["<script", "javascript:", "onerror=", "onload="]
        for pattern in xss_patterns:
            if pattern.lower() in data.lower():
                security_logger.warning(f"Potential XSS pattern detected: {pattern}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid input detected"
                )

        return True

    @staticmethod
    async def sanitize_input(data: str) -> str:
        """Basic input sanitization"""
        # Remove potential harmful characters (be careful not to over-sanitize)
        # For our use case, we mainly want to prevent injection attacks
        # while preserving the meaning of text content
        sanitized = data.replace('\0', '')  # Remove null bytes
        return sanitized


# JWT or other token-based security could be implemented here if needed
# For this implementation, we'll focus on API key validation and rate limiting