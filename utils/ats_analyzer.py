import re
import string
import spacy
from spacy.matcher import PhraseMatcher
from collections import Counter
from typing import Dict, List, Tuple
import logging

class ATSAnalyzer:
    """
    Comprehensive ATS (Applicant Tracking System) analyzer for resumes,
    powered by spaCy for production-grade accuracy.
    """
    
    def __init__(self):
        # Load spaCy NLP model
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            # Fallback if not downloaded properly, though requirements stipulate it
            from spacy.cli import download
            download("en_core_web_sm")
            self.nlp = spacy.load('en_core_web_sm')
            
        # Common ATS-friendly keywords and skills (Expanded)
        self.technical_skills = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go', 'rust', 'typescript', 'sql', 'html', 'css', 'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring'],
            'data_science': ['machine learning', 'deep learning', 'data analysis', 'pandas', 'numpy', 'tensorflow', 'pytorch', 'scikit-learn', 'nlp', 'computer vision', 'matplotlib', 'seaborn', 'keras', 'sql', 'nosql', 'hadoop', 'spark'],
            'business': ['project management', 'agile', 'scrum', 'leadership', 'strategic planning', 'business analysis', 'stakeholder management', 'kanban', 'six sigma', 'product management', 'pmp'],
            'design': ['photoshop', 'illustrator', 'figma', 'sketch', 'ui/ux', 'graphic design', 'web design', 'invision', 'adobe creative suite', 'wireframing', 'prototyping'],
            'marketing': ['seo', 'sem', 'google analytics', 'social media marketing', 'content marketing', 'email marketing', 'crm', 'hubspot', 'salesforce', 'growth hacking', 'b2b', 'b2c'],
            'cloud_devops': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'ci/cd', 'terraform', 'ansible', 'linux', 'unix']
        }
        
        # Action verbs that strengthen resumes (Expanded)
        self.action_verbs = [
            'achieved', 'managed', 'led', 'developed', 'implemented', 'improved',
            'increased', 'decreased', 'created', 'designed', 'analyzed', 'coordinated',
            'orchestrated', 'spearheaded', 'executed', 'delivered', 'optimized', 'transformed',
            'resolved', 'negotiated', 'streamlined', 'mentored', 'facilitated', 'pioneered',
            'revamped', 'maximized', 'minimized', 'formulated', 'engineered', 'architected'
        ]
        
        # Buzzwords to penalize (fluff words)
        self.buzzwords = [
            'team player', 'synergy', 'think outside the box', 'go-getter',
            'hard worker', 'detail-oriented', 'results-driven', 'dynamic',
            'self-starter', 'thought leadership', 'rockstar', 'guru', 'ninja'
        ]
        
        # Expected sections (Expanded variations)
        self.expected_sections = {
            'experience': ['experience', 'work experience', 'employment history', 'work history', 'professional experience', 'career history'],
            'education': ['education', 'academic background', 'academic history', 'degrees'],
            'skills': ['skills', 'technical skills', 'core competencies', 'expertise'],
            'summary': ['summary', 'professional summary', 'executive summary', 'profile', 'objective'],
            'projects': ['projects', 'personal projects', 'academic projects', 'portfolio'],
            'certifications': ['certifications', 'licenses', 'training']
        }
        
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
        """
        # Process text with spaCy
        doc = self.nlp(resume_text)
        text_lower = resume_text.lower()
        
        # Extract meaningful words (no stopwords, no punctuation)
        words = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
        sentences = list(doc.sents)
        
        # Perform individual analyses
        keyword_score = self._analyze_keywords(text_lower, words, doc)
        formatting_score = self._analyze_formatting(resume_text)
        content_score = self._analyze_content_quality(resume_text, sentences, doc)
        structure_score = self._analyze_structure(resume_text)
        
        # Industry-standard weighted calculation
        category_scores = {
            'keywords_skills': keyword_score,
            'structure_organization': structure_score,
            'content_quality': content_score,
            'formatting': formatting_score
        }
        
        # Weighted Overall Score (Keywords 35%, Structure 30%, Content 20%, Formatting 15%)
        overall_score = (
            (keyword_score * 0.35) +
            (structure_score * 0.30) +
            (content_score * 0.20) +
            (formatting_score * 0.15)
        )
        overall_score = int(min(max(overall_score, 0), 100))
        
        # Generate recommendations and insights
        recommendations = self._generate_recommendations(category_scores)
        strengths = self._identify_strengths(resume_text, category_scores)
        optimization_tips = self._generate_optimization_tips(category_scores)
        
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
    
    def _analyze_keywords(self, text_lower: str, words: List[str], doc) -> int:
        """Analyze keyword density and relevance using NLP bounding"""
        score = 0
        word_count = len(words)
        if word_count == 0:
            return 0
        
        # Check for technical skills using word boundaries to prevent substring matches
        skills_found = 0
        total_skills = sum(len(skills) for skills in self.technical_skills.values())
        
        for category, skills in self.technical_skills.items():
            for skill in skills:
                # Use regex \b for exact word boundary match
                if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text_lower):
                    skills_found += 1
        
        # Skills coverage (40% of score)
        # Assuming finding 15 relevant skills is considered 100%
        target_skills = 15
        skills_percentage = min((skills_found / target_skills) * 100, 100)
        score += (skills_percentage * 0.4)
        
        # Action verbs usage (40% of score)
        action_verbs_found = 0
        for verb in self.action_verbs:
            if re.search(r'\b' + re.escape(verb.lower()) + r'\b', text_lower):
                action_verbs_found += 1
        
        target_verbs = 10
        action_verb_score = min((action_verbs_found / target_verbs) * 100, 100)
        score += (action_verb_score * 0.4)
        
        # Keyword density (without stopwords) (20% of score)
        unique_words = len(set(words))
        keyword_density = (unique_words / word_count) * 100 if word_count > 0 else 0
        # Optimal density is usually between 40-70% when stopwords are removed
        if 40 <= keyword_density <= 80:
            density_score = 100
        else:
            density_score = min(keyword_density * 1.5, 100)
        
        score += (density_score * 0.2)
        
        return min(int(score), 100)
    
    def _analyze_formatting(self, resume_text: str) -> int:
        """Analyze formatting consistency and ATS compatibility"""
        score = 100
        
        special_chars = re.findall(self.formatting_flags['special_chars'], resume_text)
        if special_chars:
            score -= min(len(special_chars) * 2, 20)
        
        caps_issues = re.findall(self.formatting_flags['excessive_caps'], resume_text)
        if caps_issues:
            score -= min(len(caps_issues) * 5, 15)
        
        has_email = bool(re.search(self.formatting_flags['email_pattern'], resume_text))
        has_phone = bool(re.search(self.formatting_flags['phone_pattern'], resume_text))
        
        if not has_email:
            score -= 10
        if not has_phone:
            score -= 10
            
        lines = resume_text.split('\n')
        long_lines = [line for line in lines if len(line) > 130]
        if long_lines:
            score -= min(len(long_lines) * 2, 15)
            
        return max(score, 0)
    
    def _analyze_content_quality(self, resume_text: str, sentences: List, doc) -> int:
        """Analyze content quality with NLP and readability metrics"""
        score = 0
        
        # Get raw words count (including stopwords but not punctuation)
        raw_words = [token for token in doc if not token.is_punct and not token.is_space]
        word_count = len(raw_words)
        
        # 1. Length Assessment (20% of score)
        if 300 <= word_count <= 1000:
            word_score = 100
        elif word_count < 300:
            word_score = (word_count / 300) * 100
        else:
            word_score = max(100 - ((word_count - 1000) / 20), 50)
        score += word_score * 0.2
        
        # 2. Readability (Flesch proxy) (30% of score)
        if sentences and raw_words:
            total_words = len(raw_words)
            total_sentences = len(sentences)
            # Rough syllable proxy: vowels per word
            total_vowels = sum(len(re.findall(r'[aeiouy]', token.text.lower())) for token in raw_words)
            total_syllables = max(total_vowels, total_words) # at least 1 per word
            
            # Flesch Reading Ease
            flesch_score = 206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (total_syllables / total_words)
            
            # Optimal resume readability is usually 30-60 (College level)
            if 30 <= flesch_score <= 70:
                readability_score = 100
            elif flesch_score > 70:
                readability_score = max(100 - (flesch_score - 70), 50) # Too simple
            else:
                readability_score = max(100 - (30 - flesch_score) * 2, 40) # Too complex
            
            score += readability_score * 0.3
        
        # 3. High-Impact Quantified Achievements (35% of score)
        # Differentiate between regular numbers and high impact (percentages, money, large numbers)
        high_impact = re.findall(r'(\d+%|\$\d+[kmbKMB]?|\b\d{3,}\b)', resume_text)
        regular_numbers = re.findall(r'\b\d+\b', resume_text)
        
        achievements_score = min((len(high_impact) * 15) + (len(regular_numbers) * 5), 100)
        score += achievements_score * 0.35
        
        # 4. Buzzword Penalty (15% of score)
        buzzwords_found = 0
        text_lower = resume_text.lower()
        for buzz in self.buzzwords:
            if re.search(r'\b' + re.escape(buzz) + r'\b', text_lower):
                buzzwords_found += 1
                
        buzz_score = max(100 - (buzzwords_found * 20), 0)
        score += buzz_score * 0.15
        
        return min(int(score), 100)
    
    def _analyze_structure(self, resume_text: str) -> int:
        """Intelligent section header detection"""
        score = 0
        lines = [line.strip().lower() for line in resume_text.split('\n') if line.strip()]
        
        sections_found = set()
        
        # Look for headers (typically short lines, maybe uppercase, or exact matches)
        for line in lines:
            # Clean the line
            clean_line = re.sub(r'[^a-z\s]', '', line).strip()
            # If line is short (less than 5 words), it might be a header
            if len(clean_line.split()) <= 4:
                for sec_key, variations in self.expected_sections.items():
                    if clean_line in variations:
                        sections_found.add(sec_key)
                        
        # Section coverage (60% of score)
        expected_keys = list(self.expected_sections.keys())
        section_score = (len(sections_found) / len(expected_keys)) * 100
        score += section_score * 0.6
        
        # Contact info placement (20% of score)
        text_lower = resume_text.lower()
        first_quarter = text_lower[:max(len(text_lower)//4, 1)]
        has_contact_info = bool(re.search(self.formatting_flags['email_pattern'], first_quarter))
        contact_score = 100 if has_contact_info else 50
        score += contact_score * 0.2
        
        # Logical flow (20% of score)
        has_exp = 'experience' in sections_found
        has_edu = 'education' in sections_found
        
        if has_exp and has_edu:
            flow_score = 100
        elif has_exp or has_edu:
            flow_score = 70
        else:
            flow_score = 30
            
        score += flow_score * 0.2
        return min(int(score), 100)
    
    def _generate_recommendations(self, category_scores: Dict[str, int]) -> List[Dict]:
        """Generate specific recommendations based on analysis"""
        recommendations = []
        
        if category_scores['keywords_skills'] < 70:
            recommendations.append({
                'category': 'Keywords & Skills',
                'severity': 'High' if category_scores['keywords_skills'] < 50 else 'Medium',
                'issue': 'Limited relevant keywords and action verbs detected',
                'impact': 'ATS systems score you lower if terminology does not match the job description',
                'recommendation': 'Add more industry-specific hard skills. Start bullet points with strong action verbs (e.g., spearheaded, optimized).'
            })
            
        if category_scores['structure_organization'] < 70:
            recommendations.append({
                'category': 'Structure & Organization',
                'severity': 'High' if category_scores['structure_organization'] < 50 else 'Medium',
                'issue': 'Missing recognizable section headers',
                'impact': 'ATS parsers may fail to extract your experience or education properly',
                'recommendation': 'Use standard standalone headers like "Experience", "Education", and "Skills". Avoid creative section names.'
            })
            
        if category_scores['content_quality'] < 70:
            recommendations.append({
                'category': 'Content Quality',
                'severity': 'Medium',
                'issue': 'Content lacks high-impact quantified metrics or uses too many buzzwords',
                'impact': 'Resume may seem subjective rather than results-driven',
                'recommendation': 'Remove clichés (e.g., "team player"). Include concrete metrics ($, %, counts) to quantify your achievements.'
            })
            
        if category_scores['formatting'] < 70:
            recommendations.append({
                'category': 'Formatting',
                'severity': 'High' if category_scores['formatting'] < 50 else 'Medium',
                'issue': 'Formatting irregularities detected',
                'impact': 'Can cause errors in ATS parsing, jumbling your text',
                'recommendation': 'Ensure your contact info is at the very top. Remove special symbols, tables, and excessive capitalizations.'
            })
            
        return recommendations
    
    def _identify_strengths(self, resume_text: str, category_scores: Dict[str, int]) -> List[str]:
        strengths = []
        if category_scores['keywords_skills'] >= 80:
            strengths.append("Excellent keyword optimization and action verb usage")
        if category_scores['structure_organization'] >= 80:
            strengths.append("Standard, easily parsable structure")
        if category_scores['content_quality'] >= 80:
            strengths.append("Results-driven content with good readability and metrics")
        if category_scores['formatting'] >= 80:
            strengths.append("Clean, ATS-friendly formatting")
            
        if re.search(r'(\d+%|\$\d+[kmbKMB]?)', resume_text):
            strengths.append("Includes high-impact quantified achievements (e.g., percentages/financials)")
            
        return strengths
    
    def _generate_optimization_tips(self, category_scores: Dict[str, int]) -> List[str]:
        tips = [
            "Always tailor your resume keywords to closely match the specific job description.",
            "Save your resume as a standard PDF to preserve layout, but ensure it's text-searchable.",
            "Avoid multi-column layouts, graphics, or tables, as older ATS cannot read them."
        ]
        if category_scores['content_quality'] < 80:
            tips.append("Use the XYZ formula for bullets: Accomplished [X] as measured by [Y], by doing [Z].")
        return tips
