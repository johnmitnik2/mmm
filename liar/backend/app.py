from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask, request, jsonify
from google import genai
from google.genai import types
from PIL import Image

app = Flask(__name__)

def get_response(chat, text):
    response = chat.send_message_stream(text)
    return "".join(chunk.text for chunk in response)

@app.route("/advice", methods=["POST"])
def advice():
    data = request.json
    p_user = data["input"]

    # ---- load secrets / prompts ----
    key = os.environ["GEMINI_API_KEY"]
    p_advise = os.environ["ADVICE_PROMPT"]
    p_negate = os.environ["NEGATION_PROMPT"]
    p_strip = os.environ["STRIPPING_PROMPT"]

    # ---- Gemini setup ----
    client = genai.Client(api_key=key)
    chat1 = client.chats.create(model="gemini-3-flash-preview")
    chat2 = client.chats.create(model="gemini-3-flash-preview")

    # ---- first chat stream ----
    get_response(chat1, p_advise)
    get_response(chat1, p_user)
    r13 = get_response(chat1, p_strip)

    # ---- second chat stream ----
    get_response(chat2, p_negate)
    r22 = get_response(chat2, r13)

    return jsonify({"response": r22})

if __name__ == "__main__":
    app.run()
