import argparse
import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

try:
    from docx import Document
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

try:
    from sklearn.metrics.pairwise import cosine_similarity
    from sentence_transformers import SentenceTransformer
    HAS_SBERT = True
except ImportError:
    HAS_SBERT = False

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


COMMON_SKILLS = [
    "python", "sql", "machine learning", "deep learning", "nlp",
    "natural language processing", "large language models", "llm",
    "transformers", "pytorch", "tensorflow", "scikit-learn", "pandas",
    "numpy", "data analysis", "data visualization", "git", "docker",
    "kubernetes", "aws", "azure", "gcp", "fastapi", "flask", "rest api",
    "rag", "embeddings", "vector database", "prompt engineering", "mlops"
]


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def load_text_from_file(file_path: str) -> str:
    """Loads text from a .pdf, .docx, or .txt file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = path.suffix.lower()

    if suffix == ".pdf":
        if not HAS_PYPDF:
            raise ImportError(
                "PDF support requires 'pypdf'. Install it with: pip install pypdf"
            )
        reader = PdfReader(str(path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages).strip()

    if suffix == ".docx":
        if not HAS_DOCX:
            raise ImportError(
                "Word (.docx) support requires 'python-docx'. "
                "Install it with: pip install python-docx"
            )
        doc = Document(str(path))
        parts = [p.text for p in doc.paragraphs if p.text.strip()]
        for table in doc.tables:
            for row in table.rows:
                row_text = " | ".join(
                    cell.text.strip() for cell in row.cells if cell.text.strip()
                )
                if row_text:
                    parts.append(row_text)
        return "\n".join(parts).strip()

    return path.read_text(encoding="utf-8", errors="ignore").strip()


def extract_skills(text: str, skill_vocab: List[str] = COMMON_SKILLS) -> List[str]:
    cleaned = normalize_text(text)
    found = []
    for skill in skill_vocab:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, cleaned):
            found.append(skill)
    return sorted(set(found))


def compute_semantic_similarity(resume_text: str, jd_text: str) -> Tuple[float, str]:
    """Computes semantic similarity (0 to 100%) using Sentence-BERT if available."""
    if HAS_SBERT:
        model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = model.encode([resume_text, jd_text])
        score = float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0])
        percentage = round(max(0.0, min(1.0, score)) * 100, 2)
        return percentage, "Sentence-BERT (all-MiniLM-L6-v2)"

    resume_tokens = set(re.findall(r"[a-z0-9+#.-]+", resume_text.lower()))
    jd_tokens = set(re.findall(r"[a-z0-9+#.-]+", jd_text.lower()))
    if not jd_tokens:
        return 0.0, "Fallback Token Overlap"
    overlap = len(resume_tokens & jd_tokens) / len(jd_tokens)
    return round(min(1.0, overlap) * 100, 2), "Fallback Token Overlap"


def analyze_skill_gap(resume_text: str, jd_text: str) -> Dict:
    resume_skills = extract_skills(resume_text)
    required_skills = extract_skills(jd_text)

    resume_set = set(resume_skills)
    required_set = set(required_skills)

    matched_skills = sorted(resume_set & required_set)
    missing_skills = sorted(required_set - resume_set)
    extra_skills = sorted(resume_set - required_set)

    similarity_score, method_used = compute_semantic_similarity(resume_text, jd_text)

    coverage_pct = (
        round((len(matched_skills) / len(required_set)) * 100, 2)
        if required_set
        else 100.0
    )

    return {
        "similarity_score_pct": similarity_score,
        "skill_coverage_pct": coverage_pct,
        "method_used": method_used,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills,
    }


def generate_llm_feedback(resume_text: str, jd_text: str, analysis: Dict) -> str:
    """Uses an LLM when OPENAI_API_KEY is configured; otherwise returns rule-based guidance."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or not HAS_OPENAI:
        if not analysis["missing_skills"]:
            return "Strong skill alignment detected. Quantify project impact and metrics in your resume."
        missing_str = ", ".join(analysis["missing_skills"])
        return (
            f"Focus on adding hands-on projects or experience demonstrating: {missing_str}. "
            "Highlight measurable outcomes alongside matched technical skills."
        )

    client = OpenAI(api_key=api_key)
    prompt = f"""
You are a technical career coach. Analyze this candidate resume against the job description.

Semantic Similarity Score: {analysis['similarity_score_pct']}%
Skill Coverage: {analysis['skill_coverage_pct']}%
Matched Skills: {', '.join(analysis['matched_skills']) or 'None'}
Missing Skills (Skill Gaps): {', '.join(analysis['missing_skills']) or 'None'}

Resume:
{resume_text}

Job Description:
{jd_text}

Provide a concise, actionable skill gap summary and 3 specific resume bullet-point improvements.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze a candidate resume (.pdf, .docx, .txt) against a job description."
    )
    parser.add_argument(
        "--resume",
        type=str,
        help="Path to resume file (.pdf, .docx, or .txt)",
    )
    parser.add_argument(
        "--jd",
        type=str,
        help="Path to job description file (.pdf, .docx, or .txt)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.resume:
        resume_text = load_text_from_file(args.resume)
    else:
        resume_text = """
        Computer Science student experienced in Python, SQL, Pandas, NumPy, and Scikit-learn.
        Built a machine learning classification model and explored basic NLP preprocessing.
        Familiar with Git and REST APIs.
        """

    if args.jd:
        jd_text = load_text_from_file(args.jd)
    else:
        jd_text = """
        Looking for an AI / NLP Engineer with strong Python, NLP, Large Language Models (LLM),
        RAG, embeddings, PyTorch, Docker, and SQL skills. Experience deploying ML/NLP services
        and evaluating semantic similarity is a plus.
        """

    report = analyze_skill_gap(resume_text, jd_text)
    feedback = generate_llm_feedback(resume_text, jd_text, report)

    print("=== Resume & Skill Gap Analysis Report ===")
    print(f"Scoring Method       : {report['method_used']}")
    print(f"Semantic Similarity  : {report['similarity_score_pct']}%")
    print(f"Required Skill Match : {report['skill_coverage_pct']}%")
    print(f"Matched Skills       : {', '.join(report['matched_skills']) or 'None'}")
    print(f"Missing Skills (Gaps): {', '.join(report['missing_skills']) or 'None'}")
    print(f"Additional Skills    : {', '.join(report['extra_skills']) or 'None'}")
    print("\n=== Recommendations ===")
    print(feedback)


if __name__ == "__main__":
    main()