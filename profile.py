"""
Profile Loader — Load candidate details from mydetail.md
========================================================
Parses MyDetail.md file and provides structured access to:
- Candidate info (name, email, phone, location, etc.)
- Q&A bank (pre-written answers for common questions)
- Cover letter template
- Resume versions
"""

import re
from typing import Dict, List, Optional


class CandidateProfile:
    def __init__(self, detail_file: str = "mydetail.md"):
        self.detail_file = detail_file
        self.raw_content = self._load_file()
        self.parse_sections()

    def _load_file(self) -> str:
        with open(self.detail_file, "r", encoding="utf-8") as f:
            return f.read()

    def parse_sections(self):
        """Extract sections from markdown."""
        content = self.raw_content
        
        # Extract basic profile
        self.name = self._extract_field(content, r"\*\*Full Name:\*\*\s*(.+)", "Jayanta Mardi")
        self.email = self._extract_field(content, r"\*\*Email:\*\*.*?\(mailto:(.+?)\)", "jayantaofficial84@gmail.com")
        self.phone = self._extract_field(content, r"\*\*Phone:\*\*\s*(.+)", "+91-9083655784")
        self.location = self._extract_field(content, r"\*\*Location:\*\*\s*(.+)", "Kolkata, India")
        self.current_role = self._extract_field(content, r"\*\*Current Role:\*\*\s*(.+)", "Full Stack / Backend Developer (.NET Core)")
        self.experience = self._extract_field(content, r"\*\*Experience:\*\*\s*(.+)", "~1+ Year")
        
        self.portfolio = self._extract_field(content, r"\*\*Portfolio:\*\*.*?\[(.+?)\]", "https://jayanta-github-io.vercel.app/")
        self.github = self._extract_field(content, r"\*\*GitHub:\*\*.*?\[(.+?)\]", "https://github.com/jayantajm1")
        self.linkedin = self._extract_field(content, r"\*\*LinkedIn:\*\*.*?\((.+?)\)", "https://linkedin.com/in/jayantajm")

        # Extract cover letter template
        self._extract_cover_letter()
        
        # Extract Q&A bank
        self._extract_qa_bank()

    def _extract_field(self, content: str, pattern: str, default: str = "N/A") -> str:
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
        return default

    def _extract_cover_letter(self):
        """Extract cover letter template."""
        pattern = r"# ✉️ 5\. Cover Letter Template\n\n(.+?)(?=---|\Z)"
        match = re.search(pattern, self.raw_content, re.DOTALL)
        self.cover_letter_template = match.group(1).strip() if match else ""

    def _extract_qa_bank(self):
        """Extract Q&A bank section."""
        pattern = r"# 🧠 6\. Job Application Q&A Bank\n\n(.+?)(?=---|\Z)"
        match = re.search(pattern, self.raw_content, re.DOTALL)
        
        self.qa_bank = {}
        if match:
            qa_content = match.group(1)
            # Split by ## (subheadings)
            questions = re.split(r"## ", qa_content)[1:]  # skip first empty
            for q_section in questions:
                lines = q_section.split("\n", 1)
                if len(lines) == 2:
                    question = lines[0].strip()
                    answer = lines[1].strip()
                    self.qa_bank[question] = answer

    def get_cover_letter(self, job_title: str = "[Role]", company_name: str = "[Company]", 
                        custom_reason: str = None) -> str:
        """Generate personalized cover letter."""
        letter = self.cover_letter_template
        letter = letter.replace("[Role]", job_title)
        letter = letter.replace("[Company]", company_name)
        
        if custom_reason:
            letter = letter.replace(
                "I am particularly interested in this role because [custom reason].",
                f"I am particularly interested in this role because {custom_reason}."
            )
        
        return letter

    def get_answer(self, question: str) -> str:
        """Get pre-written answer for a common question."""
        for key, answer in self.qa_bank.items():
            if key.lower() in question.lower() or question.lower() in key.lower():
                return answer
        return "Not found in Q&A bank. Please provide manually."

    def get_profile_summary(self) -> str:
        """Return formatted profile summary."""
        return f"""
╔══════════════════════════════════════════════════════════════════════╗
║                     CANDIDATE PROFILE                                 ║
╠══════════════════════════════════════════════════════════════════════╣
║ Name              : {self.name}
║ Email             : {self.email}
║ Phone             : {self.phone}
║ Location          : {self.location}
║ Current Role      : {self.current_role}
║ Experience        : {self.experience}
║ GitHub            : {self.github}
║ Portfolio         : {self.portfolio}
╚══════════════════════════════════════════════════════════════════════╝
"""

    def to_dict(self) -> dict:
        """Export profile as dictionary."""
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "location": self.location,
            "current_role": self.current_role,
            "experience": self.experience,
            "github": self.github,
            "portfolio": self.portfolio,
            "linkedin": self.linkedin,
        }
