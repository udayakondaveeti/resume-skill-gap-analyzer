import argparse
import json
from pathlib import Path

from src.llm_recommendation import generate_recommendations
from src.matching_engine import compute_semantic_similarity
from src.resume_parser import load_text_file
from src.skill_extractor import extract_skills
from src.skill_gap_analyzer import analyze_skill_gap
from src.text_preprocessor import preprocess_text


def main() -> None:
    parser = argparse.ArgumentParser(description="Resume Skill-Gap Analyzer")
    parser.add_argument(
        "--resume",
        default="data/resumes/KONDAVEETI UDAYA LAKSHMI Resume.pdf",
        help="Path to resume file (.pdf or .txt)",
    )
    parser.add_argument(
        "--jd",
        default="data/job_descriptions/jd.txt",
        help="Path to job description file",
    )
    parser.add_argument(
        "--output",
        default="results/analysis_report.json",
        help="Path to save JSON report",
    )
    args = parser.parse_args()

    resume_clean = preprocess_text(load_text_file(args.resume))
    jd_clean = preprocess_text(load_text_file(args.jd))

    resume_skills = extract_skills(resume_clean)
    jd_skills = extract_skills(jd_clean)

    gap_report = analyze_skill_gap(resume_skills, jd_skills)
    semantic_score = compute_semantic_similarity(resume_clean, jd_clean)
    recommendations = generate_recommendations(gap_report["missing_skills"])

    print("\n=== Resume & Skill Gap Analysis Report ===")
    print("Scoring Method       : Sentence-BERT (all-MiniLM-L6-v2)")
    print(f"Semantic Similarity  : {semantic_score:.2f}%")
    print(f"Required Skill Match : {gap_report['required_skill_match']:.2f}%")
    print(f"Matched Skills       : {', '.join(gap_report['matched_skills']) or 'None'}")
    print(f"Missing Skills (Gaps): {', '.join(gap_report['missing_skills']) or 'None'}")
    print(f"Additional Skills    : {', '.join(gap_report['additional_skills']) or 'None'}")
    print("\n=== Recommendations ===")
    print(recommendations)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report_data = {
        "semantic_similarity": semantic_score,
        **gap_report,
        "recommendations": recommendations,
    }
    output_path.write_text(json.dumps(report_data, indent=2), encoding="utf-8")
    print(f"\nReport saved to: {output_path}")


if __name__ == "__main__":
    main()