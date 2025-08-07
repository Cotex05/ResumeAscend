"""
Error handling utilities for the application
"""
import streamlit as st
import traceback
from typing import Optional, Callable, Any

class ErrorHandler:
    """Centralized error handling"""
    
    @staticmethod
    def handle_api_error(error: Exception, context: str = "API operation") -> None:
        """Handle API-related errors"""
        if "API key" in str(error) or "authentication" in str(error).lower():
            st.error("🔑 API Key Error: Please check your GROQ_API_KEY environment variable")
            st.info("Make sure you have set a valid Groq API key in your environment variables")
        else:
            st.error(f"❌ {context} failed: {str(error)}")
    
    @staticmethod
    def handle_file_error(error: Exception, filename: str = "") -> None:
        """Handle file processing errors"""
        st.error(f"📄 File processing error for {filename}: {str(error)}")
        st.info("Please ensure the file is a valid PDF or DOCX document and try again")
    
    @staticmethod
    def safe_execute(func: Callable, error_message: str = "Operation failed", 
                    show_traceback: bool = False) -> Optional[Any]:
        """Safely execute a function with error handling"""
        try:
            return func()
        except Exception as e:
            st.error(f"❌ {error_message}: {str(e)}")
            if show_traceback:
                st.code(traceback.format_exc())
            return None
    
    @staticmethod
    def validate_environment() -> bool:
        """Validate required environment variables"""
        from config import Config
        
        if not Config.validate_config():
            st.error("🔧 Configuration Error")
            st.info("Please set the GROQ_API_KEY environment variable")
            return False
        return True