"""
Cover Letter Generator — AI-powered personalized cover letters
==============================================================
Generates contextual, personalized cover letters based on:
- Job description
- Company name and role
- Candidate profile (skills, experience, achievements)
- Q&A bank insights
"""

import re
from profile import CandidateProfile


class CoverLetterGenerator:
    def __init__(self, profile: CandidateProfile):
        self.profile = profile
        self.template = profile.cover_letter_template

    def extract_keywords_from_jd(self, job_description: str) -> list:
        """Extract tech keywords from job description."""
        keywords = []
        tech_stack = [
            "C#", "ASP.NET", "Core", "Entity Framework", "SQL", "PostgreSQL",
            "Docker", "Kubernetes", "Microservices", "React", "Angular",
            "TypeScript", "JavaScript", "Python", "Java", "AWS", "Azure",
            "GCP", "REST API", "GraphQL", "RabbitMQ", "Redis", "Git",
            "CI/CD", "DevOps", "Agile", "TDD", "Clean Architecture",
            "JWT", "OAuth", "OpenTelemetry", "ELK Stack", "Monitoring"
        ]
        
        for tech in tech_stack:
            if re.search(r'\b' + re.escape(tech) + r'\b', job_description, re.IGNORECASE):
                keywords.append(tech)
        
        return keywords[:6]  # Top 6 matches

    def match_candidate_skills(self, keywords: list) -> str:
        """Build paragraph matching candidate skills to JD requirements."""
        profile_dict = self.profile.to_dict()
        matches = []
        
        skill_mapping = {
            "C#": "C# backend development",
            "ASP.NET": "ASP.NET Core Web API development",
            "Core": "ASP.NET Core framework",
            "Entity Framework": "Entity Framework Core for data access",
            "PostgreSQL": "PostgreSQL database design",
            "Docker": "containerization and Docker",
            "Microservices": "microservices architecture",
            "Angular": "Angular frontend development",
            "Azure": "Azure cloud services",
            "REST API": "REST API design and implementation",
            "JWT": "JWT-based authentication",
            "OpenTelemetry": "observability and monitoring",
            "Performance": "API performance optimization",
        }
        
        for keyword in keywords:
            if keyword in skill_mapping:
                matches.append(skill_mapping[keyword])
        
        if matches:
            skills_str = ", ".join(matches[:4])
            return f"I bring hands-on experience with {skills_str}, which directly aligns with your requirements."
        return "I bring relevant technical expertise that aligns with your requirements."

    def generate(self, company_name: str, job_title: str, job_description: str = "") -> str:
        """Generate personalized cover letter."""
        letter = self.template
        
        # Replace placeholders
        letter = letter.replace("[Role]", job_title)
        letter = letter.replace("[Company]", company_name)
        
        # Extract keywords and generate custom reason
        keywords = self.extract_keywords_from_jd(job_description) if job_description else []
        
        if keywords:
            skills_match = self.match_candidate_skills(keywords)
            custom_reason = f"your team is building impactful systems using {', '.join(keywords[:3])}"
            letter = letter.replace(
                "I am particularly interested in this role because [custom reason].",
                f"I am particularly interested in this role because {custom_reason}."
            )
            
            # Replace generic skills line with personalized match
            letter = letter.replace(
                "and integrated OpenTelemetry for observability across 100+ APIs",
                skills_match
            )
        
        return letter

    def format_for_display(self, letter: str) -> str:
        """Format cover letter for nice display."""
        return f"""
{'='*70}
PERSONALIZED COVER LETTER
{'='*70}

{letter}

{'='*70}
"""
