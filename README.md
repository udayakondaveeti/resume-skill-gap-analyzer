# Resume Skill-Gap Analyzer

A modular Python CLI tool that evaluates a candidate's resume against a job description (JD) using **Sentence-BERT (`all-MiniLM-L6-v2`)** for semantic similarity scoring and canonical skill-gap analysis[span_2](start_span)[span_2](end_span)[span_3](start_span)[span_3](end_span).

## Project Structure

```text
resume-skill-gap-analyzer/
├── data/
│   ├── job_descriptions/
│   │   └── jd.txt
│   └── resumes/
│       └── KONDAVEETI UDAYA LAKSHMI Resume.pdf
├── results/
│   └── analysis_report.json
├── src/
│   ├── __init__.py
│   ├── resume_parser.py
│   ├── text_preprocessor.py
│   ├── skill_extractor.py
│   ├── matching_engine.py
│   ├── skill_gap_analyzer.py
│   └── llm_recommendation.py
├── main.py
├── requirements.txt
└── README.md