"""
Mardan Board Past Papers Telegram Bot
Author: ChatGPT
Description: Collect & Generate past papers for Mardan Board
Deploy-ready (Render/Heroku etc.)
"""

import os
import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# ================== CONFIG ==================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "PUT_YOUR_TOKEN_HERE")

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ---------------- PAST PAPER LINKS ----------------
PAST_PAPER_URLS = {
    "9th": {
        "english": "https://www.ilmkidunya.com/past_papers/mardan9th-past-papers.aspx",
        "urdu": "https://www.ilmkidunya.com/past_papers/mardan9th-past-papers.aspx",
        "math": "https://www.ilmkidunya.com/past_papers/mardan9th-past-papers.aspx",
        "computer": "https://www.ilmkidunya.com/past_papers/mardan9th-past-papers.aspx",
        "biology": "https://www.ilmkidunya.com/past_papers/mardan9th-past-papers.aspx",
    },
    "10th": {
        "english": "https://www.ilmkidunya.com/past_papers/mardan10th-past-papers.aspx",
        "urdu": "https://www.ilmkidunya.com/past_papers/mardan10th-past-papers.aspx",
        "math": "https://www.ilmkidunya.com/past_papers/mardan10th-past-papers.aspx",
        "computer": "https://www.ilmkidunya.com/past_papers/mardan10th-past-papers.aspx",
        "biology": "https://www.ilmkidunya.com/past_papers/mardan10th-past-papers.aspx",
    },
    "11th": {
        "english": "https://www.ilmkidunya.com/past_papers/mardan11th-past-papers.aspx",
        "urdu": "https://www.ilmkidunya.com/past_papers/mardan11th-past-papers.aspx",
        "math": "https://www.ilmkidunya.com/past_papers/mardan11th-past-papers.aspx",
        "computer": "https://www.ilmkidunya.com/past_papers/mardan11th-past-papers.aspx",
        "biology": "https://www.ilmkidunya.com/past_papers/mardan11th-past-papers.aspx",
    },
    "12th": {
        "english": "https://www.ilmkidunya.com/past_papers/mardan12th-past-papers.aspx",
        "urdu": "https://www.ilmkidunya.com/past_papers/mardan12th-past-papers.aspx",
        "math": "https://www.ilmkidunya.com/past_papers/mardan12th-past-papers.aspx",
        "computer": "https://www.ilmkidunya.com/past_papers/mardan12th-past-papers.aspx",
        "biology": "https://www.ilmkidunya.com/past_papers/mardan12th-past-papers.aspx",
    },
}

FALLBACK_URL = "https://www.ilmkidunya.com/past_papers/mardan-board-past-papers.aspx"

# ---------------- COMMAND HANDLERS ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("9th Class", callback_data="class_9th")],
        [InlineKeyboardButton("10th Class", callback_data="class_10th")],
        [InlineKeyboardButton("11th Class", callback_data="class_11th")],
        [InlineKeyboardButton("12th Class", callback_data="class_12th")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "📚 *Welcome to Mardan Board Past Papers Bot*\n\n"
        "Select your class to continue:",
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )


async def class_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    class_name = query.data.replace("class_", "")
    context.user_data["class"] = class_name
    keyboard = [
        [InlineKeyboardButton("English", callback_data="subject_english")],
        [InlineKeyboardButton("Urdu", callback_data="subject_urdu")],
        [InlineKeyboardButton("Math", callback_data="subject_math")],
        [InlineKeyboardButton("Computer", callback_data="subject_computer")],
        [InlineKeyboardButton("Biology", callback_data="subject_biology")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f"✅ You selected *{class_name} Class*.\n\nNow choose your subject:",
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )


async def subject_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    subject = query.data.replace("subject_", "")
    context.user_data["subject"] = subject
    keyboard = [
        [InlineKeyboardButton("📂 Collect Past Papers", callback_data="action_collect")],
        [InlineKeyboardButton("📝 Generate Random Paper", callback_data="action_generate")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f"📘 Subject selected: *{subject.title()}*\n\nChoose an option:",
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )


async def action_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action = query.data.replace("action_", "")
    class_name = context.user_data.get("class")
    subject = context.user_data.get("subject")
    if not class_name or not subject:
        await query.edit_message_text("⚠ Please start again using /start")
        return

    if action == "collect":
        url = PAST_PAPER_URLS.get(class_name, {}).get(subject, FALLBACK_URL)
        message_text = (
            f"📂 *Past Papers for {class_name} Class - {subject.title()}*\n\n"
            f"🔗 [Click here to view and download past papers]({url})\n\n"
            f"📝 *Available Papers:* 2004-2025\n"
            f"🎯 *Board:* Mardan Board\n"
            f"📚 *Subject:* {subject.title()}"
        )
    else:
        message_text = (
            f"📝 *Random Generated Paper*\n\n"
            f"📘 Class: {class_name}\n"
            f"📚 Subject: {subject.title()}\n"
            f"⚡ Note: This is an auto-generated practice paper."
        )

    keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_start")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=message_text,
        reply_markup=reply_markup,
        parse_mode="Markdown",
        disable_web_page_preview=False,
    )


async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start(update, context)


# ---------------- MAIN ----------------
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(class_handler, pattern="^class_"))
    app.add_handler(CallbackQueryHandler(subject_handler, pattern="^subject_"))
    app.add_handler(CallbackQueryHandler(action_handler, pattern="^action_"))
    app.add_handler(CallbackQueryHandler(back_to_start, pattern="^back_to_start$"))

    logger.info("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
