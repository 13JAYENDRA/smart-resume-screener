import re
import PyPDF2
from io import BytesIO
from typing import Dict, List

def parse_resume(content: bytes, filename: str) -> Dict:
    """Parse resume and extract structured data"""
    
    # Extract text based on file type
    if filename.endswith('.pdf'):
        text = extract_text_from_pdf(content)
    else:
        text = content.decode('utf-8', errors='ignore')
    
    # Extract structured data
    parsed_data = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "experience": extract_experience(text),
        "education": extract_education(text),
        "raw_text": text[:1000]  # First 1000 chars for reference
    }
    
    return parsed_data

def extract_text_from_pdf(content: bytes) -> str:
    """Extract text from PDF bytes"""
    try:
        pdf_file = BytesIO(content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

def extract_name(text: str) -> str:
    """Extract candidate name (first few lines usually contain name)"""
    lines = text.split('\n')
    for line in lines[:5]:
        line = line.strip()
        # Simple heuristic: name is usually 2-4 words, capitalized
        if len(line.split()) <= 4 and len(line) > 3:
            if not any(keyword in line.lower() for keyword in ['resume', 'cv', 'email', 'phone', 'address']):
                return line
    return "Not Found"

def extract_email(text: str) -> str:
    """Extract email address"""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_pattern, text)
    return match.group(0) if match else "Not Found"

def extract_phone(text: str) -> str:
    """Extract phone number"""
    phone_patterns = [
        r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\d{10}',
        r'\d{3}[-.\s]\d{3}[-.\s]\d{4}'
    ]
    
    for pattern in phone_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return "Not Found"

def extract_skills(text: str) -> List[str]:
    """Extract skills from resume"""
    
    # Common technical skills to look for
    common_skills = [
        'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin',
        'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring',
        'sql', 'mysql', 'postgresql', 'mongodb', 'oracle', 'redis',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
        'git', 'agile', 'scrum', 'jira',
        'machine learning', 'deep learning', 'ai', 'nlp', 'computer vision',
        'data analysis', 'data science', 'statistics',
        'html', 'css', 'typescript', 'rest api', 'graphql',
        'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
        'communication', 'leadership', 'teamwork', 'problem solving'
    ]
    
    text_lower = text.lower()
    found_skills = []
    
    for skill in common_skills:
        if skill in text_lower:
            found_skills.append(skill.title())
    
    # Look for skills section
    skills_section = re.search(r'skills?:?\s*(.*?)(?=\n\n|\nexperience|\neducation|$)', 
                               text, re.IGNORECASE | re.DOTALL)
    
    if skills_section:
        skills_text = skills_section.group(1)
        # Extract comma or bullet separated items
        additional_skills = re.findall(r'[•\-\*]?\s*([A-Za-z][A-Za-z\s\+\#\.]+?)(?=[,\n•\-\*]|$)', skills_text)
        found_skills.extend([s.strip().title() for s in additional_skills if len(s.strip()) > 2])
    
    # Remove duplicates and return
    return list(set(found_skills))[:15]  # Limit to 15 skills

def extract_experience(text: str) -> List[Dict]:
    """Extract work experience"""
    
    experience = []
    
    # Look for experience section
    exp_section = re.search(r'(?:experience|employment|work history):?\s*(.*?)(?=\n\n(?:education|skills|projects)|$)', 
                           text, re.IGNORECASE | re.DOTALL)
    
    if exp_section:
        exp_text = exp_section.group(1)
        
        # Find years (e.g., 2020-2023, 2020-Present)
        year_patterns = re.finditer(r'(\d{4})\s*[-–]\s*(\d{4}|present|current)', exp_text, re.IGNORECASE)
        
        positions = []
        for match in year_patterns:
            start_year = match.group(1)
            end_year = match.group(2)
            
            # Get text around the years (job title and company)
            context_start = max(0, match.start() - 100)
            context_end = min(len(exp_text), match.end() + 200)
            context = exp_text[context_start:context_end]
            
            positions.append({
                "period": f"{start_year} - {end_year}",
                "details": context.strip()[:200]
            })
        
        experience = positions[:5]  # Limit to 5 most recent
    
    if not experience:
        # If no structured experience found, return a note
        experience = [{"period": "Not structured", "details": "Experience details in raw text"}]
    
    return experience

def extract_education(text: str) -> List[Dict]:
    """Extract education details"""
    
    education = []
    
    # Look for education section
    edu_section = re.search(r'(?:education|academic|qualification):?\s*(.*?)(?=\n\n(?:experience|skills|projects)|$)', 
                           text, re.IGNORECASE | re.DOTALL)
    
    if edu_section:
        edu_text = edu_section.group(1)
        
        # Common degrees
        degrees = ['phd', 'ph.d', 'master', 'bachelor', 'mba', 'b.tech', 'm.tech', 'b.sc', 'm.sc', 'be', 'me']
        
        for degree in degrees:
            if degree in edu_text.lower():
                # Find the line with the degree
                lines = edu_text.split('\n')
                for line in lines:
                    if degree in line.lower():
                        education.append({
                            "degree": line.strip()[:100]
                        })
                        break
        
        # Find graduation years
        years = re.findall(r'(?:graduated|graduation|year)?\s*:?\s*(\d{4})', edu_text, re.IGNORECASE)
        if years and education:
            education[0]["year"] = years[0]
    
    if not education:
        education = [{"degree": "Not specified", "year": "N/A"}]
    
    return education[:3]  # Limit to 3 education entries