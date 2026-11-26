import os
from flask import Flask, request, Response
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

def start_outbound_call(to_number: str, candidate_id: str):
    # Obtain and record candidate consent before initiating the call.
    client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])
    base = os.environ["PUBLIC_BASE_URL"].rstrip("/")
    return client.calls.create(
        to=to_number, from_=os.environ["TWILIO_FROM_NUMBER"],
        url=f"{base}/voice?candidate_id={candidate_id}", method="POST"
    )

@app.post("/voice")
def voice():
    response = VoiceResponse()
    response.say("Automated screening interview. This call may be recorded or transcribed. "
                 "Continue only if you consent. Press 1 to continue.")
    gather = Gather(num_digits=1, action="/consent", method="POST", timeout=8)
    response.append(gather)
    response.redirect("/voice")
    return Response(str(response), mimetype="text/xml")

@app.post("/consent")
def consent():
    response = VoiceResponse()
    if request.form.get("Digits") != "1":
        response.say("Thank you. No interview will be conducted. Goodbye.")
        response.hangup()
    else:
        response.say("Please describe your relevant experience after the beep.")
        response.record(max_length=120, play_beep=True, transcribe=False,
                        action="/recording-complete", method="POST")
    return Response(str(response), mimetype="text/xml")

@app.post("/recording-complete")
def recording_complete():
    # Queue RecordingUrl/CallSid securely for asynchronous download and transcription.
    # Do not log recording URLs or candidate audio/text.
    app.logger.info("Twilio recording callback received.")
    response = VoiceResponse()
    response.say("Thank you. Your response has been received. Goodbye.")
    response.hangup()
    return Response(str(response), mimetype="text/xml")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
