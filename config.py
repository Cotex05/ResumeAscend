"""
Configuration module for AI Resume Screening Tool
Handles environment variables and application settings
"""
import os
from typing import Optional

class Config:
    """Application configuration class"""
    
    # API Configuration
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    
    # Application Settings
    MAX_FILE_SIZE_MB: int = 10
    SUPPORTED_FILE_TYPES: list = ["pdf", "docx"]
    
    # UI Configuration
    PRIMARY_COLOR: str = "#0A66C2"  # LinkedIn blue
    APP_TITLE: str = "AI Resume Screening Tool"
    APP_DESCRIPTION: str = "Analyze resume compatibility with Applicant Tracking Systems (ATS)"
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate required configuration"""
        if not cls.GROQ_API_KEY:
            return False
        return True
    
    @classmethod
    def get_groq_api_key(cls) -> str:
        """Get Groq API key with validation"""
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY environment variable is required")
        return cls.GROQ_API_KEY