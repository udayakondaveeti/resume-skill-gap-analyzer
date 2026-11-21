SKILL_ACTION_TIPS: dict[str, str] = {
    "python": "Build an end-to-end data pipeline or automation script in Python and link the GitHub repo.",
    "pandas": "Showcase data cleaning, merging, and aggregation workflows using Pandas on a real dataset.",
    "numpy": "Highlight vectorized numerical computations or statistical modeling with NumPy.",
    "scikit-learn": "Add a supervised/unsupervised ML project featuring train/test splits, pipelines, and evaluation metrics.",
    "machine learning": "Document model selection, feature engineering, and validation results (e.g., F1, RMSE, ROC-AUC).",
    "exploratory data analysis": "Include an EDA case study uncovering key trends, outliers, and actionable insights.",
    "data visualization": "Embed clear charts/dashboards (Matplotlib, Seaborn, or Power BI) that tell a story with metrics.",
    "fastapi": "Wrap a trained model or analytics query in a FastAPI service with request validation.",
    "flask": "Build a lightweight Flask web app or REST endpoint to serve predictions or reports.",
    "rest api": "Demonstrate consuming or building RESTful APIs with proper status codes and JSON payloads.",
    "git": "Maintain clean commit history, feature branches, and a well-documented README on GitHub.",
}


def generate_recommendations(missing_skills: list[str]) -> str:
    """Generate tailored, actionable resume improvement recommendations."""
    if not missing_skills:
        return (
            "Strong skill alignment! Focus on quantifying impact and measurable "
            "outcomes in your project bullet points."
        )

    lines = [
        f"Priority Gaps ({len(missing_skills)} skills): {', '.join(missing_skills)}",
        "",
        "Actionable Next Steps:",
    ]
    for skill in missing_skills:
        tip = SKILL_ACTION_TIPS.get(
            skill,
            f"Add a hands-on project or bullet point demonstrating applied {skill} with measurable outcomes.",
        )
        lines.append(f"- {skill}: {tip}")

    return "\n".join(lines)