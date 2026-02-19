"""
Xtenda Finance WhatsApp AI Bot
Stack: Python + Flask + Meta Cloud API + Gemini AI + Google Sheets
"""

from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from bot_flow import handle_message

load_dotenv()

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "xtenda_verify_token")


# ── Webhook Verification (Meta requires this on setup) ─────────────────────
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode      = request.args.get("hub.mode")
    token     = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ Webhook verified!")
        return challenge, 200
    return "Forbidden", 403


# ── Receive Incoming WhatsApp Messages ─────────────────────────────────────
@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()

    try:
        entry   = data["entry"][0]
        changes = entry["changes"][0]["value"]

        # Ignore status updates (delivered, read receipts)
        if "messages" not in changes:
            return jsonify({"status": "ok"}), 200

        message = changes["messages"][0]
        contact = changes["contacts"][0]

        phone_number = message["from"]          # e.g. 260971234567
        display_name = contact["profile"]["name"]
        msg_type     = message["type"]

        # Extract text — handles regular text AND button/list replies
        if msg_type == "text":
            user_text = message["text"]["body"].strip()
        elif msg_type == "interactive":
            interactive = message["interactive"]
            if interactive["type"] == "button_reply":
                user_text = interactive["button_reply"]["id"]
            elif interactive["type"] == "list_reply":
                user_text = interactive["list_reply"]["id"]
            else:
                user_text = ""
        else:
            user_text = ""

        print(f"📩 From {display_name} ({phone_number}): {user_text}")

        # Hand off to bot logic
        handle_message(phone_number, display_name, user_text)

    except (KeyError, IndexError) as e:
        print(f"⚠️  Parse error: {e}")

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
