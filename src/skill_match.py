import re


# Skills that the system can detect
SKILLS = [

    # Programming Languages
    "python",
    "java",
    "c++",
    "c",
    "c#",
    "javascript",
    "typescript",
    "go",
    "rust",
    "php",

    # Java / Backend
    "spring",
    "spring boot",
    "jdbc",
    "hibernate",
    "jpa",
    "maven",
    "gradle",

    # Web / Backend
    "html",
    "css",
    "react",
    "angular",
    "nodejs",
    "node.js",
    "express",
    "flask",
    "django",
    "fastapi",
    "rest api",
    "rest apis",

    # Databases
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "sqlite",
    "oracle",
    "redis",

    # DevOps / Cloud
    "git",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",

    # Data / AI / ML
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "nlp",
    "natural language processing",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "pandas",
    "numpy",

    # Computer Science
    "data structures",
    "algorithms",
    "dsa",
    "oop",
    "object oriented programming",
    "operating systems",
    "computer networks",
    "dbms",
    "database management"
]


def skill_pattern(skill):
    """
    Creates a safe pattern for matching a complete skill.
    Example:
    'java' matches 'Java'
    but does not match 'JavaScript'
    """

    escaped_skill = re.escape(skill)

    return rf"(?<!\w){escaped_skill}(?!\w)"


def extract_skills(text):
    """
    Extract technical skills from resume or job description.
    """

    if not text:
        return []

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        pattern = skill_pattern(skill)

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills


def compare_skills(resume, job_description):
    """
    Compare the skills present in the resume
    with the skills required in the job description.
    """

    resume_skills = set(extract_skills(resume))

    job_skills = set(extract_skills(job_description))

    matched = resume_skills.intersection(job_skills)

    missing = job_skills - resume_skills

    return matched, missing