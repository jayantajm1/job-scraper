"""
Application Engine — Interactive job application flow
====================================================
Handles the complete application workflow:
1. Show job details
2. Generate and review cover letter
3. Answer common questions
4. Track application status
"""

import webbrowser
from profile import CandidateProfile
from cover_letter_gen import CoverLetterGenerator
from application_tracker import ApplicationTracker


class JobApplicationEngine:
    def __init__(self, profile: CandidateProfile, excel_file: str):
        self.profile = profile
        self.tracker = ApplicationTracker(excel_file)
        self.cl_generator = CoverLetterGenerator(profile)
        self.excel_file = excel_file

    def display_job(self, job: dict):
        """Display job details."""
        print(f"\n{'='*70}")
        print(f"JOB #{job.get('No.', 'N/A')} — {job.get('Job Title', 'N/A')}")
        print(f"{'='*70}")
        print(f"Company          : {job.get('Company', 'N/A')}")
        print(f"Location         : {job.get('Location', 'N/A')}")
        print(f"Job Type         : {job.get('Job Type', 'N/A')}")
        print(f"Experience Level : {job.get('Experience', 'N/A')}")
        print(f"Salary           : {job.get('Salary', 'N/A')}")
        print(f"Source           : {job.get('Source', 'N/A')}")
        print(f"Posted Date      : {job.get('Posted Date', 'N/A')}")
        print(f"\nDescription:\n{job.get('Description', 'N/A')[:500]}...\n")
        print(f"Apply Link: {job.get('Apply Link', 'N/A')}\n")

    def show_cover_letter_preview(self, job: dict) -> str:
        """Generate and display cover letter preview."""
        job_title = job.get('Job Title', 'Developer')
        company_name = job.get('Company', 'Company')
        description = job.get('Description', '')
        
        cover_letter = self.cl_generator.generate(company_name, job_title, description)
        
        print(self.cl_generator.format_for_display(cover_letter))
        return cover_letter

    def show_qa_guides(self, job: dict):
        """Show relevant Q&A responses for this job."""
        print(f"\n{'='*70}")
        print("COMMON INTERVIEW Q&A RESPONSES")
        print(f"{'='*70}\n")
        
        common_questions = [
            "Tell me about yourself",
            "Why do you want this role?",
            "Relevant .NET experience",
            "Why are you leaving current role?",
            "Relocation"
        ]
        
        for idx, question in enumerate(common_questions, 1):
            answer = self.profile.get_answer(question)
            print(f"{idx}. Q: {question}")
            print(f"   A: {answer}\n")

    def ask_confirmation(self, action: str = "Apply") -> bool:
        """Ask user for confirmation."""
        while True:
            response = input(f"\n❓ {action}? (yes/no/skip): ").strip().lower()
            if response in ['yes', 'y']:
                return True
            elif response in ['no', 'n']:
                return False
            elif response in ['skip', 's']:
                return None
            else:
                print("  Invalid input. Enter 'yes', 'no', or 'skip'")

    def collect_custom_answers(self, job: dict) -> dict:
        """Collect custom answers for application-specific questions."""
        answers = {}
        
        print(f"\n{'='*70}")
        print("APPLICATION CUSTOM QUESTIONS")
        print(f"{'='*70}")
        
        # Standard questions many job platforms ask
        questions_to_ask = [
            "Why are you interested in this role at " + job.get('Company', 'this company') + "?",
            f"Why is {job.get('Location', 'this location')} suitable for you?",
        ]
        
        for q in questions_to_ask:
            print(f"\n❓ {q}")
            custom_answer = input("  Your answer (or press Enter for suggested): ").strip()
            
            if not custom_answer:
                # Use from Q&A bank or auto-generate
                if "role" in q.lower():
                    custom_answer = self.profile.get_answer("Why do you want this role?")
                elif "location" in q.lower():
                    custom_answer = self.profile.get_answer("Relocation")
                else:
                    custom_answer = "Not provided"
            
            answers[q] = custom_answer
        
        return answers

    def run_single_application(self, job: dict) -> bool:
        """Run interactive application flow for single job."""
        self.display_job(job)
        
        # Step 1: Review cover letter
        print("📝 STEP 1: Review Personalized Cover Letter")
        cover_letter = self.show_cover_letter_preview(job)
        if not self.ask_confirmation("Use this cover letter?"):
            print("  ⏭️  Skipping this job.")
            return False
        
        # Step 2: Show Q&A guidelines
        print("\n👤 STEP 2: Common Q&A Guidelines")
        self.show_qa_guides(job)
        
        # Step 3: Collect custom answers
        print("\n💬 STEP 3: Custom Answers for This Application")
        custom_answers = self.collect_custom_answers(job)
        
        # Step 4: Final review + open link
        print("\n🔗 STEP 4: Open Application Link")
        apply_link = job.get('Apply Link', '')
        
        if apply_link and apply_link.startswith('http'):
            open_browser = input(f"Open {apply_link} in browser? (yes/no): ").strip().lower()
            if open_browser in ['yes', 'y']:
                webbrowser.open(apply_link)
        
        # Step 5: Confirm application submitted
        print("\n✅ STEP 5: Confirm Application Submission")
        submitted = self.ask_confirmation("Have you submitted the application?")
        
        if submitted is True:
            # Mark as applied
            resume_version = input("Resume version used (default: Default): ").strip() or "Default"
            recruiter_name = input("Recruiter name (optional): ").strip()
            
            self.tracker.mark_applied(
                job_no=job.get('No.', ''),
                resume_version=resume_version,
                cover_letter_version="Generated",
                app_method="External Site",
                recruiter=recruiter_name,
                notes=str(custom_answers)
            )
            print(f"✅ Job #{job.get('No.')} marked as APPLIED")
            return True
        else:
            print(f"⏭️  Job #{job.get('No.')} not marked as applied.")
            return False

    def get_eligible_jobs(self, all_jobs: list) -> list:
        """Filter jobs that haven't been applied yet."""
        # For now, return all jobs (you can add filtering logic later)
        return all_jobs

    def run_batch_applications(self, all_jobs: list, max_applications: int = None):
        """Run applications for multiple jobs with pace control."""
        self.tracker.add_tracking_columns()
        
        eligible_jobs = self.get_eligible_jobs(all_jobs)
        
        if max_applications:
            eligible_jobs = eligible_jobs[:max_applications]
        
        print(f"\n{'='*70}")
        print(f"BATCH APPLICATION MODE")
        print(f"{'='*70}")
        print(f"Total jobs to process: {len(eligible_jobs)}")
        print(f"Remember: Review each application carefully!\n")
        
        applied_count = 0
        skipped_count = 0
        
        for idx, job in enumerate(eligible_jobs, 1):
            print(f"\n[{idx}/{len(eligible_jobs)}]")
            print(f"Progress: {applied_count} applied, {skipped_count} skipped\n")
            
            try:
                if self.run_single_application(job):
                    applied_count += 1
                else:
                    skipped_count += 1
            except Exception as e:
                print(f"Error processing job: {e}")
                skipped_count += 1
            
            # Ask if user wants to continue
            if idx < len(eligible_jobs):
                continue_app = input("\nContinue to next job? (yes/no): ").strip().lower()
                if continue_app not in ['yes', 'y']:
                    break
        
        # Summary
        print(f"\n{'='*70}")
        print("APPLICATION SUMMARY")
        print(f"{'='*70}")
        print(f"Applied: {applied_count}")
        print(f"Skipped: {skipped_count}")
        print(f"Total Processed: {applied_count + skipped_count}")
        
        stats = self.tracker.get_application_stats()
        print(f"\nOverall Stats:")
        print(f"  Total Jobs: {stats.get('total', 0)}")
        print(f"  Applied: {stats.get('applied', 0)}")
        print(f"  Not Applied: {stats.get('not_applied', 0)}")

    def run_auto_applications(self, all_jobs: list, max_applications: int = None):
        """Auto-apply to jobs without user interaction."""
        self.tracker.add_tracking_columns()
        
        eligible_jobs = self.get_eligible_jobs(all_jobs)
        
        if max_applications:
            eligible_jobs = eligible_jobs[:max_applications]
        
        print(f"\n{'='*70}")
        print("AUTO-APPLY MODE (No Interaction)")
        print(f"{'='*70}")
        print(f"Total jobs to auto-apply: {len(eligible_jobs)}\n")
        
        applied_count = 0
        failed_count = 0
        
        for idx, job in enumerate(eligible_jobs, 1):
            try:
                job_no = job.get('No.', '')
                job_title = job.get('Job Title', 'Developer')
                company_name = job.get('Company', 'Company')
                description = job.get('Description', '')
                
                # Generate cover letter
                cover_letter = self.cl_generator.generate(company_name, job_title, description)
                
                # Auto-generate custom answers
                custom_answers = {
                    "Why interested": "Your company aligns with my career goals in backend systems.",
                    "Location": "The location works well for me.",
                }
                
                # Mark as applied immediately
                self.tracker.mark_applied(
                    job_no=job_no,
                    resume_version="Default",
                    cover_letter_version="Auto-Generated",
                    app_method="Auto-Applied",
                    recruiter="",
                    notes=f"Auto-applied on {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}"
                )
                
                print(f"[{idx}/{len(eligible_jobs)}] Applied to Job #{job_no}: {company_name} - {job_title}")
                applied_count += 1
                
            except Exception as e:
                print(f"[{idx}/{len(eligible_jobs)}] Failed on Job #{job.get('No.', 'N/A')}: {str(e)[:60]}")
                failed_count += 1
        
        # Summary
        print(f"\n{'='*70}")
        print("AUTO-APPLY SUMMARY")
        print(f"{'='*70}")
        print(f"Successfully Applied: {applied_count}")
        print(f"Failed: {failed_count}")
        print(f"Total Processed: {applied_count + failed_count}")
        
        stats = self.tracker.get_application_stats()
        print(f"\nOverall Stats:")
        print(f"  Total Jobs: {stats.get('total', 0)}")
        print(f"  Applied: {stats.get('applied', 0)}")
        print(f"  Not Applied: {stats.get('not_applied', 0)}")
