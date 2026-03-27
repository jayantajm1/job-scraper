# QUICK REFERENCE GUIDE - Auto-Apply Features

## One-Liner Commands

### FASTEST: Auto-Apply Everything
```bash
python auto_apply.py dotnet_jobs_*.xlsx
```
Applies to ALL jobs in the file without any prompts.

### SAFE: Auto-Apply Limited Batch
```bash
python auto_apply.py dotnet_jobs_*.xlsx 20
```
Applies to first 20 jobs automatically.

### INTERACTIVE: Review Each Job
```bash
python apply_jobs.py dotnet_jobs_*.xlsx interactive 10
```
Shows each job; you review cover letter and confirm.

### HYBRID: After Scrape
```bash
python dotnet_job_scraper.py
# Then choose: interactive/auto/skip
```

---

## Common Workflows

### Workflow 1: Scrape + Auto-Apply
```bash
$env:NO_PROXY='*'
python dotnet_job_scraper.py
# Choose "auto" mode
# Done!
```
**Time:** ~5 minutes for 40 jobs

---

### Workflow 2: Scrape, Then Apply Later
```bash
# Day 1: Scrape
$env:NO_PROXY='*'
python dotnet_job_scraper.py
# Choose "skip"

# Day 2: Apply (after reviewing jobs)
python auto_apply.py dotnet_jobs_*.xlsx 30
```
**Time:** Flexible scheduling

---

### Workflow 3: Test Then Scale
```bash
# Test with 5 jobs
python apply_jobs.py dotnet_jobs_*.xlsx auto 5
# Check Excel and confirm

# Then apply to 50 more
python apply_jobs.py dotnet_jobs_*.xlsx auto 50
```
**Time:** 3 min test + 3 min for 50 jobs

---

### Workflow 4: Mixed (Some Interactive + Some Auto)
```bash
# First 10 with review
python apply_jobs.py dotnet_jobs_*.xlsx interactive 10

# Next 50 automatically
python apply_jobs.py dotnet_jobs_*.xlsx auto 50
```
**Time:** 20 min interactive + 3 min auto

---

## What Gets Applied

When you run auto-apply, for each job:

✅ Generates personalized cover letter  
✅ Uses your profile from `mydetail.md`  
✅ Marks "Apply Status" = Applied  
✅ Records timestamp  
✅ Sets Resume = "Default"  
✅ Sets Method = "Auto-Applied"  
✅ Updates Excel instantly  

---

## Checking Progress

### In Terminal
- See job number, company, title as it processes
- Count of applied jobs updates in real-time

### In Excel
Sort/filter by "Apply Status":
- **Applied** = Green (✓ completed)
- **Not Applied** = White (pending)

Columns updated:
- Apply Status
- Applied DateTime
- Resume Version
- Cover Letter Version
- Application Method

---

## Customization

### Change Default Answers
Edit `mydetail.md`:
- Q&A Bank section
- Cover Letter Template
- Profile information

### Change Resume Version
Edit `apply_jobs.py` line 35:
```python
resume_version="Default"  # Change to "Backend" or other version
```

### Limit Applications Per Day
Edit `auto_apply.py`:
```python
max_apps = 50  # Apply max 50 per day
```

---

## Safety Features

✅ Profile must exist (`mydetail.md`)  
✅ Excel file must exist  
✅ Interactive mode for first applications  
✅ All applications logged in Excel  
✅ Can pause between batches  
✅ Manual review possible anytime  

---

## Summary Table

| Task | Command | Time | Mode |
|------|---------|------|------|
| Quick 10 jobs | `python auto_apply.py jobs.xlsx 10` | 1 min | Auto |
| 50 jobs batch | `python auto_apply.py jobs.xlsx 50` | 3 min | Auto |
| Review + apply 5 | `python apply_jobs.py jobs.xlsx interactive 5` | 10 min | Interactive |
| All jobs | `python auto_apply.py jobs.xlsx` | 5 min | Auto |
| Scrape + apply | `python dotnet_job_scraper.py` | 10 min | Choice |

---

## Troubleshooting

### No Excel file found
```bash
python dotnet_job_scraper.py  # Scrape first
```

### Profile not found
Make sure `mydetail.md` exists in same folder

### Want to change cover letter
Edit `mydetail.md` → section 5

### Want to stop auto-apply mid-run
Press Ctrl+C in terminal (will save progress)

---

## Stats After Running

Terminal will show:
```
Successfully Applied: 45
Failed: 0
Total Processed: 45

Overall Stats:
  Total Jobs: 100
  Applied: 87
  Not Applied: 13
```

Open Excel file to see full tracking!
