import os
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram.error import TimedOut, NetworkError

# ======================
# BOT TOKEN & CHAT ID
# ======================
BOT_TOKEN = "8023108538:AAE51wAdhjHSv6TQOYBBe7RS0jIrOTRoOcs"
CHAT_ID = "5969642968"

# ======================
# SUBJECT SLUGS (FIXED URLs)
# ======================
SUBJECT_MAP = {
    "english": {
        "slug": "english",
        "url": "https://www.ilmkidunya.com/past_papers/9th-class-english-past-papers-mardan-board.aspx"
    },
    "urdu": {
        "slug": "urdu",
        "url": "https://www.ilmkidunya.com/past_papers/9th-class-urdu-past-papers-mardan-board.aspx"
    },
    "math": {
        "slug": "mathematics",
        "url": "https://www.ilmkidunya.com/past_papers/9th-class-mathematics-past-papers-mardan-board.aspx"
    },
    "computer": {
        "slug": "computer-science",
        "url": "https://www.ilmkidunya.com/past_papers/9th-class-computer-science-past-papers-mardan-board.aspx"
    },
    "biology": {
        "slug": "biology",
        "url": "https://www.ilmkidunya.com/past_papers/9th-class-biology-past-papers-mardan-board.aspx"
    }
}

# ======================
# SAMPLE QUESTIONS
# ======================
QUESTION_BANK = {
    "english": {
        "mcqs": [
            "He ____ to school daily. (go/goes)",
            "Synonym of Happy?",
            "Antonym of Brave?",
            "Correct passive: 'Ali writes a letter.'",
            "Choose the correct spelling: (Enviroment/Environment)"
        ],
        "short": [
            "Define a noun with examples.",
            "What is a pronoun?",
            "Difference between Active & Passive voice?",
            "Write 5 sentences using Present Perfect Tense.",
            "What is a Paragraph? Write an example."
        ],
        "long": [
            "Write an essay on 'My Country'.",
            "Translate the following passage into English."
        ]
    },
    "urdu": {
        "mcqs": [
            "لفظ 'کتاب' کس صنف سے تعلق رکھتا ہے؟",
            "'خوبصورت' کا مترادف کیا ہے؟",
            "جملہ مکمل کریں: وہ اسکول ___ ہے۔",
            "'دوستی' پر صحیح محاورہ منتخب کریں۔",
            "'محبت' کا متضاد کیا ہے؟"
        ],
        "short": [
            "سبق 'قوم کی ترقی' کا خلاصہ لکھیں۔",
            "محاورہ کی تعریف کریں۔",
            "قائداعظم پر چند جملے لکھیں۔",
            "شاعر کے بارے میں لکھیں۔",
            "سبق 'ہمت اور حوصلہ' کے نکات لکھیں۔"
        ],
        "long": [
            "یادداشت پر مضمون لکھیں۔",
            "پاکستان پر ایک تقریر تحریر کریں۔"
        ]
    },
    "math": {
        "mcqs": [
            "2 + 2 × 2 = ?",
            "Square root of 144?",
            "Derivative of x²?",
            "Value of π?",
            "Solve: 5x = 20"
        ],
        "short": [
            "Simplify: (x+2)(x+3)",
            "Find LCM of 12 and 18.",
            "Solve: 2x+5=15",
            "Define prime numbers with examples.",
            "Factorize: x² - 9"
        ],
        "long": [
            "Solve quadratic equation: x²+5x+6=0",
            "Draw a graph of y=2x+3"
        ]
    },
    "computer": {
        "mcqs": [
            "CPU stands for?",
            "1 KB = ? bytes",
            "Who is the father of Computer?",
            "Shortcut of Copy in Windows?",
            "Binary of 5?"
        ],
        "short": [
            "Define Software.",
            "Difference between RAM & ROM.",
            "What is Algorithm?",
            "Write 2 advantages of Internet.",
            "Define Operating System."
        ],
        "long": [
            "Explain generations of computers.",
            "Write a note on MS Word."
        ]
    },
    "biology": {
        "mcqs": [
            "Unit of life is?",
            "Photosynthesis occurs in?",
            "Which organ pumps blood?",
            "DNA stands for?",
            "Name the largest bone in human body."
        ],
        "short": [
            "Define Cell Theory.",
            "Difference between Mitosis & Meiosis.",
            "What is Chlorophyll?",
            "Define respiration.",
            "What is tissue?"
        ],
        "long": [
            "Explain Digestive System in detail.",
            "Write a note on Human Heart."
        ]
    }
}

# ======================
# START MENU with ERROR HANDLING
# ======================
async def start(update: Update, context: CallbackContext):
    try:
        keyboard = [
            [InlineKeyboardButton("9th", callback_data="class_9th"),
             InlineKeyboardButton("10th", callback_data="class_10th")],
            [InlineKeyboardButton("11th", callback_data="class_11th"),
             InlineKeyboardButton("12th", callback_data="class_12th")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        text = (
            "📘 Welcome to Mardan Board Papers Bot!\n\n"
            "👉 Choose your Class: 9th | 10th | 11th | 12th\n"
            "👉 Choose Subject: English | Urdu | Math | Bio | Computer\n"
            "👉 Options:\n"
            "     📂 Get Past Papers (2020–2025)\n"
            "     📝 Generate New Paper"
        )
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    except (TimedOut, NetworkError):
        await asyncio.sleep(5)
        await update.message.reply_text("⌛ Connection timeout. Please try again /start")

# ======================
# HANDLE CLASS SELECTION with ERROR HANDLING
# ======================
async def class_handler(update: Update, context: CallbackContext):
    try:
        query = update.callback_query
        await query.answer()
        selected_class = query.data.replace("class_", "")

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
            text=f"📘 You selected {selected_class} Class.\n\n👉 Now choose a subject 👇",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except (TimedOut, NetworkError):
        await asyncio.sleep(5)
        await query.edit_message_text("⌛ Timeout. Please try again.")

# ======================
# HANDLE SUBJECT SELECTION with ERROR HANDLING
# ======================
async def subject_handler(update: Update, context: CallbackContext):
    try:
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
            text=f"📗 You selected {context.user_data['class']} Class – {selected_subject.title()}.\n\n👉 Choose an option 👇",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except (TimedOut, NetworkError):
        await asyncio.sleep(5)
        await query.edit_message_text("⌛ Timeout. Please try again.")

# ======================
# HANDLE FINAL ACTION with FIXED URLS
# ======================
async def action_handler(update: Update, context: CallbackContext):
    try:
        query = update.callback_query
        await query.answer()

        action = query.data.replace("action_", "")
        class_name = context.user_data.get("class")
        subject = context.user_data.get("subject")

        if not class_name or not subject:
            await query.edit_message_text("⚠ Please start again using /start")
            return

        if action == "collect":
            # Get subject data from updated SUBJECT_MAP
            subject_data = SUBJECT_MAP.get(subject, {})
            
            # Create dynamic URL based on class
            if class_name == "9th":
                url = subject_data["url"]
            elif class_name == "10th":
                url = subject_data["url"].replace("9th", "10th")
            elif class_name == "11th":
                url = subject_data["url"].replace("9th-class", "11th-class-intermediate-part-1")
            elif class_name == "12th":
                url = subject_data["url"].replace("9th-class", "12th-class-intermediate-part-2")
            else:
                url = subject_data["url"]

            await query.edit_message_text(
                text=f"📂 Here are the past papers for {class_name} Class – {subject.title()} (2020–2025):\n\n🔗 [Click here to view papers]({url})",
                parse_mode="Markdown"
            )
        else:
            # Generate New Paper code remains same
            qdata = QUESTION_BANK.get(subject, {})
            mcqs = random.sample(qdata.get("mcqs", []), min(5, len(qdata.get("mcqs", []))))
            shorts = random.sample(qdata.get("short", []), min(5, len(qdata.get("short", []))))
            longs = random.sample(qdata.get("long", []), min(2, len(qdata.get("long", []))))

            paper_text = f"📝 Generated Paper – {class_name} Class ({subject.title()})\n\n"
            paper_text += "📌 MCQs:\n" + "\n".join([f"{i+1}. {q}" for i, q in enumerate(mcqs)]) + "\n\n"
            paper_text += "✏ Short Questions:\n" + "\n".join([f"{i+1}. {q}" for i, q in enumerate(shorts)]) + "\n\n"
            paper_text += "📖 Long Questions:\n" + "\n".join([f"{i+1}. {q}" for i, q in enumerate(longs)])

            await query.edit_message_text(paper_text, parse_mode="Markdown")
            
    except (TimedOut, NetworkError):
        await asyncio.sleep(5)
        await query.edit_message_text("⌛ Timeout. Please try again.")

# ======================
# MAIN with TIMEOUT SETTINGS
# ======================
def main():
    # Increased timeout settings
    app = Application.builder().token(BOT_TOKEN).read_timeout(30).write_timeout(30).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(class_handler, pattern="^class_"))
    app.add_handler(CallbackQueryHandler(subject_handler, pattern="^sub_"))
    app.add_handler(CallbackQueryHandler(action_handler, pattern="^action_"))
    
    print("✅ Bot running with improved timeout settings...")
    
    # Run with exception handling
    try:
        app.run_polling()
    except Exception as e:
        print(f"❌ Error: {e}")
        # Restart after delay
        asyncio.sleep(10)
        main()

if __name__ == "__main__":
    main()
