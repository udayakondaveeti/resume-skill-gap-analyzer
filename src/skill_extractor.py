import re

SKILL_ALIASES: dict[str, str] = {
    "eda": "exploratory data analysis",
    "ml": "machine learning",
    "dl": "deep learning",
    "natural language processing": "nlp",
    "large language models": "llm",
    "retrieval augmented generation": "rag",
    "restful api": "rest api",
    "rest apis": "rest api",
    "powerbi": "power bi",
    "sklearn": "scikit-learn",
}

DEFAULT_SKILLS: list[str] = [
    "python",
    "sql",
    "pandas",
    "numpy",
    "scikit-learn",
    "sklearn",
    "machine learning",
    "ml",
    "deep learning",
    "dl",
    "nlp",
    "natural language processing",
    "llm",
    "large language models",
    "rag",
    "retrieval augmented generation",
    "data analysis",
    "data visualization",
    "exploratory data analysis",
    "eda",
    "power bi",
    "powerbi",
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
    "restful api",
    "rest apis",
]


def extract_skills(text: str, skills: list[str] | None = None) -> list[str]:
    """Return sorted unique canonical skills found in the given text."""
    skill_pool = skills if skills is not None else DEFAULT_SKILLS
    normalized_text = text.lower()
    found: set[str] = set()

    for skill in skill_pool:
        target = skill.lower().strip()
        if not target:
            continue
        pattern = r"(?<!\w)" + re.escape(target) + r"(?!\w)"
        if re.search(pattern, normalized_text):
            canonical = SKILL_ALIASES.get(target, target)
            found.add(canonical)

    return sorted(found)