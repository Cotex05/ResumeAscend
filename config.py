"""
Configuration module for AI Resume Screening Tool
Handles environment variables and application settings
"""
import os
import logging
from typing import Optional

# Suppress Streamlit file watcher and transformers inspection warnings
logging.getLogger("streamlit.watcher.local_sources_watcher").setLevel(logging.ERROR)
try:
    import transformers.utils.logging as tf_logging
    tf_logging.set_verbosity_error()
except Exception:
    pass

class Config:
    """Application configuration class"""
    
    # API Configuration
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    
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
        return bool(os.getenv("GROQ_API_KEY") or cls.GROQ_API_KEY)
    
    @classmethod
    def get_groq_api_key(cls) -> str:
        """Get Groq API key with validation"""
        api_key = os.getenv("GROQ_API_KEY") or cls.GROQ_API_KEY
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
        return api_key