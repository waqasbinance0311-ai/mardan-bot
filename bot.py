import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# ======================
# BOT TOKEN (Env se lo)
# ======================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN not set in environment variables.")

# ======================
# SUBJECT SLUGS
# ======================
SUBJECT_MAP = {
    "english": "english",
    "urdu": "urdu",
    "math": "mathematics",
    "computer": "computer-science",
    "biology": "biology"
}

# ======================
# START MENU
# ======================
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("9th", callback_data="class_9th"),
         InlineKeyboardButton("10th", callback_data="class_10th")],
        [InlineKeyboardButton("11th", callback_data="class_11th"),
         InlineKeyboardButton("12th", callback_data="class_12th")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "📘 *Welcome to Mardan Board Papers Bot!*\n\n"
        "👉 Choose your Class: 9th | 10th | 11th | 12th\n"
        "👉 Choose Subject: English | Urdu | Math | Bio | Computer\n"
        "👉 Options:\n"
        "     📂 Get Past Papers (2020–2025)\n"
        "     📝 Generate New Paper"
    )
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

# ======================
# HANDLE CLASS SELECTION
# ======================
async def class_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    selected_class = query.data.replace("class_", "")  # e.g. "9th"

    context.user_data["class"] = selected_class

    keyboard = [
        [InlineKeyboardButton("🇬🇧 English", callback_data="sub_english"),
         InlineKeyboardButton("🇵🇰 Urdu", callback_data="sub_urdu")],
        [InlineKeyboardButton("➗ Math", callback_data="sub_math"),
         InlineKeyboardButton("💻 Computer", callback_data="sub_computer")],
        [InlineKeyboardButton("🧬 Biology", callback_data="sub_biology")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=f"📘 You selected *{selected_class} Class*.\n\n👉 Now choose a subject 👇",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ======================
# HANDLE SUBJECT SELECTION
# ======================
async def subject_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    selected_subject = query.data.replace("sub_", "")

    context.user_data["subject"] = selected_subject

    keyboard = [
        [InlineKeyboardButton("📂 Get Past Papers", callback_data="action_collect")],
        [InlineKeyboardButton("📝 Generate New Paper", callback_data="action_generate")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=f"📗 You selected *{context.user_data['class']} Class – {selected_subject.title()}*.\n\n👉 Choose an option 👇",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ======================
# HANDLE FINAL ACTION
# ======================
async def action_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    action = query.data.replace("action_", "")
    class_name = context.user_data.get("class")   # e.g. "9th"
    subject = context.user_data.get("subject")    # e.g. "english"

    if not class_name or not subject:
        await query.edit_message_text("⚠️ Please start again using /start")
        return

    if action == "collect":
        subject_slug = SUBJECT_MAP.get(subject, subject)
        url = f"https://www.ilmkidunya.com/past_papers/mardan-board-{class_name}-class-{subject_slug}-past-papers.aspx"

        await query.edit_message_text(
            text=f"📂 Here are the past papers for *{class_name} Class – {subject.title()} (2020–2025)*:\n\n🔗 [Click here to view papers]({url})",
            parse_mode="Markdown"
        )
    else:
        await query.edit_message_text(
            text=f"📝 Generating a new paper for *{class_name} Class – {subject.title()}*...\n\n⚡ Paper coming soon!"
        )

# ======================
# MAIN
# ======================
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(class_handler, pattern="^class_"))
    app.add_handler(CallbackQueryHandler(subject_handler, pattern="^sub_"))
    app.add_handler(CallbackQueryHandler(action_handler, pattern="^action_"))
    print("✅ Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
