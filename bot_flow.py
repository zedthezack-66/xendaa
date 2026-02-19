"""
bot_flow.py — Hybrid bot logic for Xtenda Finance
Rules handle menus & structured flows. Gemini AI handles open questions.

CONVERSATION STATES:
    idle             → Show welcome / main menu
    awaiting_amount  → Collecting loan amount (free text)
    awaiting_name    → Collecting full name
    awaiting_callback_name → Collecting name for callback
    awaiting_callback_time → Waiting for time selection
    ai_mode          → Open Q&A with Gemini
"""

from whatsapp import (
    send_text, send_main_menu, send_product_menu,
    send_loan_type_selection, send_employment_status,
    send_callback_time, send_back_prompt
)


# ── In-memory session store ─────────────────────────────────────────────────
# Format: { phone: {"state": "...", "lead": {...}, "name": "..."} }
sessions: dict[str, dict] = {}


def get_session(phone: str, display_name: str) -> dict:
    if phone not in sessions:
        sessions[phone] = {"state": "idle", "lead": {}, "name": display_name}
    return sessions[phone]


def reset_session(phone: str, display_name: str):
    sessions[phone] = {"state": "idle", "lead": {}, "name": display_name}


# ── Product Info Texts ───────────────────────────────────────────────────────
PRODUCT_INFO = {
    "prod_personal": (
        "💳 *Personal Loan*\n\n"
        "• Amount: ZMW 1,000 – 50,000\n"
        "• Term: 3 – 24 months\n"
        "• Rate: From 4.5% per month\n"
        "• Required: NRC, payslip, 3-month bank statement\n\n"
        "Approval within 24–48 hours ✅"
    ),
    "prod_business": (
        "🏢 *Business Loan*\n\n"
        "• Amount: ZMW 5,000 – 500,000\n"
        "• Term: 6 – 36 months\n"
        "• Rate: From 3.8% per month\n"
        "• Required: Business reg, financials, NRC\n\n"
        "Ideal for stock, equipment or expansion 📈"
    ),
    "prod_salary": (
        "💼 *Salary-Backed Loan*\n\n"
        "• Up to 3× your net monthly salary\n"
        "• Repaid via payroll deduction (stress-free!)\n"
        "• Available to civil servants & private employees\n"
        "• ✅ Same-day approval in most cases!\n\n"
        "Fastest loan we offer 🚀"
    ),
    "prod_asset": (
        "🚗 *Asset Finance*\n\n"
        "• Finance vehicles, equipment & machinery\n"
        "• Terms: Up to 60 months\n"
        "• New & used assets accepted\n"
        "• Competitive interest rates\n\n"
        "Drive your business forward 💪"
    ),
}

LOAN_TYPE_NAMES = {
    "apply_personal": "Personal Loan",
    "apply_business": "Business Loan",
    "apply_salary":   "Salary-Backed Loan",
    "apply_asset":    "Asset Finance",
}

EMPLOYMENT_LABELS = {
    "emp_employed":    "Employed",
    "emp_selfemployed": "Self-Employed",
    "emp_civil":       "Civil Servant",
}

CALLBACK_TIME_LABELS = {
    "time_morning":   "Morning (8am–12pm)",
    "time_afternoon": "Afternoon (12pm–5pm)",
    "time_evening":   "Evening (5pm–7pm)",
}

# Keywords that reset to main menu
MENU_KEYWORDS = {"menu", "hi", "hello", "start", "hie", "hey", "muli bwanji",
                 "mwabonwa", "howzit", "back", "restart", "home"}


# ── Main Handler ─────────────────────────────────────────────────────────────
def handle_message(phone: str, display_name: str, user_input: str):
    session = get_session(phone, display_name)
    state   = session["state"]
    text    = user_input.lower().strip()

    # Global escape — any greeting/menu keyword resets to main menu
    if text in MENU_KEYWORDS or user_input == "menu_main":
        reset_session(phone, display_name)
        send_main_menu(phone, display_name)
        return

    # ── IDLE: Show main menu ─────────────────────────────────────────────────
    if state == "idle":
        _handle_menu(phone, session, user_input, display_name)

    # ── APPLY FLOW ────────────────────────────────────────────────────────────
    elif state == "awaiting_loan_type":
        if user_input in LOAN_TYPE_NAMES:
            session["lead"]["loan_type"] = LOAN_TYPE_NAMES[user_input]
            session["state"] = "awaiting_amount"
            send_text(phone,
                f"How much would you like to borrow? 💵\n"
                f"Please enter the amount in ZMW\n"
                f"_(e.g. 15000)_"
            )
        else:
            send_loan_type_selection(phone)

    elif state == "awaiting_amount":
        # Accept any numeric-ish text as amount
        amount = user_input.replace(",", "").replace("zmw", "").replace("k", "000").strip()
        if amount.isdigit():
            session["lead"]["loan_amount"] = f"ZMW {int(amount):,}"
            session["state"] = "awaiting_employment"
            send_employment_status(phone)
        else:
            send_text(phone, "Please enter a number — e.g. *15000* (no letters or symbols)")

    elif state == "awaiting_employment":
        if user_input in EMPLOYMENT_LABELS:
            session["lead"]["employment"] = EMPLOYMENT_LABELS[user_input]
            session["state"] = "awaiting_name"
            send_text(phone, "Almost done! 😊\n\nWhat is your *full name*?")
        else:
            send_employment_status(phone)

    elif state == "awaiting_name":
        session["lead"]["name"]  = user_input
        session["lead"]["phone"] = phone
        session["state"] = "awaiting_callback_time"
        send_callback_time(phone)

    elif state == "awaiting_callback_time":
        if user_input in CALLBACK_TIME_LABELS:
            session["lead"]["callback_time"] = CALLBACK_TIME_LABELS[user_input]
            _save_and_confirm(phone, session, display_name)
        else:
            send_callback_time(phone)

    # ── CALLBACK FLOW ─────────────────────────────────────────────────────────
    elif state == "awaiting_callback_name":
        session["lead"]["name"]  = user_input
        session["lead"]["phone"] = phone
        session["state"] = "awaiting_callback_time_only"
        send_callback_time(phone)

    elif state == "awaiting_callback_time_only":
        if user_input in CALLBACK_TIME_LABELS:
            session["lead"]["callback_time"] = CALLBACK_TIME_LABELS[user_input]
            session["lead"]["loan_type"]  = session["lead"].get("loan_type", "General Inquiry")
            session["lead"]["loan_amount"] = "TBD"
            session["lead"]["employment"]  = "TBD"
            _save_and_confirm(phone, session, display_name)
        else:
            send_callback_time(phone)

    # ── AI MODE ───────────────────────────────────────────────────────────────
    elif state == "ai_mode":
        ai_reply = ask_gemini(phone, user_input)
        send_text(phone, ai_reply)
        # After AI reply, offer to go back to menu
        send_text(phone, "─────────────────\nType *menu* anytime to go back to the main menu 🏠")

    else:
        # Unknown state — reset
        reset_session(phone, display_name)
        send_main_menu(phone, display_name)


# ── Menu Handler ──────────────────────────────────────────────────────────────
def _handle_menu(phone: str, session: dict, user_input: str, display_name: str):

    # First message (new user or greeting)
    if not user_input:
        send_main_menu(phone, display_name)
        return

    # ── Main menu selections ─────────────────────────────────────────────────
    if user_input == "menu_products":
        send_product_menu(phone)

    elif user_input in PRODUCT_INFO:
        send_text(phone, PRODUCT_INFO[user_input])
        send_back_prompt(phone)

    elif user_input == "menu_eligibility":
        send_text(phone,
            "✅ *Eligibility Requirements*\n\n"
            "To qualify for an Xtenda Finance loan:\n\n"
            "• 🎂 Age 18 or above\n"
            "• 🇿🇲 Zambian citizen or resident\n"
            "• 💼 Employed OR running a business for 6+ months\n"
            "• 🪪 Valid NRC\n"
            "• 🏦 Active bank account\n\n"
            "If you meet these, you're likely eligible! 🎉"
        )
        send_back_prompt(phone)

    elif user_input == "menu_apply":
        session["state"] = "awaiting_loan_type"
        send_loan_type_selection(phone)

    elif user_input == "menu_callback":
        session["state"] = "awaiting_callback_name"
        send_text(phone,
            "📞 *Book a Callback*\n\n"
            "One of our sales agents will call you!\n\n"
            "First, what is your *full name*?"
        )

    elif user_input == "menu_ai":
        session["state"] = "ai_mode"
        send_text(phone,
            "🤖 You can ask me anything about Xtenda Finance!\n\n"
            "Go ahead — type your question 👇\n"
            "_(Type *menu* anytime to go back)_"
        )

    elif user_input in ("menu_apply", "apply_personal", "apply_business",
                        "apply_salary", "apply_asset"):
        session["state"] = "awaiting_loan_type"
        send_loan_type_selection(phone)

    else:
        # Unknown input in idle → route to AI or show menu
        if len(user_input) > 5:
            # Treat as a question — use Gemini
            session["state"] = "ai_mode"
            ai_reply = ask_gemini(phone, user_input)
            send_text(phone, ai_reply)
            send_text(phone, "─────────────────\nType *menu* to go back to the main menu 🏠")
        else:
            send_main_menu(phone, display_name)


# ── Save Lead & Confirm ───────────────────────────────────────────────────────
def _save_and_confirm(phone: str, session: dict, display_name: str):
    lead   = session["lead"]
    saved  = save_lead(lead)

    name          = lead.get("name", display_name)
    loan_type     = lead.get("loan_type", "")
    loan_amount   = lead.get("loan_amount", "")
    callback_time = lead.get("callback_time", "")

    send_text(phone,
        f"🎉 *Thank you, {name}!*\n\n"
        f"Your request has been received:\n"
        f"• Loan Type: {loan_type}\n"
        f"• Amount: {loan_amount}\n"
        f"• Callback: {callback_time}\n\n"
        f"Our sales team will call you during your preferred time 📞\n\n"
        f"_Reference #XF{phone[-4:].upper()}_ | Xtenda Finance 🇿🇲"
    )

    if not saved:
        send_text(phone,
            "⚠️ Note: There was a small issue saving your details.\n"
            "Our team will still follow up — but please also call us on *+260 XXX XXX XXX* to confirm."
        )

    # Reset session after completion
    reset_session(phone, display_name)
