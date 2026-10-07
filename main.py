from src.read_file import read_file
from src.preprocess import preprocess_text
from src.similarity import calculate_similarity
from src.predict_model import predict_category
from src.skill_match import compare_skills
from src.suggestion import generate_suggestions

resume = read_file("data/resume.txt")
job_description = read_file("data/job_description.txt")


if resume is not None and job_description is not None:

    # ---------- Preprocessing ----------
    clean_resume = preprocess_text(resume)
    clean_job = preprocess_text(job_description)

    # ---------- Resume Match ----------
    score = calculate_similarity(
        clean_resume,
        clean_job
    )

    # ---------- Resume Category ----------
    category = predict_category(resume)

    # ---------- Skill Matching ----------
    matched, missing = compare_skills(
        resume,
        job_description
    )
    suggestions = generate_suggestions(missing)
    # ---------- Output ----------
    print("=" * 50)

    print(f"Resume Match Score : {score}%")

    print(f"Predicted Category : {category}")

    print("=" * 50)

    print("\nMatched Skills")

    if matched:
        for skill in sorted(matched):
            print(f"✔ {skill}")
    else:
        print("No matched skills found.")

    print("\nMissing Skills")

    if missing:
        for skill in sorted(missing):
            print(f"✖ {skill}")
    else:
        print("No missing skills.")

    print("=" * 50)
    print("\nSuggestions")

    if suggestions:

        for suggestion in suggestions:
            print(f"• {suggestion}")

    else:
        print("Your resume already covers the required skills.")