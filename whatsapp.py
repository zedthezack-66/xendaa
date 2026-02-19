"""
whatsapp.py — All WhatsApp Cloud API message senders
Handles: text, buttons (up to 3), list menus (up to 10 options)
"""

import requests
import os

API_URL = "https://graph.facebook.com/v19.0"
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
ACCESS_TOKEN    = os.getenv("WHATSAPP_ACCESS_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type":  "application/json",
}


def _post(payload: dict):
    url = f"{API_URL}/{PHONE_NUMBER_ID}/messages"
    r   = requests.post(url, json=payload, headers=HEADERS)
    if r.status_code != 200:
        print(f"❌ WhatsApp API error: {r.text}")
    return r.json()


# ── 1. Plain text message ───────────────────────────────────────────────────
def send_text(to: str, body: str):
    return _post({
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"preview_url": False, "body": body},
    })


# ── 2. Button message (max 3 buttons) ──────────────────────────────────────
def send_buttons(to: str, body: str, buttons: list[dict]):
    """
    buttons = [{"id": "btn_id", "title": "Label"}, ...]  — max 3
    """
    return _post({
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": body},
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {"id": b["id"], "title": b["title"]}}
                    for b in buttons[:3]
                ]
            },
        },
    })


# ── 3. List message (max 10 rows) ───────────────────────────────────────────
def send_list(to: str, body: str, button_label: str, sections: list[dict]):
    """
    sections = [
        {
            "title": "Section Title",
            "rows": [{"id": "row_id", "title": "Row Label", "description": "Optional"}, ...]
        }
    ]
    """
    return _post({
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body":   {"text": body},
            "action": {
                "button":   button_label,
                "sections": sections,
            },
        },
    })


# ── Helper: Main Menu ────────────────────────────────────────────────────────
def send_main_menu(to: str, name: str):
    send_list(
        to   = to,
        body = (
            f"Hello {name}! 👋 Welcome to *Xtenda Finance*.\n\n"
            "We offer fast, affordable loans in Zambia 🇿🇲\n"
            "How can we help you today?"
        ),
        button_label = "Choose an Option",
        sections = [{
            "title": "Main Menu",
            "rows": [
                {"id": "menu_products",    "title": "💰 Our Loan Products",   "description": "View all loan types & rates"},
                {"id": "menu_eligibility", "title": "✅ Check Eligibility",   "description": "See if you qualify"},
                {"id": "menu_apply",       "title": "📋 Apply / Get a Quote", "description": "Start your loan application"},
                {"id": "menu_callback",    "title": "📞 Book a Callback",     "description": "Speak to our sales team"},
                {"id": "menu_ai",          "title": "❓ Ask a Question",      "description": "Ask us anything"},
            ],
        }],
    )


# ── Helper: Loan Product Menu ────────────────────────────────────────────────
def send_product_menu(to: str):
    send_list(
        to   = to,
        body = "We have 4 loan products 👇\nSelect one to see details:",
        button_label = "View Product",
        sections = [{
            "title": "Loan Products",
            "rows": [
                {"id": "prod_personal",  "title": "💳 Personal Loan",       "description": "ZMW 1,000 – 50,000 | 3–24 months"},
                {"id": "prod_business",  "title": "🏢 Business Loan",       "description": "ZMW 5,000 – 500,000 | 6–36 months"},
                {"id": "prod_salary",    "title": "💼 Salary-Backed Loan",  "description": "Up to 3× net salary | Fastest approval"},
                {"id": "prod_asset",     "title": "🚗 Asset Finance",       "description": "Vehicles & equipment | Up to 60 months"},
                {"id": "menu_main",      "title": "🔙 Back to Main Menu",   "description": ""},
            ],
        }],
    )


# ── Helper: Apply — Loan Type Selection ──────────────────────────────────────
def send_loan_type_selection(to: str):
    send_list(
        to   = to,
        body = "Great! Let's get you started 🚀\n\nWhich type of loan are you applying for?",
        button_label = "Select Loan Type",
        sections = [{
            "title": "Loan Type",
            "rows": [
                {"id": "apply_personal",  "title": "💳 Personal Loan"},
                {"id": "apply_business",  "title": "🏢 Business Loan"},
                {"id": "apply_salary",    "title": "💼 Salary-Backed Loan"},
                {"id": "apply_asset",     "title": "🚗 Asset Finance"},
            ],
        }],
    )


# ── Helper: Employment Status ─────────────────────────────────────────────────
def send_employment_status(to: str):
    send_buttons(
        to      = to,
        body    = "What is your employment status?",
        buttons = [
            {"id": "emp_employed",   "title": "🏦 Employed"},
            {"id": "emp_selfemployed","title": "🏪 Self-Employed"},
            {"id": "emp_civil",      "title": "🏛️ Civil Servant"},
        ],
    )


# ── Helper: Callback Time ─────────────────────────────────────────────────────
def send_callback_time(to: str):
    send_buttons(
        to      = to,
        body    = "When would you prefer our team to call you?",
        buttons = [
            {"id": "time_morning",   "title": "🌅 Morning (8–12)"},
            {"id": "time_afternoon", "title": "☀️ Afternoon (12–17)"},
            {"id": "time_evening",   "title": "🌆 Evening (17–19)"},
        ],
    )


# ── Helper: Back to menu prompt ───────────────────────────────────────────────
def send_back_prompt(to: str):
    send_buttons(
        to      = to,
        body    = "What would you like to do next?",
        buttons = [
            {"id": "menu_apply",    "title": "📋 Apply Now"},
            {"id": "menu_callback", "title": "📞 Book Callback"},
            {"id": "menu_main",     "title": "🔙 Main Menu"},
        ],
    )
