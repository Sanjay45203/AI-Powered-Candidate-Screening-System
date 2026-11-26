import argparse
from pathlib import Path
from src.recruitment.pipeline import run_batch

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/resumes")
    parser.add_argument("--job", default="data/job_description.txt")
    parser.add_argument("--output", default="outputs")
    args = parser.parse_args()
    job = Path(args.job).read_text(encoding="utf-8")
    rows, metrics = run_batch(args.input, job, args.output)
    print(f"Processed {len(rows)} resumes. Metrics: {metrics}")

if __name__ == "__main__":
    main()
