from dataclasses import dataclass
from typing import List
import numpy as np


@dataclass
class AnalysisResult:
    match_percentage: float
    matched_skills: List[str]
    partial_skills: List[str]
    missing_skills: List[str]


class ResumeSkillGapAnalyzer:
    """
    Semantic NLP and LLM-ready analyzer for resume matching and skill gap detection.
    Swap _embed and _generate_llm_summary with real embedding/LLM APIs as needed.
    """

    def _init_(self, match_threshold: float = 0.80, partial_threshold: float = 0.50):
        self.match_threshold = match_threshold
        self.partial_threshold = partial_threshold

    def _embed(self, text: str) -> np.ndarray:
        words = [w.strip(".,()[]:;\"'").lower() for w in text.split() if w.strip()]
        vocab = sorted(set(words))
        if not vocab:
            return np.zeros(1)
        vec = np.array([words.count(token) for token in vocab], dtype=float)
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else vec

    @staticmethod
    def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        size = min(len(a), len(b))
        if size == 0:
            return 0.0
        va, vb = a[:size], b[:size]
        denom = np.linalg.norm(va) * np.linalg.norm(vb)
        return float(np.dot(va, vb) / denom) if denom > 0 else 0.0

    def evaluate(self, resume_text: str, required_skills: List[str]) -> AnalysisResult:
        matched, partial, missing = [], [], []
        resume_vec = self._embed(resume_text)
        resume_lower = resume_text.lower()

        for skill in required_skills:
            if skill.lower() in resume_lower:
                matched.append(skill)
                continue

            similarity = self._cosine_similarity(resume_vec, self._embed(skill))
            if similarity >= self.match_threshold:
                matched.append(skill)
            elif similarity >= self.partial_threshold:
                partial.append(skill)
            else:
                missing.append(skill)

        total = max(len(required_skills), 1)
        score = ((len(matched) + 0.5 * len(partial)) / total) * 100

        return AnalysisResult(
            match_percentage=round(score, 2),
            matched_skills=matched,
            partial_skills=partial,
            missing_skills=missing,
        )


if _name_ == "_main_":
    resume = (
        "Backend developer skilled in Python, REST APIs, Docker, PostgreSQL, "
        "and natural language processing pipelines."
    )
    target_skills = ["Python", "Docker", "Kubernetes", "NLP", "LLM"]

    analyzer = ResumeSkillGapAnalyzer()
    report = analyzer.evaluate(resume, target_skills)

    print(f"Match Score: {report.match_percentage}%")
    print("Matched Skills:", report.matched_skills)
    print("Partial Skills:", report.partial_skills)
    print("Skill Gaps (Missing):", report.missing_skills)