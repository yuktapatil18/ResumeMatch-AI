# ResumeMatch AI

An NLP-powered Resume and Job Description Matching System that analyzes how well a resume aligns with a specific job description.

The application extracts resume content, identifies relevant technical skills, calculates text similarity using TF-IDF, predicts the candidate's job category using a machine learning model, and provides suggestions based on missing skills.

# Overview

Applying for jobs often means comparing a resume against many different job descriptions.

ResumeMatch AI automates this comparison by analyzing both documents and presenting the results in an easy-to-understand format.

The system provides:

- Overall resume-job match score
- Required skill coverage
- NLP-based content similarity
- Predicted resume category
- Matched technical skills
- Missing skills
- Resume improvement suggestions

The project combines traditional NLP techniques, machine learning and a lightweight web interface.

# Features
# Resume Analysis
Upload a resume in:
- PDF
- TXT
The application extracts the text and processes it for analysis.

# Job Description Analysis
Paste the complete job description into the application.
The system analyzes the job requirements and identifies relevant technical skills.

# Skill Matching
The application compares the technical skills found in the resume with the skills detected in the job description.
It separates them into:
- Matched Skills
- Missing Skills

# Content Similarity
TF-IDF vectorization and cosine similarity are used to measure the textual similarity between the resume and job description.

# Match Score
The overall score combines two factors: text
Overall Match = Skill Coverage × 60% + Content Similarity × 40%