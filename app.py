from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

# המפתח שלך ל-Gemini
GEMINI_API_KEY = "AIzaSyAS7-gayw68rfTSzLJ-UvQqEEBg6bNSR-4"

@app.route("/", methods=["POST"])
def yemot_handler():
    user_text = request.values.get("RecordingText")
    
    if not user_text:
        xml_response = """<?xml version="1.0" encoding="UTF-8"?>
        <response>
            <say>שלום! דבר אחרי הצפצוף ואני אענה לך</say>
            <record max_seconds="10" silence_timeout="3" />
        </response>"""
        return Response(xml_response, mimetype="text/xml")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": user_text}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        ai_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"Error: {e}")
        ai_text = "מצטער, הייתה שגיאה בחיבור למוח שלי."

    xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
    <response>
        <say>{ai_text}</say>
        <record max_seconds="10" silence_timeout="3" />
    </response>"""
    
    return Response(xml_response, mimetype="text/xml")

if __name__ == "__main__":
    app.run(port=5000)
