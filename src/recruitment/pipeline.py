import json, os, time
from pathlib import Path
import pandas as pd
from src.recruitment.workflow import build_screening_graph
from src.recruitment.metrics import calculate_time_savings

def run_batch(input_dir: str, job_description: str, output_dir: str):
    source, destination = Path(input_dir), Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    resume_files = sorted(p for p in source.iterdir() if p.suffix.lower() in {".pdf", ".txt"})
    graph, rows = build_screening_graph(), []
    start = time.perf_counter()
    for path in resume_files:
        try:
            result = graph.invoke({"resume_path": str(path), "job_description": job_description})
            evaluation = result["evaluation"]
            rows.append({
                "candidate_id": path.stem, "score": evaluation["score"],
                "matched_terms": ", ".join(evaluation["matched_terms"]),
                "missing_terms": ", ".join(evaluation["missing_terms"]),
                "status": result["status"], "review_note": evaluation["review_note"], "error": ""
            })
        except Exception as exc:
            rows.append({"candidate_id": path.stem, "score": None, "matched_terms": "",
                         "missing_terms": "", "status": "processing_error",
                         "review_note": "", "error": str(exc)})
    elapsed = time.perf_counter() - start
    frame = pd.DataFrame(rows)
    fraction = float(os.getenv("SHORTLIST_FRACTION", "0.10"))
    if not frame.empty:
        valid = frame[frame["score"].notna()].sort_values("score", ascending=False)
        count = max(1, int(len(valid) * fraction)) if len(valid) else 0
        selected = set(valid.head(count)["candidate_id"])
        frame["shortlist_flag"] = frame["candidate_id"].isin(selected)
    frame.to_csv(destination / "candidate_results.csv", index=False)
    automated_hours = elapsed * 1000 / max(len(resume_files), 1) / 3600
    metrics = {
        "resume_count": len(resume_files),
        "processed_count": int((frame["status"] != "processing_error").sum()) if not frame.empty else 0,
        "elapsed_seconds": round(elapsed, 3),
        "time_savings_example": calculate_time_savings(1000, automated_hours)
    }
    (destination / "run_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return rows, metrics
