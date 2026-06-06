"""
AI Resume Screening Tool - Main Application
Clean, modular architecture with environment variable support
"""

from html import escape
import os

import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from config import Config
from core.session_manager import SessionManager
from core.error_handler import ErrorHandler
from ui import inject_theme
from utils import (
    extract_text_from_file,
    ATSAnalyzer, 
    GroqResumeAnalyzer,
    create_score_chart,
    create_category_breakdown
)

# Configure page
st.set_page_config(
    page_title="ResumeAscend",
    page_icon="R",
    layout="wide",
    initial_sidebar_state="auto"
)


def safe_text(value, fallback="Not specified"):
    """Return escaped display text for generated or uploaded content."""
    return escape(str(value or fallback))


def render_app_header(status="Resume intelligence"):
    """Render the compact application masthead."""
    st.markdown(
        f"""
        <div class="resume-shell">
            <div class="brand-lockup">
                <div class="brand-seal">R</div>
                <div>
                    <div class="brand-name">ResumeAscend</div>
                    <div class="brand-note">Clarity for every application</div>
                </div>
            </div>
            <div class="shell-status">{safe_text(status)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(eyebrow, title, description=""):
    """Render a consistent editorial section heading."""
    description_html = f"<p>{safe_text(description)}</p>" if description else ""
    st.markdown(
        f"""
        <div class="section-heading">
            <div class="eyebrow">{safe_text(eyebrow)}</div>
            <h2>{safe_text(title)}</h2>
            {description_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def init_app():
    """Initialize application"""
    inject_theme()

    # Initialize session state
    SessionManager.init_session_state()
    
    # Validate environment
    if not ErrorHandler.validate_environment():
        st.stop()

def upload_section():
    """File upload section"""
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="brand-seal">R</div>
                <h2>ResumeAscend</h2>
                <p>Private, focused resume intelligence.</p>
            </div>
            <div class="sidebar-rule"></div>
            <div class="eyebrow">Your document</div>
            """,
            unsafe_allow_html=True,
        )
        uploaded_file = st.file_uploader(
            "Upload resume",
            type=Config.SUPPORTED_FILE_TYPES,
            help=f"Supported formats: {', '.join(Config.SUPPORTED_FILE_TYPES).upper()}",
            label_visibility="collapsed",
        )

        if uploaded_file:
            # Validate file size
            if uploaded_file.size > Config.MAX_FILE_SIZE_MB * 1024 * 1024:
                st.error(f"File too large. Maximum size: {Config.MAX_FILE_SIZE_MB}MB")
                return None

            file_size = uploaded_file.size / (1024 * 1024)
            st.markdown(
                f"""
                <div class="upload-ready">
                    <strong>{safe_text(uploaded_file.name)}</strong>
                    <span>{file_size:.2f} MB · Ready to analyze</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            f"""
            <div class="sidebar-rule"></div>
            <p class="sidebar-note">
                PDF or DOCX · Up to {Config.MAX_FILE_SIZE_MB} MB<br>
                Your file is processed only for this session.
            </p>
            """,
            unsafe_allow_html=True,
        )

        if SessionManager.get('analysis_complete'):
            st.markdown('<div class="sidebar-rule"></div>', unsafe_allow_html=True)
            if st.button("Start a new analysis", width="stretch"):
                SessionManager.reset_analysis()
                st.rerun()

        if uploaded_file:
            return uploaded_file
    return None


def analyze_resume(uploaded_file):
    """Analyze uploaded resume"""
    if st.button("Analyze this resume", type="primary", width="stretch"):
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
                from utils.rag_qa import create_resume_rag

                rag_chain = create_resume_rag(resume_text, Config.get_groq_api_key())
                if rag_chain:
                    SessionManager.set('rag_chain', rag_chain)
                    SessionManager.set('rag_initialized', True)
                else:
                    st.warning("Resume chat could not be initialized. The analysis is still available.")
            except Exception as e:
                print(f"Warning: RAG initialization failed: {e}")
                st.warning("Resume chat could not be initialized. The analysis is still available.")
            
            SessionManager.set('analysis_complete', True)
            
            st.rerun()


def display_landing(uploaded_file):
    """Display the premium landing and analysis entry experience."""
    st.markdown(
        """
        <div class="hero-panel">
            <div class="eyebrow">AI resume intelligence</div>
            <h1>A sharper resume begins with a clearer reading.</h1>
            <p>
                Understand how applicant systems read your resume, uncover the details
                that weaken your story, and leave with precise improvements you can use.
            </p>
        </div>
        <div class="feature-grid">
            <div class="paper-card">
                <span class="card-index">01</span>
                <h3>ATS readiness</h3>
                <p>A measured view of structure, formatting, content, and keyword strength.</p>
            </div>
            <div class="paper-card">
                <span class="card-index">02</span>
                <h3>Editorial guidance</h3>
                <p>Specific recommendations grounded in the resume you actually uploaded.</p>
            </div>
            <div class="paper-card">
                <span class="card-index">03</span>
                <h3>Resume conversation</h3>
                <p>Ask focused questions and keep the full conversation for the session.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_section_header(
        "Begin",
        "One document. A complete reading.",
        "Choose a PDF or DOCX in the left panel. We will prepare the analysis while preserving the original document.",
    )

    action_col, note_col = st.columns([1, 1.35], gap="large")
    with action_col:
        if uploaded_file:
            analyze_resume(uploaded_file)
        else:
            st.button("First upload a resume to continue", disabled=True, width="stretch")

    with note_col:
        if uploaded_file:
            st.markdown(
                f"""
                <div class="upload-ready">
                    <strong>Ready for review</strong>
                    <span>{safe_text(uploaded_file.name)} has been selected.</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="upload-ready">
                    <strong>Your resume stays in this session</strong>
                    <span>Use the upload panel to begin. No account or profile setup is required.</span>
                </div>
                """,
                unsafe_allow_html=True,
            )


def display_results():
    """Display analysis results"""
    results = SessionManager.get('analysis_results')
    personal_details = SessionManager.get('personal_details')
    ai_analysis = SessionManager.get('ai_analysis')
    dynamic_recommendations = SessionManager.get('dynamic_recommendations')
    
    candidate_name = safe_text((personal_details or {}).get('name'), "Your resume")
    role = safe_text((personal_details or {}).get('job_role'), "Professional profile")
    category_scores = results.get('category_scores', {})
    strongest_category = max(category_scores, key=category_scores.get) if category_scores else "Overall"
    strongest_score = category_scores.get(strongest_category, results['overall_score'])

    st.markdown(
        f"""
        <div class="results-hero">
            <div class="eyebrow">Analysis complete</div>
            <h1>{candidate_name}, here is the signal your resume sends.</h1>
            <p>A concise view of ATS readiness, narrative strength, and the highest-value improvements.</p>
        </div>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">ATS score</div>
                <div class="metric-value">{results['overall_score']}</div>
                <div class="metric-detail">out of 100</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Strongest area</div>
                <div class="metric-value">{strongest_score}</div>
                <div class="metric-detail">{safe_text(strongest_category.replace('_', ' ').title())}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Opportunities</div>
                <div class="metric-value">{results.get('total_issues', 0)}</div>
                <div class="metric-detail">recommended changes</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Priority items</div>
                <div class="metric-value">{results.get('critical_issues', 0)}</div>
                <div class="metric-detail">requiring attention</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    score_col, profile_col = st.columns([1.15, 0.85], gap="large")
    with score_col:
        st.plotly_chart(
            create_score_chart(results['overall_score']),
            width="stretch",
            config={"displayModeBar": False},
        )

    with profile_col:
        details = personal_details or {}
        st.markdown(
            f"""
            <div class="profile-card">
                <div class="eyebrow">Candidate profile</div>
                <h3 class="profile-name">{candidate_name}</h3>
                <div class="profile-role">{role}</div>
                <div class="profile-grid">
                    <div class="profile-item">
                        <span>Company</span>
                        <strong>{safe_text(details.get('current_company'))}</strong>
                    </div>
                    <div class="profile-item">
                        <span>Education</span>
                        <strong>{safe_text(details.get('last_education'))}</strong>
                    </div>
                    <div class="profile-item">
                        <span>Email</span>
                        <strong>{safe_text(details.get('email'))}</strong>
                    </div>
                    <div class="profile-item">
                        <span>Phone</span>
                        <strong>{safe_text(details.get('phone'))}</strong>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_section_header(
        "Performance",
        "How the resume holds together",
        "The target marker shows the level generally associated with a strong ATS-ready document.",
    )
    st.plotly_chart(
        create_category_breakdown(category_scores),
        width="stretch",
        config={"displayModeBar": False},
    )

    if ai_analysis:
        render_section_header(
            "Professional reading",
            "The story an employer is likely to hear",
        )
        st.markdown(
            f"""
            <div class="quote-card">
                <p>{safe_text(ai_analysis.get('professional_summary'), 'No summary available')}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if dynamic_recommendations:
        recommendations = dynamic_recommendations.get('recommendations', [])
        render_section_header(
            "Refinement",
            "The changes most worth making",
            "Each recommendation connects an observed issue to its likely impact and a practical revision.",
        )

        if not recommendations:
            st.info("No priority recommendations were generated for this resume.")

        for i, rec in enumerate(recommendations, 1):
            with st.expander(
                f"{i:02d}  {rec.get('category', 'General')}",
                expanded=i == 1,
            ):
                st.markdown(
                    f"""
                    <div class="recommendation-meta">Observed issue</div>
                    <p>{safe_text(rec.get('issue'), 'Not available')}</p>
                    <div class="recommendation-meta">Why it matters</div>
                    <p>{safe_text(rec.get('impact'), 'Not available')}</p>
                    <div class="recommendation-copy">
                        <div class="recommendation-meta">Recommended revision</div>
                        <p>{safe_text(rec.get('recommendation'), 'Not available')}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        strengths = dynamic_recommendations.get('strengths', [])
        if strengths:
            render_section_header(
                "Strengths",
                "What already deserves to stay",
                "Protect these qualities as you refine the weaker sections.",
            )
            strength_items = "".join(
                f'<div class="strength-item">{safe_text(strength)}</div>'
                for strength in strengths
            )
            st.markdown(
                f'<div class="strength-grid">{strength_items}</div>',
                unsafe_allow_html=True,
            )

    render_section_header(
        "Deeper review",
        "Move from diagnosis to revision",
        "Open the detailed review for line-of-thought guidance on weaknesses and concrete enhancements.",
    )
    action_col, spacer_col = st.columns([0.55, 1.45], gap="large")
    with action_col:
        if st.button("Open detailed review", type="primary", width="stretch"):
            SessionManager.set('show_detailed_analysis', True)
            st.rerun()


def ask_resume_question(question):
    """Query the resume RAG pipeline and store the response in session history."""
    normalized_question = question.strip()
    if not normalized_question:
        return

    rag_chain = SessionManager.get('rag_chain')
    if not rag_chain:
        st.error("RAG system not initialized. Please restart the analysis.")
        return

    with st.spinner("Searching your resume..."):
        result = rag_chain.query(normalized_question)

    if not result:
        st.error("Unable to process your question. Please try again.")
        return

    qa_history = list(SessionManager.get('qa_history', []))
    qa_history.append({
        'question': normalized_question,
        'answer': result['answer'],
        'confidence': result.get('confidence', 'Low')
    })
    SessionManager.set('qa_history', qa_history)


def display_resume_qa():
    """Display a bottom-right resume chat backed by the RAG pipeline."""
    with st.container(key="resume_chat_widget"):
        with st.popover("Ask your resume", width="stretch"):
            st.markdown('<div class="eyebrow">Resume conversation</div>', unsafe_allow_html=True)
            st.subheader("Ask a focused question")
            st.caption("Answers use only the document from this session.")

            qa_history = SessionManager.get('qa_history', [])
            if not qa_history:
                st.info("Try asking about experience, education, strengths, or missing details.")

            for qa_pair in qa_history:
                with st.chat_message("user", avatar=":material/person:"):
                    st.markdown(qa_pair['question'])

                with st.chat_message("assistant", avatar=":material/ink_highlighter:"):
                    st.markdown(qa_pair['answer'])
                    confidence = qa_pair.get('confidence')
                    if confidence:
                        st.caption(f"Confidence: {confidence}")

            with st.form("resume_chat_form", clear_on_submit=True):
                user_question = st.text_input(
                    "Question",
                    placeholder="What are my strongest skills?",
                    label_visibility="collapsed"
                )
                ask_button = st.form_submit_button(
                    "Ask",
                    type="primary",
                    width="stretch"
                )

            if ask_button:
                ask_resume_question(user_question)
                st.rerun()

def display_detailed_analysis():
    """Display detailed weak points analysis"""
    resume_text = SessionManager.get('resume_text', '')
    category_scores = SessionManager.get('analysis_results', {}).get('category_scores', {})
    detailed_analysis = SessionManager.get('detailed_analysis')

    header_col, action_col = st.columns([1.5, 0.5], gap="large")
    with header_col:
        st.markdown(
            """
            <div class="results-hero">
                <div class="eyebrow">Detailed review</div>
                <h1>Turn the diagnosis into better language.</h1>
                <p>Work through the highest-value weaknesses, then compare practical before-and-after improvements.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with action_col:
        st.write("")
        st.write("")
        if st.button("Back to overview", width="stretch"):
            SessionManager.set('show_detailed_analysis', False)
            st.rerun()

    if detailed_analysis is None:
        try:
            with st.spinner("Preparing the detailed editorial review..."):
                groq_analyzer = GroqResumeAnalyzer()
                detailed_analysis = groq_analyzer.generate_dynamic_detailed_analysis(
                    resume_text,
                    category_scores,
                )
                SessionManager.set('detailed_analysis', detailed_analysis)
        except Exception as e:
            ErrorHandler.handle_api_error(e, "Detailed analysis")
            return

    weak_points = detailed_analysis.get('weak_points', [])
    render_section_header(
        "Areas for improvement",
        "Where the resume loses momentum",
        "These are the passages or patterns most likely to weaken clarity, relevance, or credibility.",
    )

    if not weak_points:
        st.info("No detailed weak points were returned for this resume.")

    for index, point in enumerate(weak_points, 1):
        with st.expander(
            f"{index:02d}  {point.get('title', 'Improvement area')}",
            expanded=index == 1,
        ):
            st.markdown(
                f"""
                <div class="recommendation-meta">Current issue</div>
                <p>{safe_text(point.get('current_issue'), 'Not available')}</p>
                <div class="recommendation-meta">Likely impact</div>
                <p>{safe_text(point.get('impact'), 'Not available')}</p>
                <div class="recommendation-copy">
                    <div class="recommendation-meta">Editorial direction</div>
                    <p>{safe_text(point.get('enhanced_suggestion'), 'Not available')}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    enhancements = detailed_analysis.get('enhancements', [])
    render_section_header(
        "Concrete enhancements",
        "A clearer version, side by side",
        "Use these examples as patterns rather than fixed copy; preserve your own facts and voice.",
    )

    if not enhancements:
        st.info("No before-and-after enhancements were returned for this resume.")

    for index, enhancement in enumerate(enhancements, 1):
        st.markdown(
            f"""
            <div class="detail-card">
                <div class="recommendation-meta">
                    {index:02d} · {safe_text(enhancement.get('category'), 'General')}
                </div>
                <h3>Before</h3>
                <p>{safe_text(enhancement.get('before'), 'Not available')}</p>
                <div class="recommendation-copy">
                    <div class="recommendation-meta">Refined version</div>
                    <p>{safe_text(enhancement.get('after'), 'Not available')}</p>
                </div>
                <h3 style="margin-top: 1.2rem;">Why this is stronger</h3>
                <p>{safe_text(enhancement.get('explanation'), 'Not available')}</p>
            </div>
            <div style="height: 1rem;"></div>
            """,
            unsafe_allow_html=True,
        )

def main():
    """Main application flow"""
    init_app()

    # File upload
    uploaded_file = upload_section()

    if SessionManager.get('analysis_complete'):
        render_app_header("Analysis workspace")
        if SessionManager.get('show_detailed_analysis'):
            display_detailed_analysis()
        else:
            display_results()

        if SessionManager.get('rag_initialized'):
            display_resume_qa()
    else:
        render_app_header()
        display_landing(uploaded_file)

    st.markdown(
        """
        <div class="app-footer">
            ResumeAscend · Thoughtful resume intelligence powered by Groq
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
