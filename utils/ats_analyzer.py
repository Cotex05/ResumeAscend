import re
import string
from collections import Counter
from typing import Dict, List, Tuple

class ATSAnalyzer:
    """
    Comprehensive ATS (Applicant Tracking System) analyzer for resumes
    """
    
    def __init__(self):
        # Common ATS-friendly keywords and skills
        self.technical_skills = {
            'programming': ['python', 'java', 'javascript', 'c++', 'sql', 'html', 'css', 'react', 'angular', 'node.js'],
            'data_science': ['machine learning', 'data analysis', 'pandas', 'numpy', 'tensorflow', 'pytorch', 'scikit-learn'],
            'business': ['project management', 'agile', 'scrum', 'leadership', 'strategic planning', 'business analysis'],
            'design': ['photoshop', 'illustrator', 'figma', 'sketch', 'ui/ux', 'graphic design', 'web design'],
            'marketing': ['seo', 'sem', 'google analytics', 'social media', 'content marketing', 'email marketing']
        }
        
        # Common section headers that ATS looks for
        self.expected_sections = [
            'experience', 'education', 'skills', 'summary', 'objective',
            'projects', 'certifications', 'achievements', 'awards'
        ]
        
        # Action verbs that strengthen resumes
        self.action_verbs = [
            'achieved', 'managed', 'led', 'developed', 'implemented', 'improved',
            'increased', 'decreased', 'created', 'designed', 'analyzed', 'coordinated'
        ]
        
        # Common formatting issues
        self.formatting_flags = {
            'special_chars': r'[^\w\s\-\.\,\(\)\[\]\@\#\%\&\*\+\=\|\\\:\;\"\'\<\>\?\/\!\$\^\~\`]',
            'excessive_caps': r'\b[A-Z]{4,}\b',
            'phone_pattern': r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            'email_pattern': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        }
    
    def analyze_resume(self, resume_text: str) -> Dict:
        """
        Perform comprehensive ATS analysis of resume text
        
        Args:
            resume_text (str): Full text content of the resume
            
        Returns:
            Dict: Complete analysis results
        """
        
        # Prepare text for analysis
        text_lower = resume_text.lower()
        sentences = self._split_into_sentences(resume_text)
        words = self._extract_words(text_lower)
        
        # Perform individual analyses
        keyword_score = self._analyze_keywords(text_lower, words)
        formatting_score = self._analyze_formatting(resume_text)
        content_score = self._analyze_content_quality(resume_text, sentences, words)
        structure_score = self._analyze_structure(text_lower)
        
        # Calculate overall score
        category_scores = {
            'keywords_skills': keyword_score,
            'formatting': formatting_score,
            'content_quality': content_score,
            'structure_organization': structure_score
        }
        
        overall_score = sum(category_scores.values()) // len(category_scores)
        
        # Generate recommendations and insights
        recommendations = self._generate_recommendations(resume_text, category_scores)
        strengths = self._identify_strengths(resume_text, category_scores)
        optimization_tips = self._generate_optimization_tips(category_scores)
        
        # Count issues
        total_issues = len(recommendations)
        critical_issues = sum(1 for rec in recommendations if rec['severity'] == 'High')
        
        return {
            'overall_score': overall_score,
            'category_scores': category_scores,
            'total_issues': total_issues,
            'critical_issues': critical_issues,
            'recommendations': recommendations,
            'strengths': strengths,
            'optimization_tips': optimization_tips
        }
    
    def _analyze_keywords(self, text_lower: str, words: List[str]) -> int:
        """Analyze keyword density and relevance"""
        
        score = 0
        word_count = len(words)
        
        if word_count == 0:
            return 0
        
        # Check for technical skills
        skills_found = 0
        total_skills = sum(len(skills) for skills in self.technical_skills.values())
        
        for category, skills in self.technical_skills.items():
            for skill in skills:
                if skill.lower() in text_lower:
                    skills_found += 1
        
        # Skills coverage (40% of score)
        skills_percentage = min((skills_found / total_skills) * 100, 100)
        score += (skills_percentage * 0.4)
        
        # Action verbs usage (30% of score)
        action_verbs_found = sum(1 for verb in self.action_verbs if verb in text_lower)
        action_verb_score = min((action_verbs_found / len(self.action_verbs)) * 100, 100)
        score += (action_verb_score * 0.3)
        
        # Keyword density (30% of score)
        unique_words = len(set(words))
        keyword_density = (unique_words / word_count) * 100 if word_count > 0 else 0
        density_score = min(keyword_density * 2, 100)  # Normalize to 100
        score += (density_score * 0.3)
        
        return min(int(score), 100)
    
    def _analyze_formatting(self, resume_text: str) -> int:
        """Analyze formatting consistency and ATS compatibility"""
        
        score = 100
        
        # Check for problematic characters
        special_chars = re.findall(self.formatting_flags['special_chars'], resume_text)
        if special_chars:
            score -= min(len(special_chars) * 2, 20)
        
        # Check for excessive capitalization
        caps_issues = re.findall(self.formatting_flags['excessive_caps'], resume_text)
        if caps_issues:
            score -= min(len(caps_issues) * 5, 15)
        
        # Check for contact information
        has_email = bool(re.search(self.formatting_flags['email_pattern'], resume_text))
        has_phone = bool(re.search(self.formatting_flags['phone_pattern'], resume_text))
        
        if not has_email:
            score -= 10
        if not has_phone:
            score -= 10
        
        # Check line length (too long lines can cause parsing issues)
        lines = resume_text.split('\n')
        long_lines = [line for line in lines if len(line) > 120]
        if long_lines:
            score -= min(len(long_lines) * 2, 15)
        
        return max(score, 0)
    
    def _analyze_content_quality(self, resume_text: str, sentences: List[str], words: List[str]) -> int:
        """Analyze content quality and professionalism"""
        
        score = 0
        
        # Word count assessment (20% of score)
        word_count = len(words)
        if 200 <= word_count <= 800:
            word_score = 100
        elif word_count < 200:
            word_score = (word_count / 200) * 100
        else:
            word_score = max(100 - ((word_count - 800) / 20), 50)
        
        score += word_score * 0.2
        
        # Sentence length and readability (30% of score)
        if sentences:
            avg_sentence_length = sum(len(sentence.split()) for sentence in sentences) / len(sentences)
            if 10 <= avg_sentence_length <= 25:
                readability_score = 100
            elif avg_sentence_length < 10:
                readability_score = (avg_sentence_length / 10) * 100
            else:
                readability_score = max(100 - ((avg_sentence_length - 25) * 3), 40)
            
            score += readability_score * 0.3
        
        # Quantified achievements (25% of score)
        numbers = re.findall(r'\d+', resume_text)
        percentages = re.findall(r'\d+%', resume_text)
        achievements_score = min((len(numbers) + len(percentages) * 2) * 10, 100)
        score += achievements_score * 0.25
        
        # Professional language (25% of score)
        professional_words = ['responsible', 'manage', 'develop', 'analyze', 'coordinate', 'implement']
        professional_count = sum(1 for word in professional_words if word in resume_text.lower())
        professional_score = min(professional_count * 20, 100)
        score += professional_score * 0.25
        
        return min(int(score), 100)
    
    def _analyze_structure(self, text_lower: str) -> int:
        """Analyze resume structure and organization"""
        
        score = 0
        
        # Check for expected sections
        sections_found = 0
        for section in self.expected_sections:
            if section in text_lower:
                sections_found += 1
        
        # Section coverage (60% of score)
        section_score = (sections_found / len(self.expected_sections)) * 100
        score += section_score * 0.6
        
        # Check for proper contact information placement (20% of score)
        first_quarter = text_lower[:len(text_lower)//4]
        has_contact_info = bool(re.search(self.formatting_flags['email_pattern'], first_quarter))
        contact_score = 100 if has_contact_info else 50
        score += contact_score * 0.2
        
        # Check for logical flow (20% of score)
        # Experience should come before or after education
        exp_pos = text_lower.find('experience')
        edu_pos = text_lower.find('education')
        
        if exp_pos != -1 and edu_pos != -1:
            flow_score = 100  # Both sections present
        elif exp_pos != -1 or edu_pos != -1:
            flow_score = 70   # One section present
        else:
            flow_score = 30   # Neither section clearly identified
        
        score += flow_score * 0.2
        
        return min(int(score), 100)
    
    def _generate_recommendations(self, resume_text: str, category_scores: Dict[str, int]) -> List[Dict]:
        """Generate specific recommendations based on analysis"""
        
        recommendations = []
        
        # Keywords and Skills recommendations
        if category_scores['keywords_skills'] < 70:
            recommendations.append({
                'category': 'Keywords & Skills',
                'severity': 'High' if category_scores['keywords_skills'] < 50 else 'Medium',
                'issue': 'Limited relevant keywords and technical skills detected',
                'impact': 'ATS systems may not identify your resume as a match for relevant positions',
                'recommendation': 'Add more industry-specific keywords, technical skills, and action verbs. Research job descriptions for target roles and incorporate relevant terminology.'
            })
        
        # Formatting recommendations
        if category_scores['formatting'] < 70:
            recommendations.append({
                'category': 'Formatting',
                'severity': 'High' if category_scores['formatting'] < 50 else 'Medium',
                'issue': 'Formatting issues that may interfere with ATS parsing',
                'impact': 'Poor formatting can cause ATS systems to misread or skip important information',
                'recommendation': 'Use standard fonts, avoid special characters, ensure consistent formatting, and include clear contact information at the top.'
            })
        
        # Content Quality recommendations
        if category_scores['content_quality'] < 70:
            recommendations.append({
                'category': 'Content Quality',
                'severity': 'Medium',
                'issue': 'Content lacks quantified achievements or professional language',
                'impact': 'Resume may not effectively demonstrate your value and impact',
                'recommendation': 'Include specific numbers, percentages, and measurable achievements. Use professional action verbs and maintain appropriate length (300-600 words).'
            })
        
        # Structure recommendations
        if category_scores['structure_organization'] < 70:
            recommendations.append({
                'category': 'Structure & Organization',
                'severity': 'High' if category_scores['structure_organization'] < 50 else 'Medium',
                'issue': 'Missing key sections or poor organization',
                'impact': 'ATS systems expect standard resume sections in logical order',
                'recommendation': 'Include standard sections: Contact Info, Summary/Objective, Experience, Education, Skills. Organize information in a logical, chronological order.'
            })
        
        return recommendations
    
    def _identify_strengths(self, resume_text: str, category_scores: Dict[str, int]) -> List[str]:
        """Identify strengths in the resume"""
        
        strengths = []
        
        if category_scores['keywords_skills'] >= 80:
            strengths.append("Strong keyword optimization with relevant technical skills")
        
        if category_scores['formatting'] >= 80:
            strengths.append("Clean, ATS-friendly formatting and structure")
        
        if category_scores['content_quality'] >= 80:
            strengths.append("High-quality content with quantified achievements")
        
        if category_scores['structure_organization'] >= 80:
            strengths.append("Well-organized with all essential resume sections")
        
        # Check for specific positive indicators
        if re.search(r'\d+%', resume_text):
            strengths.append("Includes quantified achievements with percentages")
        
        if re.search(self.formatting_flags['email_pattern'], resume_text) and re.search(self.formatting_flags['phone_pattern'], resume_text):
            strengths.append("Complete contact information provided")
        
        return strengths
    
    def _generate_optimization_tips(self, category_scores: Dict[str, int]) -> List[str]:
        """Generate general optimization tips"""
        
        tips = []
        
        # Always include general tips
        tips.extend([
            "Use standard section headings like 'Experience', 'Education', 'Skills'",
            "Save your resume as both PDF and Word formats for different ATS systems",
            "Tailor your resume keywords to match specific job descriptions",
            "Keep formatting simple and avoid tables, graphics, or columns",
            "Use bullet points for easy scanning and parsing"
        ])
        
        # Add specific tips based on scores
        if category_scores['keywords_skills'] < 80:
            tips.append("Research industry-specific keywords and incorporate them naturally")
        
        if category_scores['content_quality'] < 80:
            tips.append("Quantify your achievements with specific numbers and percentages")
        
        return tips
    
    # Helper methods
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _extract_words(self, text: str) -> List[str]:
        """Extract words from text"""
        # Remove punctuation and split into words
        text_clean = text.translate(str.maketrans('', '', string.punctuation))
        words = [word for word in text_clean.split() if word.strip()]
        return words
