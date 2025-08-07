import os
import json
import re
from typing import Dict, Optional
from groq import Groq
from config import Config

class GroqResumeAnalyzer:
    """
    Enhanced resume analyzer using Groq Cloud API with Llama 3.1
    """
    
    def __init__(self):
        """Initialize with API key from environment variables"""
        try:
            api_key = Config.get_groq_api_key()
            self.client = Groq(api_key=api_key)
            self.model = Config.GROQ_MODEL
        except ValueError as e:
            raise ValueError(f"Configuration error: {e}")
    
    def extract_personal_details(self, resume_text: str) -> Dict[str, str]:
        """
        Extract personal details from resume using Llama 3.1
        """
        
        prompt = f"""
        Analyze the following resume text and extract the personal details in JSON format.
        
        Resume Text:
        {resume_text}
        
        Please extract and return ONLY a valid JSON object with these fields:
        {{
            "name": "Full name of the person",
            "email": "Email address",
            "phone": "Phone or contact number",
            "current_company": "Current company or most recent company",
            "job_role": "Current job title or most recent role",
            "last_education": "Most recent education (degree, institution, year)"
        }}
        
        If any information is not found, use "Not specified" as the value.
        Return only the JSON object, no additional text.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert resume parser. Extract information accurately and return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.1,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            if not content:
                raise Exception("Empty response from AI model")
                
            content = content.strip()
            
            # Clean up the response using the helper method
            content = self.clean_json_content(content)
            
            # Parse JSON
            personal_details = json.loads(content)
            
            # Validate required fields
            required_fields = ["name", "current_company", "job_role", "last_education"]
            for field in required_fields:
                if field not in personal_details:
                    personal_details[field] = "Not specified"
            
            return personal_details
            
        except Exception as e:
            print(f"Error extracting personal details: {e}")
            return {
                "name": "Not specified",
                "current_company": "Not specified", 
                "job_role": "Not specified",
                "last_education": "Not specified"
            }
    
    def generate_ai_summary_and_suggestions(self, resume_text: str, ats_score: int) -> Dict[str, str]:
        """
        Generate AI-powered resume summary and improvement suggestions
        """
        
        prompt = f"""
        Analyze this resume and provide insights based on the ATS score of {ats_score}/100.
        
        Resume Text:
        {resume_text}
        
        Please provide:
        1. A concise professional summary (2-3 sentences) highlighting the candidate's key strengths and experience
        2. Specific, actionable suggestions for improvement based on the ATS score
        
        Return your response in this exact JSON format:
        {{
            "professional_summary": "2-3 sentence summary highlighting key strengths and experience",
            "improvement_suggestions": "Specific actionable suggestions for improving the resume and ATS score"
        }}
        
        Make suggestions specific and practical. Consider the ATS score context.
        Return only the JSON object, no additional text.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert career coach and resume writer. Provide insightful, actionable advice."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.3,
                max_tokens=800
            )
            
            content = response.choices[0].message.content
            if not content:
                raise Exception("Empty response from AI model")
                
            content = content.strip()
            
            # Clean up the response using the helper method
            content = self.clean_json_content(content)
            
            # Parse JSON
            ai_analysis = json.loads(content)
            
            # Validate required fields
            if "professional_summary" not in ai_analysis:
                ai_analysis["professional_summary"] = "Professional with diverse experience and skills."
            if "improvement_suggestions" not in ai_analysis:
                ai_analysis["improvement_suggestions"] = "Consider adding more specific achievements and technical skills."
            
            return ai_analysis
            
        except Exception as e:
            print(f"Error generating AI summary: {e}")
            return {
                "professional_summary": "Professional with diverse experience and demonstrated skills across multiple domains.",
                "improvement_suggestions": "Consider quantifying achievements with specific numbers, adding relevant technical skills, and ensuring clear section organization for better ATS compatibility."
            }
    
    def analyze_strengths_and_weaknesses(self, resume_text: str, category_scores: Dict[str, int]) -> Dict[str, list]:
        """
        Generate detailed strengths and weaknesses analysis using AI
        """
        
        prompt = f"""
        Analyze this resume with the following category scores:
        - Keywords & Skills: {category_scores.get('keywords_skills', 0)}/100
        - Formatting: {category_scores.get('formatting', 0)}/100  
        - Content Quality: {category_scores.get('content_quality', 0)}/100
        - Structure & Organization: {category_scores.get('structure_organization', 0)}/100
        
        Resume Text:
        {resume_text}
        
        Provide detailed analysis in JSON format:
        {{
            "strengths": ["strength 1", "strength 2", "strength 3"],
            "weaknesses": ["weakness 1", "weakness 2", "weakness 3"],
            "specific_recommendations": ["recommendation 1", "recommendation 2", "recommendation 3"]
        }}
        
        Make each point specific and actionable. Base analysis on the category scores.
        Return only the JSON object, no additional text.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert ATS and resume optimization specialist."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.2,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            if not content:
                raise Exception("Empty response from AI model")
                
            content = content.strip()
            
            # Clean up the response using the helper method
            content = self.clean_json_content(content)
            
            # Parse JSON
            analysis = json.loads(content)
            
            # Validate and provide defaults
            default_analysis = {
                "strengths": ["Clear professional experience", "Relevant educational background", "Good use of action verbs"],
                "weaknesses": ["Could benefit from more quantified achievements", "Missing some technical keywords", "Formatting could be more ATS-friendly"],
                "specific_recommendations": ["Add specific metrics to achievements", "Include more industry keywords", "Use standard section headers"]
            }
            
            for key in default_analysis:
                if key not in analysis or not analysis[key]:
                    analysis[key] = default_analysis[key]
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing strengths and weaknesses: {e}")
            return {
                "strengths": ["Clear professional experience", "Relevant educational background", "Good use of action verbs"],
                "weaknesses": ["Could benefit from more quantified achievements", "Missing some technical keywords", "Formatting could be more ATS-friendly"],
                "specific_recommendations": ["Add specific metrics to achievements", "Include more industry keywords", "Use standard section headers"]
            }
    
    def clean_json_content(self, content: str) -> str:
        """Clean JSON content by removing control characters"""
        import re
        # Remove control characters that cause JSON parsing issues
        content = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', content)
        
        # Clean up the response to extract JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        return content
    
    def generate_dynamic_recommendations(self, resume_text: str, category_scores: Dict[str, int]) -> Dict[str, list]:
        """Generate dynamic, context-aware recommendations based on actual resume content"""
        
        prompt = f"""
        Analyze this resume and provide specific, actionable recommendations based on the actual content and ATS scores:
        
        Category Scores:
        - Keywords & Skills: {category_scores.get('keywords_skills', 0)}/100
        - Formatting: {category_scores.get('formatting', 0)}/100  
        - Content Quality: {category_scores.get('content_quality', 0)}/100
        - Structure & Organization: {category_scores.get('structure_organization', 0)}/100
        
        Resume Text:
        {resume_text[:2000]}...
        
        Generate specific recommendations in JSON format:
        {{
            "recommendations": [
                {{
                    "category": "specific category name",
                    "issue": "specific issue found in this resume",
                    "impact": "specific impact on ATS compatibility",
                    "recommendation": "specific actionable recommendation",
                    "severity": "High"
                }}
            ],
            "strengths": ["specific strength 1", "specific strength 2"],
            "optimization_tips": ["specific tip 1", "specific tip 2"]
        }}
        
        Base recommendations on actual resume content, not generic advice.
        Return only JSON, no additional text.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert ATS resume analyzer. Provide specific, actionable advice based on actual resume content."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.2,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content
            if not content:
                raise Exception("Empty response from AI model")
                
            content = self.clean_json_content(content.strip())
            dynamic_analysis = json.loads(content)
            
            # Validate structure
            if "recommendations" not in dynamic_analysis:
                dynamic_analysis["recommendations"] = []
            if "strengths" not in dynamic_analysis:
                dynamic_analysis["strengths"] = []
            if "optimization_tips" not in dynamic_analysis:
                dynamic_analysis["optimization_tips"] = []
            
            return dynamic_analysis
            
        except Exception as e:
            print(f"Error generating dynamic recommendations: {e}")
            return {"recommendations": [], "strengths": [], "optimization_tips": []}
    
    def generate_dynamic_detailed_analysis(self, resume_text: str, category_scores: Dict[str, int]) -> Dict[str, list]:
        """Generate dynamic detailed weak points analysis with specific examples from the resume"""
        
        prompt = f"""
        Analyze this specific resume and identify exact weak points with before/after examples:
        
        Category Scores:
        - Keywords & Skills: {category_scores.get('keywords_skills', 0)}/100
        - Formatting: {category_scores.get('formatting', 0)}/100  
        - Content Quality: {category_scores.get('content_quality', 0)}/100
        - Structure: {category_scores.get('structure_organization', 0)}/100
        
        Resume Text:
        {resume_text[:2500]}...
        
        Generate specific weak points and enhancements in JSON format:
        {{
            "weak_points": [
                {{
                    "title": "specific issue title",
                    "current_issue": "exact issue found in this resume",
                    "impact": "specific impact on ATS score",
                    "enhanced_suggestion": "specific improvement suggestion",
                    "expected_improvement": "expected score improvement",
                    "priority": "High"
                }}
            ],
            "enhancements": [
                {{
                    "category": "enhancement category",
                    "before": "actual text from resume that needs improvement",
                    "after": "improved version of the same text",
                    "explanation": "why this improvement helps ATS"
                }}
            ]
        }}
        
        Base analysis on actual resume content. Use real examples from the text.
        Return only JSON, no additional text.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert resume optimization specialist. Analyze actual content and provide specific improvements."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.3,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            if not content:
                raise Exception("Empty response from AI model")
                
            content = self.clean_json_content(content.strip())
            detailed_analysis = json.loads(content)
            
            # Validate structure
            if "weak_points" not in detailed_analysis:
                detailed_analysis["weak_points"] = []
            if "enhancements" not in detailed_analysis:
                detailed_analysis["enhancements"] = []
            
            return detailed_analysis
            
        except Exception as e:
            print(f"Error generating dynamic detailed analysis: {e}")
            return {"weak_points": [], "enhancements": []}