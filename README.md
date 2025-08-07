# AI Resume Screening Tool

A professional AI-powered resume analysis tool that evaluates ATS compatibility and provides intelligent optimization recommendations.

## Features

- **ATS Compatibility Analysis** - Comprehensive scoring across multiple categories
- **AI-Powered Insights** - Dynamic recommendations using Groq's Llama 3.1 model
- **Personal Details Extraction** - Automatic extraction of candidate information
- **Interactive Visualizations** - Professional charts and gauge displays
- **Detailed Analysis** - Specific weak points identification and enhancement suggestions
- **Multi-Format Support** - PDF and DOCX file processing

## Quick Start

1. **Environment Setup**
   ```bash
   # Set your Groq API key as an environment variable
   export GROQ_API_KEY=your_api_key_here
   ```

2. **Local Installation**
   ```bash
   git clone <repository-url>
   cd ai-resume-screening-tool
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run Application**
   ```bash
   streamlit run app.py
   ```

## Architecture

### Modular Design
```
├── app.py                 # Main application entry point
├── config.py             # Configuration and environment variables
├── core/                 # Core application modules
│   ├── session_manager.py    # Streamlit session state management
│   └── error_handler.py      # Centralized error handling
├── utils/                # Utility modules
│   ├── text_extractor.py     # File processing (PDF/DOCX)
│   ├── ats_analyzer.py       # ATS compatibility analysis
│   ├── groq_analyzer.py      # AI-powered analysis
│   └── visualizations.py     # Chart generation
└── .streamlit/          # Streamlit configuration
    └── config.toml
```

### Key Components

- **Configuration Management** - Centralized settings and environment variables
- **Session Management** - Clean state handling for Streamlit
- **Error Handling** - Robust error management with user-friendly messages
- **Modular Utilities** - Separated concerns for maintainability

## Configuration

Required environment variables:
- `GROQ_API_KEY` - Your Groq Cloud API key for AI features

Optional configuration (in `config.py`):
- `MAX_FILE_SIZE_MB` - Maximum upload file size (default: 10MB)
- `SUPPORTED_FILE_TYPES` - Allowed file formats (default: pdf, docx)

## Dependencies

- **streamlit** - Web application framework
- **groq** - AI model integration
- **plotly** - Interactive visualizations
- **pandas** - Data processing
- **PyPDF2** - PDF text extraction
- **python-docx** - Word document processing
- **python-dotenv** - Environment variable management

## Usage

1. Upload your resume (PDF or DOCX format)
2. Click "Analyze Resume" to start the analysis
3. View comprehensive ATS compatibility scores
4. Review AI-generated recommendations and insights
5. Access detailed analysis for specific improvement suggestions

## Development

The application follows clean architecture principles:

- **Separation of Concerns** - Each module has a specific responsibility
- **Environment Configuration** - All settings managed through environment variables
- **Error Resilience** - Comprehensive error handling throughout
- **Modular Design** - Easy to extend and maintain

## Security

- API keys are managed through environment variables
- No sensitive data is stored in the codebase
- Secure file processing with size and type validation