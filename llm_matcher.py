import requests
import json
import re
from typing import Dict, List

# Using Groq API (Free tier: 30 requests/min)
GROQ_API_KEY = "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"  # Get free key from Groq
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

USE_OLLAMA = False
OLLAMA_URL = "http://localhost:11434/api/generate"

def match_candidate_with_job(parsed_resume: Dict, job_description: str) -> Dict:
    """
    Enhanced matching with section-wise scoring
    Returns: {
        "score": int (1-10),
        "justification": str,
        "section_scores": {
            "skills": int,
            "experience": int,
            "education": int,
            "cultural_fit": int,
            "leadership": int
        },
        "strengths": List[str],
        "gaps": List[str],
        "recommendations": str
    }
    """
    
    prompt = create_enhanced_prompt(parsed_resume, job_description)
    
    if USE_OLLAMA:
        response = query_ollama(prompt)
    else:
        response = query_groq(prompt)
    
    result = parse_enhanced_response(response, parsed_resume, job_description)
    
    return result

def create_enhanced_prompt(parsed_resume: Dict, job_description: str) -> str:
    """Create detailed prompt for section-wise analysis"""
    
    skills_str = ", ".join(parsed_resume.get("skills", []))
    experience_str = "\n".join([f"- {exp.get('period', '')}: {exp.get('details', '')}" 
                                for exp in parsed_resume.get("experience", [])])
    education_str = "\n".join([f"- {edu.get('degree', '')} ({edu.get('year', 'N/A')})" 
                               for edu in parsed_resume.get("education", [])])
    
    prompt = f"""You are an expert HR recruiter with deep understanding of candidate evaluation. Analyze this candidate comprehensively.

**Job Description:**
{job_description}

**Candidate Profile:**

Name: {parsed_resume.get('name', 'Not specified')}
Email: {parsed_resume.get('email', 'Not specified')}

Skills: {skills_str if skills_str else 'Not specified'}

Experience:
{experience_str if experience_str else 'Not specified'}

Education:
{education_str if education_str else 'Not specified'}

**Your Task:**
Provide a comprehensive evaluation with section-wise scores (1-10 for each):

1. **Skills Match Score** (1-10): How well do technical skills align?
2. **Experience Score** (1-10): Relevant experience quality and duration?
3. **Education Score** (1-10): Educational background fit?
4. **Cultural Fit Score** (1-10): Soft skills, communication, teamwork indicators?
5. **Leadership Potential Score** (1-10): Leadership, mentorship, impact potential?

Also provide:
- **Overall Score** (1-10): Weighted average
- **Top 3 Strengths**: What makes this candidate stand out?
- **Top 3 Gaps**: What's missing or needs improvement?
- **Recommendation**: Hire/Interview/Reject with reasoning

**Output Format (STRICTLY follow this):**
Overall Score: [number]
Skills Score: [number]
Experience Score: [number]
Education Score: [number]
Cultural Fit Score: [number]
Leadership Score: [number]
Strengths: [strength1], [strength2], [strength3]
Gaps: [gap1], [gap2], [gap3]
Recommendation: [Your detailed recommendation in 2-3 sentences]

Respond with only these fields, nothing else."""

    return prompt

def query_groq(prompt: str) -> str:
    """Query Groq API"""
    
    if GROQ_API_KEY == "your_groq_api_key_here":
        return fallback_enhanced_scoring(prompt)
    
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are an expert HR recruiter with deep analytical skills."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 800
        }
        
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    except Exception as e:
        print(f"Groq API Error: {str(e)}")
        return fallback_enhanced_scoring(prompt)

def query_ollama(prompt: str) -> str:
    """Query local Ollama"""
    
    try:
        payload = {
            "model": "llama2",
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        return result["response"]
    
    except Exception as e:
        print(f"Ollama Error: {str(e)}")
        return fallback_enhanced_scoring(prompt)

def fallback_enhanced_scoring(prompt: str) -> str:
    """Enhanced rule-based scoring with section breakdown"""
    
    # Extract job requirements
    job_skills = re.findall(r'\b(?:python|java|javascript|react|node|sql|aws|docker|kubernetes|machine learning|ai|data science|django|fastapi|leadership|communication|teamwork)\b', 
                           prompt.lower())
    
    # Extract candidate skills
    skills_match = re.search(r'Skills: (.*?)(?:\n|$)', prompt)
    candidate_skills = []
    if skills_match:
        candidate_skills = [s.strip().lower() for s in skills_match.group(1).split(',')]
    
    # Extract experience years
    exp_years = 0
    exp_match = re.search(r'(\d+)\+?\s*years?', prompt.lower())
    if exp_match:
        exp_years = int(exp_match.group(1))
    
    # Calculate section scores
    matched_skills = [skill for skill in job_skills if any(skill in cs for cs in candidate_skills)]
    
    skills_score = min(10, max(1, int((len(matched_skills) / max(len(job_skills), 1)) * 10)))
    experience_score = min(10, max(1, int(exp_years / 5 * 10))) if exp_years > 0 else 5
    education_score = 7  # Default moderate score
    cultural_fit_score = 6 if any(word in prompt.lower() for word in ['leadership', 'team', 'communication']) else 5
    leadership_score = 7 if 'senior' in prompt.lower() or 'lead' in prompt.lower() else 5
    
    overall_score = int((skills_score * 0.3 + experience_score * 0.3 + education_score * 0.2 + 
                        cultural_fit_score * 0.1 + leadership_score * 0.1))
    
    # Generate strengths and gaps
    strengths = []
    if skills_score >= 7:
        strengths.append("Strong technical skill alignment")
    if experience_score >= 7:
        strengths.append("Relevant work experience")
    if leadership_score >= 7:
        strengths.append("Leadership potential")
    
    if not strengths:
        strengths = ["Basic qualifications met", "Potential for growth", "Willingness to learn"]
    
    gaps = []
    if skills_score < 7:
        gaps.append("Some technical skills missing")
    if experience_score < 7:
        gaps.append("Limited relevant experience")
    if cultural_fit_score < 7:
        gaps.append("Soft skills not clearly demonstrated")
    
    if not gaps:
        gaps = ["Minor skill gaps", "Could improve documentation", "Additional certifications beneficial"]
    
    recommendation = f"Candidate scores {overall_score}/10 overall. "
    if overall_score >= 8:
        recommendation += "Strong fit - highly recommend for interview. Demonstrates excellent alignment with requirements."
    elif overall_score >= 6:
        recommendation += "Moderate fit - consider for interview with additional screening. Shows potential but has some gaps."
    else:
        recommendation += "Limited fit - may not meet current requirements. Consider for alternative positions or future opportunities."
    
    return f"""Overall Score: {overall_score}
Skills Score: {skills_score}
Experience Score: {experience_score}
Education Score: {education_score}
Cultural Fit Score: {cultural_fit_score}
Leadership Score: {leadership_score}
Strengths: {', '.join(strengths[:3])}
Gaps: {', '.join(gaps[:3])}
Recommendation: {recommendation}"""

def parse_enhanced_response(response: str, parsed_resume: Dict, job_description: str) -> Dict:
    """Parse enhanced LLM response with section scores"""
    
    try:
        # Extract all scores
        overall_score = extract_score(response, "Overall Score")
        skills_score = extract_score(response, "Skills Score")
        experience_score = extract_score(response, "Experience Score")
        education_score = extract_score(response, "Education Score")
        cultural_fit_score = extract_score(response, "Cultural Fit Score")
        leadership_score = extract_score(response, "Leadership Score")
        
        # Extract strengths
        strengths_match = re.search(r'Strengths?:\s*(.+?)(?=\n\w+:|$)', response, re.IGNORECASE | re.DOTALL)
        strengths = []
        if strengths_match:
            strengths = [s.strip() for s in re.split(r'[,;]|\d+\.', strengths_match.group(1)) if s.strip()][:3]
        
        # Extract gaps
        gaps_match = re.search(r'Gaps?:\s*(.+?)(?=\n\w+:|$)', response, re.IGNORECASE | re.DOTALL)
        gaps = []
        if gaps_match:
            gaps = [g.strip() for g in re.split(r'[,;]|\d+\.', gaps_match.group(1)) if g.strip()][:3]
        
        # Extract recommendation
        recommendation_match = re.search(r'Recommendation:\s*(.+)', response, re.IGNORECASE | re.DOTALL)
        recommendation = recommendation_match.group(1).strip()[:500] if recommendation_match else "No specific recommendation provided."
        
        return {
            "score": overall_score,
            "justification": recommendation,
            "section_scores": {
                "skills": skills_score,
                "experience": experience_score,
                "education": education_score,
                "cultural_fit": cultural_fit_score,
                "leadership": leadership_score
            },
            "strengths": strengths if strengths else ["Analysis in progress"],
            "gaps": gaps if gaps else ["Analysis in progress"],
            "recommendation": recommendation
        }
    
    except Exception as e:
        print(f"Parsing error: {str(e)}")
        return {
            "score": 5,
            "justification": response[:500],
            "section_scores": {
                "skills": 5,
                "experience": 5,
                "education": 5,
                "cultural_fit": 5,
                "leadership": 5
            },
            "strengths": ["Error in analysis"],
            "gaps": ["Error in analysis"],
            "recommendation": response[:300]
        }

def extract_score(text: str, label: str) -> int:
    """Extract numeric score from text"""
    pattern = f'{label}:?\\s*(\\d+)'
    match = re.search(pattern, text, re.IGNORECASE)
    score = int(match.group(1)) if match else 5
    return max(1, min(10, score))