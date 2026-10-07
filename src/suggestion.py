def generate_suggestions(missing_skills):
    """
    Generate practical suggestions based on missing skills.
    """

    if not missing_skills:
        return [
            "Your resume covers the main skills detected in the job description.",
            "Consider adding measurable achievements to strengthen your resume."
        ]

    suggestions = []

    for skill in sorted(missing_skills):

        suggestions.append(
            f"Consider adding relevant experience or projects related to {skill}."
        )

    return suggestions