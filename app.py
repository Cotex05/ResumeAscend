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
from utils.rag_qa import create_resume_rag

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
            SessionManager.set('resume_text', resume_text)
            
            # Initialize RAG pipeline for Q&A
            try:
                rag_chain = create_resume_rag(resume_text, Config.get_groq_api_key())
                if rag_chain:
                    SessionManager.set('rag_chain', rag_chain)
                    SessionManager.set('rag_initialized', True)
                else:
                    st.warning("⚠️ RAG Q&A system could not be initialized. Skipping this feature.")
            except Exception as e:
                print(f"Warning: RAG initialization failed: {e}")
                st.warning("⚠️ RAG Q&A system could not be initialized. Skipping this feature.")
            
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
    
    # RAG-based Q&A section
    if SessionManager.get('rag_initialized'):
        display_resume_qa()
    
    # Detailed analysis button
    if st.button("🔍 Show Detailed Analysis"):
        SessionManager.set('show_detailed_analysis', True)
        st.rerun()

def display_resume_qa():
    """Display resume Q&A interface using RAG"""
    st.subheader("💬 Ask Questions About Your Resume")
    st.markdown("*Ask any questions about your resume and get instant answers based on your resume content*")
    
    # Create columns for input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_question = st.text_input(
            "Ask a question about your resume",
            placeholder="Example: What is my last education? What programming languages do I know?",
            key="resume_qa_input"
        )
    
    with col2:
        ask_button = st.button("🔍 Ask", use_container_width=True)
    
    # Process question
    if ask_button and user_question:
        rag_chain = SessionManager.get('rag_chain')
        
        if rag_chain:
            with st.spinner("Analyzing your resume..."):
                result = rag_chain.query(user_question)
                
                if result:
                    # Display answer
                    st.info(f"**Q:** {user_question}")
                    st.success(f"**A:** {result['answer']}")
                    
                    # Show confidence level
                    confidence = result.get('confidence', 'Low')
                    if confidence == "High":
                        st.caption(f"✅ Confidence: {confidence} (Based on resume content)")
                    else:
                        st.caption(f"⚠️ Confidence: {confidence} (Limited matching content)")
                    
                    # Store in history
                    qa_history = SessionManager.get('qa_history', [])
                    qa_history.append({
                        'question': user_question,
                        'answer': result['answer']
                    })
                    SessionManager.set('qa_history', qa_history)
                else:
                    st.error("Unable to process your question. Please try again.")
        else:
            st.error("RAG system not initialized. Please restart the analysis.")
    
    # Display Q&A history
    qa_history = SessionManager.get('qa_history', [])
    if qa_history:
        with st.expander("📋 Q&A History", expanded=False):
            for i, qa_pair in enumerate(qa_history, 1):
                st.markdown(f"**Q{i}:** {qa_pair['question']}")
                st.markdown(f"**A{i}:** {qa_pair['answer']}")
                st.divider()

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