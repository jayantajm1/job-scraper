#!/usr/bin/env python
"""
Quick Test/Demo Script
======================
Tests all components of the job application automation system.
"""

from profile import CandidateProfile
from cover_letter_gen import CoverLetterGenerator
from application_tracker import ApplicationTracker
import os

def test_profile():
    print("\n" + "="*70)
    print("TEST 1: Profile Loading")
    print("="*70)
    p = CandidateProfile("mydetail.md")
    print(p.get_profile_summary())
    print(f"[OK] Loaded {len(p.qa_bank)} Q&A answers")
    print(f"[OK] Loaded cover letter template ({len(p.cover_letter_template)} chars)")
    return p

def test_cover_letter(profile):
    print("\n" + "="*70)
    print("TEST 2: Cover Letter Generation")
    print("="*70)
    gen = CoverLetterGenerator(profile)
    
    # Test 1: Microservices role
    jd1 = "We need a senior backend developer with ASP.NET Core, microservices, and PostgreSQL expertise"
    letter1 = gen.generate("TechCorp", "Senior Backend Engineer", jd1)
    print(f"[OK] Generated cover letter for TechCorp (microservices role)")
    print(f"   Length: {len(letter1)} characters")
    
    # Test 2: Full Stack role
    jd2 = "Full Stack Developer with Angular and ASP.NET Core needed"
    letter2 = gen.generate("StartupXYZ", "Full Stack Developer", jd2)
    print(f"[OK] Generated cover letter for StartupXYZ (full stack role)")
    print(f"   Length: {len(letter2)} characters")
    
    # Test 3: Cloud role
    jd3 = "Azure cloud engineer with Docker and Kubernetes required"
    letter3 = gen.generate("CloudCo", "Cloud Engineer", jd3)
    print(f"[OK] Generated cover letter for CloudCo (cloud role)")
    print(f"   Length: {len(letter3)} characters")

def test_qa_bank(profile):
    print("\n" + "="*70)
    print("TEST 3: Q&A Bank Lookups")
    print("="*70)
    
    questions = [
        "Tell me about yourself",
        "Why do you want this role?",
        ".NET experience",
        "Relocation",
    ]
    
    for q in questions:
        answer = profile.get_answer(q)
        print(f"Q: {q}")
        print(f"A: {answer[:80]}...")
        print()

def test_tracker():
    print("\n" + "="*70)
    print("TEST 4: Application Tracker")
    print("="*70)
    
    # Find an existing Excel file
    excel_files = [f for f in os.listdir(".") if f.endswith(".xlsx")]
    if excel_files:
        test_file = excel_files[0]
        print(f"Using test file: {test_file}")
        
        tracker = ApplicationTracker(test_file)
        print("[OK] Tracker initialized")
        
        # Add tracking columns if needed
        tracker.add_tracking_columns()
        print("[OK] Tracking columns added/verified")
        
        # Get stats
        stats = tracker.get_application_stats()
        print(f"[OK] Application Stats:")
        for key, val in stats.items():
            print(f"   {key}: {val}")
    else:
        print("[NOTE] No Excel file found for testing. Run scraper first.")

def main():
    print("\n" + "="*70)
    print("TEST: JOB APPLICATION AUTOMATION - SYSTEM TEST")
    print("="*70)
    
    try:
        # Run all tests
        profile = test_profile()
        test_cover_letter(profile)
        test_qa_bank(profile)
        test_tracker()
        
        print("\n" + "="*70)
        print("[OK] ALL TESTS PASSED!")
        print("="*70)
        print("\nYou're ready to use the job application system:")
        print("  1. python dotnet_job_scraper.py       Scrape + apply")
        print("  2. python apply_jobs.py <excel_file>  Apply to existing jobs")
        print("\nRead README.md for full documentation.")
        
    except Exception as e:
        print(f"\n[ERROR] TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
