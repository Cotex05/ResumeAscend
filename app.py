"""
AI Resume Screening Tool - Main Application
Clean, modular architecture with environment variable support
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from config import Config
from core.session_manager import SessionManager
from core.error_handler import ErrorHandler
from utils import (
    extract_text_from_file,
    ATSAnalyzer, 
    GroqResumeAnalyzer,
    create_score_chart,
    create_category_breakdown
)

# Configure page
st.set_page_config(
    page_title=Config.APP_TITLE,
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

def init_app():
    """Initialize application"""
    # Initialize session state
    SessionManager.init_session_state()
    
    # Validate environment
    if not ErrorHandler.validate_environment():
        st.stop()

def upload_section():
    """File upload section"""
    with st.sidebar:
        st.header("📎 Upload Resume")
        uploaded_file = st.file_uploader(
            "Choose your resume file",
            type=Config.SUPPORTED_FILE_TYPES,
            help=f"Supported formats: {', '.join(Config.SUPPORTED_FILE_TYPES).upper()}"
        )
        
        if uploaded_file:
            # Validate file size
            if uploaded_file.size > Config.MAX_FILE_SIZE_MB * 1024 * 1024:
                st.error(f"File too large. Maximum size: {Config.MAX_FILE_SIZE_MB}MB")
                return None
                
            return uploaded_file
    return None

def analyze_resume(uploaded_file):
    """Analyze uploaded resume"""
    if st.button("🔍 Analyze Resume", type="primary", use_container_width=True):
        with st.spinner("Analyzing your resume..."):
            # Extract text
            resume_text = ErrorHandler.safe_execute(
                lambda: extract_text_from_file(uploaded_file),
                "Failed to extract text from file"
            )
            
            if not resume_text:
                return
            
            # Store resume text
            SessionManager.set('resume_text', resume_text)
            
            # Perform ATS analysis
            ats_analyzer = ATSAnalyzer()
            results = ErrorHandler.safe_execute(
                lambda: ats_analyzer.analyze_resume(resume_text),
                "ATS analysis failed"
            )
            
            if not results:
                return
            
            # AI-powered analysis
            try:
                groq_analyzer = GroqResumeAnalyzer()
                
                # Extract personal details
                personal_details = ErrorHandler.safe_execute(
                    lambda: groq_analyzer.extract_personal_details(resume_text),
                    "Personal details extraction failed"
                )
                
                # Generate AI summary
                ai_analysis = ErrorHandler.safe_execute(
                    lambda: groq_analyzer.generate_ai_summary_and_suggestions(resume_text, results['overall_score']),
                    "AI summary generation failed"
                )
                
                # Generate dynamic recommendations
                dynamic_recommendations = ErrorHandler.safe_execute(
                    lambda: groq_analyzer.generate_dynamic_recommendations(resume_text, results['category_scores']),
                    "Dynamic recommendations generation failed"
                )
                
            except Exception as e:
                ErrorHandler.handle_api_error(e, "AI analysis")
                return
            
            # Store results
            SessionManager.set('analysis_results', results)
            SessionManager.set('personal_details', personal_details)
            SessionManager.set('ai_analysis', ai_analysis)
            SessionManager.set('dynamic_recommendations', dynamic_recommendations)
            SessionManager.set('analysis_complete', True)
            
            st.success("✅ Analysis completed successfully!")
            st.rerun()

def display_results():
    """Display analysis results"""
    results = SessionManager.get('analysis_results')
    personal_details = SessionManager.get('personal_details')
    ai_analysis = SessionManager.get('ai_analysis')
    dynamic_recommendations = SessionManager.get('dynamic_recommendations')
    
    # Header section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📊 ATS Analysis Results")
        if personal_details:
            st.markdown(f"""
            **👤 Candidate:** {personal_details.get('name', 'Not specified')}  
            **📧 Email:** {personal_details.get('email', 'Not specified')}  
            **📱 Phone:** {personal_details.get('phone', 'Not specified')}  
            **🏢 Company:** {personal_details.get('current_company', 'Not specified')}  
            **💼 Role:** {personal_details.get('job_role', 'Not specified')}  
            **🎓 Education:** {personal_details.get('last_education', 'Not specified')}
            """)
    
    with col2:
        if st.button("🔄 New Analysis", use_container_width=True):
            SessionManager.reset_analysis()
            st.rerun()
    
    # Overall score visualization
    st.plotly_chart(
        create_score_chart(results['overall_score']), 
        use_container_width=True
    )
    
    # Category breakdown
    st.subheader("📈 Category Breakdown")
    st.plotly_chart(
        create_category_breakdown(results['category_scores']), 
        use_container_width=True
    )
    
    # AI Analysis sections
    if ai_analysis:
        st.subheader("🤖 AI Professional Summary")
        st.info(ai_analysis.get('professional_summary', 'No summary available'))
    
    # Dynamic recommendations
    if dynamic_recommendations:
        st.subheader("🎯 AI-Generated Recommendations")
        
        # Display recommendations
        recommendations = dynamic_recommendations.get('recommendations', [])
        for i, rec in enumerate(recommendations, 1):
            with st.expander(f"Recommendation {i}: {rec.get('category', 'General')}", expanded=True):
                st.write(f"**Issue:** {rec.get('issue', 'N/A')}")
                st.write(f"**Impact:** {rec.get('impact', 'N/A')}")
                st.write(f"**Recommendation:** {rec.get('recommendation', 'N/A')}")
        
        # Display strengths
        strengths = dynamic_recommendations.get('strengths', [])
        if strengths:
            st.subheader("✅ Resume Strengths")
            for strength in strengths:
                st.success(f"✓ {strength}")
    
    # Detailed analysis button
    if st.button("🔍 Show Detailed Analysis"):
        SessionManager.set('show_detailed_analysis', True)
        st.rerun()

def display_detailed_analysis():
    """Display detailed weak points analysis"""
    st.header("🔍 Detailed Analysis")
    
    resume_text = SessionManager.get('resume_text', '')
    category_scores = SessionManager.get('analysis_results', {}).get('category_scores', {})
    
    try:
        groq_analyzer = GroqResumeAnalyzer()
        detailed_analysis = groq_analyzer.generate_dynamic_detailed_analysis(resume_text, category_scores)
        
        # Weak points
        weak_points = detailed_analysis.get('weak_points', [])
        if weak_points:
            st.subheader("⚠️ Areas for Improvement")
            for point in weak_points:
                with st.expander(f"{point.get('title', 'Issue')}", expanded=True):
                    st.write(f"**Current Issue:** {point.get('current_issue', 'N/A')}")
                    st.write(f"**Impact:** {point.get('impact', 'N/A')}")
                    st.write(f"**Suggestion:** {point.get('enhanced_suggestion', 'N/A')}")
        
        # Enhancements
        enhancements = detailed_analysis.get('enhancements', [])
        if enhancements:
            st.subheader("🔧 Specific Enhancements")
            for enhancement in enhancements:
                with st.expander(f"Enhancement: {enhancement.get('category', 'General')}", expanded=False):
                    st.write(f"**Before:** {enhancement.get('before', 'N/A')}")
                    st.write(f"**After:** {enhancement.get('after', 'N/A')}")
                    st.write(f"**Why:** {enhancement.get('explanation', 'N/A')}")
                    
    except Exception as e:
        ErrorHandler.handle_api_error(e, "Detailed analysis")
    
    if st.button("⬅️ Back to Overview"):
        SessionManager.set('show_detailed_analysis', False)
        st.rerun()

def main():
    """Main application flow"""
    init_app()
    
    # Header
    st.title(f"🤖 {Config.APP_TITLE}")
    st.markdown(Config.APP_DESCRIPTION)
    
    # File upload
    uploaded_file = upload_section()
    
    # Analysis flow
    if uploaded_file and not SessionManager.get('analysis_complete'):
        analyze_resume(uploaded_file)
    
    # Display results
    if SessionManager.get('analysis_complete'):
        if SessionManager.get('show_detailed_analysis'):
            display_detailed_analysis()
        else:
            display_results()
    
    # Footer
    st.markdown("---")
    st.markdown("*Powered by Groq Cloud AI and built with Streamlit*")

if __name__ == "__main__":
    main()