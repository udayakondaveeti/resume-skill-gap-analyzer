def analyze_skill_gap(
    resume_skills: list[str],
    jd_skills: list[str],
) -> dict[str, list[str] | float]:
    """Compare resume skills against JD skills and return gap breakdown."""
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    matched = sorted(resume_set & jd_set)
    missing = sorted(jd_set - resume_set)
    additional = sorted(resume_set - jd_set)

    match_pct = round((len(matched) / len(jd_set)) * 100, 2) if jd_set else 0.0

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "additional_skills": additional,
        "required_skill_match": match_pct,
    }