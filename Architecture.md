# Application Architecture

## Overview

A professional AI-powered resume screening tool built with clean, modular architecture. The application analyzes resume compatibility with Applicant Tracking Systems (ATS) using advanced AI models and provides comprehensive optimization recommendations. Features include dynamic AI-generated insights, personal details extraction, interactive visualizations, and detailed weak points analysis.

## Recent Changes (August 2025)

- **Enhanced Modular Architecture** - Separated concerns into core modules for session management and error handling
- **Environment Variable Integration** - Moved all API keys and configuration to environment variables for security
- **Streamlined Codebase** - Removed unnecessary files and simplified application structure
- **Improved Error Handling** - Centralized error management with user-friendly messages
- **Configuration Management** - Centralized all settings in config.py module
- **Extended Personal Details** - Added email and phone number extraction to candidate information display

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

**Clean Modular Design**: The application follows enterprise-level separation of concerns:

**Core Modules**:
- `core/session_manager.py` - Centralized Streamlit session state management
- `core/error_handler.py` - Robust error handling with user-friendly messages
- `config.py` - Configuration management and environment variables

**Utility Modules**:
- `utils/text_extractor.py` - Multi-format file processing (PDF/DOCX)
- `utils/ats_analyzer.py` - Comprehensive ATS compatibility scoring
- `utils/groq_analyzer.py` - AI-powered analysis using Groq Cloud API
- `utils/visualizations.py` - Interactive Plotly visualizations

**Main Application**:
- `app.py` - Clean, streamlined main application with modular imports
- Environment variable integration for secure API key management
- Comprehensive error handling throughout the application flow

**Analysis Engine**: Multi-dimensional resume evaluation:
- Technical keyword matching across industry categories
- Formatting and structure validation for ATS compatibility
- AI-powered personal details extraction and professional summaries
- Dynamic recommendations based on actual resume content
- Detailed weak points analysis with specific improvement suggestions

## External Dependencies

**Core Framework**: Streamlit for web application framework and user interface components.

**AI/ML Services**: Groq Cloud API with llama-3.1-8b-instant model for AI-powered resume analysis, personal details extraction, and dynamic recommendations.

**File Processing Libraries**: 
- PyPDF2 for PDF text extraction
- python-docx for DOCX document processing

**Data Processing**: pandas for data manipulation and analysis operations.

**Visualization**: Plotly (plotly.graph_objects and plotly.express) for creating interactive charts, gauges, and data visualizations.

**Text Processing**: Standard Python libraries (re, string, collections) for regex operations, text analysis, and data structure handling.

**Environment Management**: python-dotenv for managing environment variables and API keys securely.

## Local Setup Information

The application can be run locally using Python virtual environments. Key setup requirements:
- Python 3.8 or higher
- Groq API key for AI features
- Virtual environment for dependency isolation
- All dependencies listed in the setup guide and automated setup script
