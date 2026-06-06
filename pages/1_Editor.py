import streamlit as st
import os
import sys
import copy

# Ensure imports work when run from pages folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.session_manager import SessionManager
from utils.groq_analyzer import GroqResumeAnalyzer
from utils.document_exporter import DocumentExporter
from ui import inject_theme
from streamlit_pdf_viewer import pdf_viewer

# Configure page
st.set_page_config(
    page_title="Resume Editor | ResumeAscend",
    page_icon="✏️",
    layout="wide"
)

inject_theme()

def render_editor_header():
    st.markdown(
        """
        <div class="resume-shell">
            <div class="brand-lockup">
                <div class="brand-seal">R</div>
                <div>
                    <div class="brand-name">ResumeAscend</div>
                    <div class="brand-note">Clarity for every application</div>
                </div>
            </div>
            <div class="shell-status">Resume Editor</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

render_editor_header()

if not SessionManager.get('resume_json'):
    st.warning("Please upload and analyze a resume first on the main page.")
    if st.button("Go to Analysis"):
        st.switch_page("app.py")
    st.stop()

# Initialize editor state if empty
if not SessionManager.get('editor_versions'):
    SessionManager.set('editor_versions', [{'json': SessionManager.get('resume_json'), 'note': 'Original Upload'}])
    SessionManager.set('editor_index', 0)

versions = SessionManager.get('editor_versions')
current_index = SessionManager.get('editor_index')

# Helper functions for Undo/Redo
def undo():
    if current_index > 0:
        SessionManager.set('editor_index', current_index - 1)

def redo():
    if current_index < len(versions) - 1:
        SessionManager.set('editor_index', current_index + 1)

# Layout: Main Area (Chat Left | Preview Right)
main_left, main_right = st.columns([1, 1.2], gap="large")

with main_left:
    st.markdown('<div class="eyebrow">AI Assistant</div>', unsafe_allow_html=True)
    st.markdown("Instruct the AI to rewrite or update specific sections of the document. For example: *'Shorten the summary'* or *'Add Project Management to skills'*.")
    
    with st.form("editor_chat"):
        edit_prompt = st.text_area("Your instructions:", placeholder="Enter your edits here...", height=200)
        submit_edit = st.form_submit_button("Apply Changes", type="primary", use_container_width=True)
        
    if submit_edit and edit_prompt:
        with st.spinner("Applying your edits to the structure..."):
            analyzer = GroqResumeAnalyzer()
            current_json = versions[current_index]['json']
            new_json = analyzer.apply_json_edits(current_json, edit_prompt)
            
            # Save new version and discard future redo versions if we are not at the end
            new_versions = versions[:current_index + 1]
            note = edit_prompt[:40] + "..." if len(edit_prompt) > 40 else edit_prompt
            new_versions.append({"json": new_json, "note": note})
            
            SessionManager.set('editor_versions', new_versions)
            SessionManager.set('editor_index', len(new_versions) - 1)
            st.rerun()

    st.write("")
    if st.button("Back to Analysis", use_container_width=True):
        st.switch_page("app.py")

with main_right:
    st.markdown('<div class="eyebrow">Live PDF Preview</div>', unsafe_allow_html=True)
    current_json = versions[current_index]['json']
    
    # Generate PDF for preview
    pdf_bytes = None
    try:
        pdf_bytes = DocumentExporter.export_json_to_pdf(current_json)
        
        # Native rendering via streamlit-pdf-viewer
        pdf_viewer(input=pdf_bytes, width=700, height=800)
            
    except Exception as e:
        st.error(f"PDF generation error: {e}")
        st.json(current_json)

# Bottom Section: Timeline and Export
st.markdown("---")
st.markdown('<div class="eyebrow">Version Control & Export</div>', unsafe_allow_html=True)

bottom_left, bottom_right = st.columns([2, 1], gap="large")

with bottom_left:
    st.markdown("### Version History")
    
    col1, col2, _ = st.columns([1, 1, 3])
    with col1:
        st.button("↩ Undo", disabled=(current_index == 0), on_click=undo, use_container_width=True)
    with col2:
        st.button("↪ Redo", disabled=(current_index == len(versions) - 1), on_click=redo, use_container_width=True)
    
    # Horizontal timeline display
    timeline_html = "<div style='display: flex; overflow-x: auto; padding: 10px 0; gap: 15px;'>"
    for i, version in enumerate(versions):
        if i == current_index:
            timeline_html += f"<div style='min-width: 150px; padding: 10px; border-radius: 5px; background: #e6f3ff; border: 1px solid #0066cc; color: #000;'><strong>v{i+1}</strong><br><small>{version['note']}</small></div>"
        else:
            timeline_html += f"<div style='min-width: 150px; padding: 10px; border-radius: 5px; background: #f9f9f9; border: 1px solid #eee; color: #666;'><strong>v{i+1}</strong><br><small>{version['note']}</small></div>"
    timeline_html += "</div>"
    st.markdown(timeline_html, unsafe_allow_html=True)

with bottom_right:
    st.markdown("### Export Document")
    st.markdown("Download the high-quality PDF of this version.")
    
    if pdf_bytes:
        st.download_button(
            label="📥 Download PDF",
            data=pdf_bytes,
            file_name="Updated_Resume.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary"
        )
