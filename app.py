from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import shutil
import os

from src.file_reader import extract_text
from src.preprocess import preprocess_text
from src.predict_model import predict_category
from src.similarity import calculate_similarity
from src.skill_match import compare_skills
from src.suggestion import generate_suggestions


app = FastAPI(
    title="ResumeMatch AI",
    description="NLP-powered Resume and Job Description Matching System",
    version="1.0"
)


# Serve frontend
app.mount(
    "/static",
    StaticFiles(directory="frontend"),
    name="static"
)


@app.get("/")
def home():
    return FileResponse("frontend/index.html")


@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):

    # --------------------------------------------------
    # 1. Validate uploaded file
    # --------------------------------------------------

    if not resume.filename:
        return {"error": "Please upload a resume."}

    extension = resume.filename.split(".")[-1].lower()

    if extension not in ["pdf", "txt"]:
        return {
            "error": "Only PDF and TXT files are supported."
        }


    # --------------------------------------------------
    # 2. Save uploaded resume
    # --------------------------------------------------

    os.makedirs("data/uploads", exist_ok=True)

    safe_filename = os.path.basename(resume.filename)

    file_path = os.path.join(
        "data",
        "uploads",
        safe_filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)


    # --------------------------------------------------
    # 3. Extract resume text
    # --------------------------------------------------

    resume_text = extract_text(file_path)

    if not resume_text.strip():
        return {
            "error": "Could not extract text from the resume."
        }


    # --------------------------------------------------
    # 4. NLP preprocessing
    # --------------------------------------------------

    clean_resume = preprocess_text(resume_text)

    clean_job = preprocess_text(job_description)


    # --------------------------------------------------
    # 5. Calculate NLP content similarity
    # --------------------------------------------------

    content_similarity = calculate_similarity(
        clean_resume,
        clean_job
    )


    # --------------------------------------------------
    # 6. Extract and compare skills
    # --------------------------------------------------

    matched, missing = compare_skills(
        resume_text,
        job_description
    )


    # --------------------------------------------------
    # 7. Calculate skill coverage
    # --------------------------------------------------

    total_required_skills = len(matched) + len(missing)

    if total_required_skills > 0:

        skill_coverage = (
            len(matched) / total_required_skills
        ) * 100

    else:

        skill_coverage = 0


    skill_coverage = round(skill_coverage, 2)


    # --------------------------------------------------
    # 8. Calculate overall match score
    #
    # 60% = required skill coverage
    # 40% = NLP content similarity
    # --------------------------------------------------

    overall_score = (
        (skill_coverage * 0.60)
        +
        (content_similarity * 0.40)
    )

    overall_score = round(
        min(overall_score, 100),
        2
    )


    # --------------------------------------------------
    # 9. Predict resume category
    # --------------------------------------------------

    category = predict_category(resume_text)


    # --------------------------------------------------
    # 10. Generate suggestions
    # --------------------------------------------------

    suggestions = generate_suggestions(missing)


    # --------------------------------------------------
    # 11. Return complete analysis
    # --------------------------------------------------

    return {

        "match_score": overall_score,

        "content_similarity": round(
            content_similarity,
            2
        ),

        "skill_coverage": skill_coverage,

        "predicted_category": category,

        "matched_skills": sorted(
            list(matched)
        ),

        "missing_skills": sorted(
            list(missing)
        ),

        "suggestions": suggestions
    }