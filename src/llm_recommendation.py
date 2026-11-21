def generate_recommendations(missing_skills: list[str]) -> str:
    """Generate actionable resume improvement tips based on missing skills."""
    if not missing_skills:
        return (
            "Strong skill alignment! Focus on quantifying impact and measurable "
            "outcomes in your project bullet points."
        )

    skills_str = ", ".join(missing_skills)
    return (
        f"Focus on adding hands-on projects or experience demonstrating: {skills_str}. "
        "Highlight measurable outcomes alongside matched technical skills."
    )