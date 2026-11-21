import re

DEFAULT_SKILLS: list[str] = [
    "python",
    "sql",
    "pandas",
    "numpy",
    "scikit-learn",
    "machine learning",
    "deep learning",
    "nlp",
    "llm",
    "rag",
    "data analysis",
    "data visualization",
    "exploratory data analysis",
    "eda",
    "power bi",
    "tableau",
    "git",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "flask",
    "fastapi",
    "rest api",
]


def extract_skills(text: str, skills: list[str] | None = None) -> list[str]:
    """Return sorted unique skills found in the given text."""
    skill_pool = skills if skills is not None else DEFAULT_SKILLS
    normalized_text = text.lower()
    found: set[str] = set()

    for skill in skill_pool:
        target = skill.lower().strip()
        if not target:
            continue
        pattern = r"(?<!\w)" + re.escape(target) + r"(?!\w)"
        if re.search(pattern, normalized_text):
            found.add(target)

    return sorted(found)