"""
Session state management for Streamlit application
"""
import streamlit as st
from typing import Any, Optional

class SessionManager:
    """Manages Streamlit session state"""
    
    @staticmethod
    def init_session_state():
        """Initialize all session state variables"""
        defaults = {
            'analysis_complete': False,
            'analysis_results': None,
            'personal_details': None,
            'ai_analysis': None,
            'ai_strengths_analysis': None,
            'dynamic_recommendations': None,
            'resume_text': None,
            'show_detailed_analysis': False,
            'detailed_analysis': None,
            'rag_chain': None,
            'rag_initialized': False,
            'qa_history': []
        }
        
        for key, default_value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
    
    @staticmethod
    def clear_session():
        """Clear all session state"""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
    
    @staticmethod
    def reset_analysis():
        """Reset only analysis-related session state"""
        reset_keys = [
            'analysis_complete',
            'analysis_results', 
            'personal_details',
            'ai_analysis',
            'ai_strengths_analysis',
            'dynamic_recommendations',
            'resume_text',
            'show_detailed_analysis',
            'detailed_analysis',
            'rag_chain',
            'rag_initialized',
            'qa_history'
        ]
        
        for key in reset_keys:
            if key in st.session_state:
                st.session_state[key] = None if key not in ['analysis_complete', 'show_detailed_analysis', 'rag_initialized', 'qa_history'] else (False if key != 'qa_history' else [])
    
    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """Get session state value safely"""
        return st.session_state.get(key, default)
    
    @staticmethod
    def set(key: str, value: Any):
        """Set session state value"""
        st.session_state[key] = value
