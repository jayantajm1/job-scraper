# 🚀 Job Application Automation Workflow

Complete automated job scraper + intelligent applicant assistant

---

## � Quick Start

### 1. Setup Environment Variable (One-time)
```powershell
$env:NO_PROXY='*'
$env:no_proxy='*'
```

### 2. Run Scraper + Apply
```bash
python dotnet_job_scraper.py
```

You'll get a prompt to choose mode:
- **interactive** - Review each job before applying
- **auto** - Auto-apply to all jobs without review
- **skip** - Just scrape, don't apply

### 3. Apply to Existing Jobs (Standalone)

**Interactive Mode:**
```bash
python apply_jobs.py dotnet_jobs_20260327_084640.xlsx interactive 10
```

**Auto Mode:**
```bash
python apply_jobs.py dotnet_jobs_20260327_084640.xlsx auto 20
```

**Quick Auto-Apply Script:**
```bash
python auto_apply.py dotnet_jobs_20260327_084640.xlsx 30
```

---

## 📁 Project Structure

```
.
├── dotnet_job_scraper.py       # Main scraper + application coordinator
├── apply_jobs.py                # Apply with choice of interactive/auto mode
├── auto_apply.py                # Quick auto-apply without options
├── profile.py                   # Load candidate details from mydetail.md
├── cover_letter_gen.py          # Generate personalized cover letters
├── application_tracker.py       # Track application status in Excel
├── apply_engine.py              # Core application flow (interactive + auto)
├── test_system.py               # Validate all modules
├── mydetail.md                  # Your profile, Q&A, links (EDIT THIS)
├── Jayanta_Mardi_December_2025.pdf  # Your resume
└── dotnet_jobs_*.xlsx           # Generated job listings
```

---

## 🔧 Configuration

### Update Your Profile: `mydetail.md`

Edit this file with:
- ✅ Name, Email, Phone
- ✅ Experience Level & Tech Stack
- ✅ Portfolio, GitHub, LinkedIn Links
- ✅ Cover Letter Template (customizable)
- ✅ Q&A Bank (common interview questions)

### Update Resume Versions (Optional)

Place your resume PDFs in the project folder:
```
Resume_DotNet_Backend_v1.pdf
Resume_FullStack_DotNet_Angular_v1.pdf
Resume_Cloud_Azure_DotNet_v1.pdf
```

---

## 🎯 Application Workflow

### What Happens When You Apply:

1. **Job Display** - Shows title, company, salary, description
2. **Cover Letter Review** - AI-generated, personalized cover letter based on job description
3. **Q&A Guidelines** - Shows pre-written answers to common questions
4. **Custom Answers** - Prompt to answer application-specific questions
5. **Link Opening** - Option to open job link in browser
6. **Confirmation** - Confirm when you've submitted the application
7. **Excel Update** - Job marked as "Applied" with timestamp

---

## ⚡ Application Modes

### Mode 1: Interactive (Default)
- Review each job before applying
- Customize cover letter if needed
- Answer application-specific questions
- Best for: **Careful, high-quality applications**

```bash
python apply_jobs.py dotnet_jobs_*.xlsx interactive 10
```

What you control:
- ✅ Preview cover letter
- ✅ Yes/No on each application
- ✅ Custom answers per job
- ✅ Recruiter info collection

### Mode 2: Auto-Apply (NEW)
- Automatically applies to jobs without prompts
- Generates cover letter automatically
- Marks job as applied instantly
- Best for: **Rapid bulk applications**

```bash
python auto_apply.py dotnet_jobs_*.xlsx 50
# or
python apply_jobs.py dotnet_jobs_*.xlsx auto 50
```

What's automated:
- ✅ Cover letter generated automatically
- ✅ Standard answers used
- ✅ All jobs applied in sequence
- ✅ Excel tracking updated instantly
- ✅ Progress shown in real-time

### Choosing Your Mode

| Criteria | Interactive | Auto |
|----------|-------------|------|
| Speed | Slow (1-2 min per job) | Fast (5-10 sec per job) |
| Customization | Full | Limited |
| Control | Complete | Automatic |
| Best For | Quality focus | Volume/speed |
| Resume | Choose per job | Default always |
| Cover Letter | Review each | Auto-generated |

---

## 💡 How to Use Auto-Apply

### Step 1: Scrape Jobs First
```bash
$env:NO_PROXY='*'
python dotnet_job_scraper.py
# Generates: dotnet_jobs_20260327_XXXXXX.xlsx
```

### Step 2: Auto-Apply Immediately
```bash
python auto_apply.py dotnet_jobs_20260327_XXXXXX.xlsx 50
```

**That's it!** The system will:
- ✅ Load your profile from `mydetail.md`
- ✅ Generate personalized cover letters for each job
- ✅ Mark 50 jobs as "Applied" automatically
- ✅ Update Excel with timestamps
- ✅ Show progress in terminal

### Step 3: Monitor Progress
Open the Excel file to see:
- Apply Status: "Applied" (Green)
- Applied DateTime: Timestamp
- Resume Version: "Default"
- Cover Letter: "Auto-Generated"

---

## 📊 Large Scale Batch Examples

### Apply to 100 Jobs Automatically
```bash
python auto_apply.py dotnet_jobs_*.xlsx 100
```

### Apply Across Multiple Scraped Files
```bash
python auto_apply.py dotnet_jobs_20260327_*.xlsx 200
```

### Quick 5-Job Test (Verify System)
```bash
python apply_jobs.py dotnet_jobs_*.xlsx auto 5
```

---

### Excel Tracking Columns

After applying, these columns are automatically updated:

| Column | Purpose |
|--------|---------|
| Apply Status | Not Applied / Draft Ready / Applied / Skipped / Failed |
| Applied DateTime | When you applied (auto-filled) |
| Resume Version | Which resume version you used |
| Cover Letter | Generated / Custom (auto-filled) |
| Application Method | External Site / LinkedIn / Indeed (you choose) |
| Recruiter | Recruiter name if mentioned |
| Follow-up Date | When to follow up |

---

## 💡 How Cover Letters Work

The system intelligently matches job descriptions to your background:

1. **Extracts Keywords** from job description (C#, ASP.NET Core, Docker, etc.)
2. **Matches Your Experience** - Highlights relevant skills you have
3. **Personalizes Content** - Adapts reasons to fit specific company/role
4. **Keeps It Professional** - Uses your provided template as base

---

## 🤖 Interactive Mode Features

### During Application:
- ✅ Preview cover letter before use
- ✅ Option to skip or customize any section
- ✅ Browser link opens automatically
- ✅ Confirm after you've submitted
- ✅ Add notes/recruiter information
- ✅ Manual pause/resume between applications

### Controls:
```
yes/y     → Proceed with action
no/n      → Reject/Skip action
skip/s    → Skip this job entirely
Enter     → Use suggested answer (if applicable)
```

---

## 📊 Tracking & Reports

View your application stats in Excel:
- **All Jobs Sheet** - Complete job listings with application status
- **Summary Sheet** - Statistics and metrics
- **Per-Source Sheets** - LinkedIn, Indeed, Glassdoor breakdowns
- **Application Status** - Color-coded cell backgrounds

---

## ⚡ Pro Tips

### Batch Processing
```bash
# Apply to first 5 jobs (test run)
python apply_jobs.py dotnet_jobs_*.xlsx auto 5

# Apply to first 50 jobs
python apply_jobs.py dotnet_jobs_*.xlsx auto 50

# Apply to ALL jobs in file
python auto_apply.py dotnet_jobs_*.xlsx
```

### Mixed Strategy (RECOMMENDED)
1. **First 10 jobs**: Use interactive mode to customize
   ```bash
   python apply_jobs.py dotnet_jobs_*.xlsx interactive 10
   ```

2. **Remaining jobs**: Use auto-mode for speed
   ```bash
   python apply_jobs.py dotnet_jobs_*.xlsx auto 40
   ```

### Auto-Apply Best Practices
- ✅ Test with 5-10 jobs first
- ✅ Review your `mydetail.md` before auto-apply
- ✅ Check Excel after first 10 to verify format
- ✅ Use for jobs with similar JD requirements
- ✅ Monitor application status regularly

### When to Use Auto-Apply
- ✅ Applying to 50+ similar jobs
- ✅ Volume > quality is your goal
- ✅ You've already customized key experiences
- ✅ You want rapid job market coverage

### When to Use Interactive
- ✅ First few applications (quality check)
- ✅ Highly customized roles
- ✅ Dream company applications
- ✅ Limited number of targets

---

## 🔐 Security & Best Practices

✅ **API Token** - Keep your Apify token private (already in code)
✅ **Resumes** - Store sensitive docs locally, never in repo
✅ **Rate Limiting** - Script includes pauses between applications (respect platform ToS)
✅ **Manual Review** - Every application requires your review before submission
✅ **Tracking** - All applications tracked in Excel for reference

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'openpyxl'"
```bash
$env:NO_PROXY='*'
pip install openpyxl
```

### "mydetail.md not found"
Make sure you've created/updated `mydetail.md` with your profile

### Cover letter looks generic
Update your profile with more specific achievements and keywords

### No jobs scraped
- Check your Apify API token
- Verify internet connection
- Try disabling Windows proxy:
  ```powershell
  $env:NO_PROXY='*'
  ```

---

## 📚 What Gets Scraped

Jobs are collected from:
1. **LinkedIn Jobs** (via Apify)
2. **Indeed.com** (via Apify)
3. **Glassdoor.com** (via Apify)

Each listing includes:
- Job title, company, location
- Job type (Full-time, Contract, etc.)
- Experience level required
- Salary range (if available)
- Job description
- Direct apply link

---

## 🎓 Next Steps

1. ✅ Update `mydetail.md` with your info
2. ✅ Place your resume PDF in the folder
3. ✅ Run `python dotnet_job_scraper.py`
4. ✅ Choose to scrape + apply interactively
5. ✅ Review each job/cover letter carefully
6. ✅ Check Excel file for application tracking

---

## 📞 Support

If you encounter issues:
1. Check this README
2. Review error messages in terminal
3. Ensure all dependencies are installed:
   ```bash
   pip install requests openpyxl
   ```
4. Verify your profile is correctly formatted in `mydetail.md`

---

**Happy job hunting! 🎉**
