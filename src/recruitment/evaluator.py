import re

def _terms(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z][a-zA-Z+#.-]{1,}", text.lower()))

def evaluate_candidate(resume_text: str, job_description: str) -> dict:
    # Explainable keyword-overlap demo only; not a validated hiring assessment.
    stop = {"with", "from", "that", "this", "will", "your", "have", "the",
            "and", "for", "are", "you", "our", "role", "required"}
    criteria = sorted(_terms(job_description) - stop)
    matched = sorted(set(criteria) & _terms(resume_text))
    score = round(100 * len(matched) / max(len(criteria), 1), 2)
    return {
        "score": score,
        "matched_terms": matched,
        "missing_terms": sorted(set(criteria) - set(matched)),
        "review_note": "Keyword overlap only; human review and role-specific validation required."
    }
