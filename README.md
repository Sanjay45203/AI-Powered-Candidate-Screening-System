# AI-Powered Multi-Channel Candidate Screening

Modular starter repository using LangGraph, Gmail API, Twilio Voice, and faster-whisper.

## Modules
- `src/recruitment/resume_parser.py`: PDF/TXT extraction
- `src/recruitment/evaluator.py`: explainable keyword baseline score
- `src/recruitment/workflow.py`: LangGraph screening workflow
- `src/recruitment/pipeline.py`: batch processing, ranking, CSV and metrics
- `src/integrations/gmail_client.py`: Gmail OAuth email sending
- `src/integrations/twilio_voice.py`: outbound calls and consent-aware TwiML webhook
- `src/integrations/transcription.py`: local audio transcription
- `src/recruitment/metrics.py`: measured time-savings calculation

## Setup
Use Python 3.11:
```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```
On macOS/Linux activate with `source .venv/bin/activate` and copy with `cp .env.example .env`.

Place anonymized PDF/TXT resumes in `data/resumes/`, edit `data/job_description.txt`, then run:
```bash
python -m src.main --input data/resumes --job data/job_description.txt --output outputs
```

## Gmail setup
Enable Gmail API in Google Cloud, create an OAuth Desktop client, save its JSON as `credentials.json`, and run `GmailClient` from an interactive environment. First authorization creates `token.json`. Never commit either file.

## Twilio setup
Configure a Twilio Voice number and set account credentials in `.env`. Expose the Flask app using HTTPS and set `PUBLIC_BASE_URL`. Configure the number's voice webhook to `POST /voice`, then run:
```bash
python -m src.integrations.twilio_voice
```
Call only candidates who have consented. The sample collects consent before recording. Recording/transcription requirements vary by jurisdiction.

## Speech-to-text
`transcribe_audio()` uses faster-whisper on a saved audio file. The sample Twilio route demonstrates a recording callback, not low-latency streaming. For genuine real-time STT, add Twilio Media Streams over WebSockets and a streaming transcription service.

## Run the LangGraph workflow
```python
from src.recruitment.workflow import build_screening_graph
graph = build_screening_graph()
result = graph.invoke({
    "resume_path": "data/resumes/sample.pdf",
    "job_description": open("data/job_description.txt", encoding="utf-8").read()
})
print(result["evaluation"])
```

## Responsible use and metrics
The keyword evaluator is a demo baseline, not a validated hiring model. It measures textual overlap, not candidate ability. Use job-related criteria, validate for disparate impact, provide human review, and never score protected traits or proxies. A top-10% list is only a review aid.

The claimed 99.5% time reduction (1,000 hours to 5 hours per 1,000 resumes) is not asserted by this code. `metrics.py` calculates a reduction from measured times; benchmark your actual workflow before publishing performance claims. Keep real resumes, recordings, phone numbers, `.env`, and OAuth tokens out of GitHub.

## Git
```bash
git init
git add .
git commit -m "Add AI recruitment screening project"
git branch -M main
git remote add origin <YOUR_REPOSITORY_URL>
git push -u origin main
```
