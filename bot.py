import os
import random
import asyncio
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram.error import TimedOut, NetworkError
# ======================
# BOT TOKEN & CHAT ID
# ======================
BOT_TOKEN = "8023108538:AAE51wAdhjHSv6TQOYBBe7RS0jIrOTRoOcs"
CHAT_ID = "5969642968"
# ======================
# SUBJECT URLS FOR DIFFERENT CLASSES
# ======================
PAST_PAPER_URLS = {
    "9th": {
        "english": "https://www.ilmkidunya.com/past_papers/9th-class-english-past-papers-mardan-board.aspx",
        "urdu": "https://www.ilmkidunya.com/past_papers/9th-class-urdu-past-papers-mardan-board.aspx",
        "math": "https://www.ilmkidunya.com/past_papers/9th-class-mathematics-past-papers-mardan-board.aspx",
        "computer": "https://www.ilmkidunya.com/past_papers/9th-class-computer-science-past-papers-mardan-board.aspx",
        "biology": "https://www.ilmkidunya.com/past_papers/9th-class-biology-past-papers-mardan-board.aspx"
    },
    "10th": {
        "english": "https://www.ilmkidunya.com/past_papers/10th-class-english-past-papers-mardan-board.aspx",
        "urdu": "https://www.ilmkidunya.com/past_papers/10th-class-urdu-past-papers-mardan-board.aspx",
        "math": "https://www.ilmkidunya.com/past_papers/10th-class-mathematics-past-papers-mardan-board.aspx",
        "computer": "https://www.ilmkidunya.com/past_papers/10th-class-computer-science-past-papers-mardan-board.aspx",
        "biology": "https://www.ilmkidunya.com/past_papers/10th-class-biology-past-papers-mardan-board.aspx"
    },
    "11th": {
        "english": "https://www.ilmkidunya.com/past_papers/11th-class-english-past-papers-mardan-board.aspx",
        "urdu": "https://www.ilmkidunya.com/past_papers/11th-class-urdu-past-papers-mardan-board.aspx",
        "math": "https://www.ilmkidunya.com/past_papers/11th-class-mathematics-past-papers-mardan-board.aspx",
        "computer": "https://www.ilmkidunya.com/past_papers/11th-class-computer-science-past-papers-mardan-board.aspx",
        "biology": "https://www.ilmkidunya.com/past_papers/11th-class-biology-past-papers-mardan-board.aspx"
    },
    "12th": {
        "english": "https://www.ilmkidunya.com/past_papers/12th-class-english-past-papers-mardan-board.aspx",
        "urdu": "https://www.ilmkidunya.com/past_papers/12th-class-urdu-past-papers-mardan-board.aspx",
        "math": "https://www.ilmkidunya.com/past_papers/12th-class-mathematics-past-papers-mardan-board.aspx",
        "computer": "https://www.ilmkidunya.com/past_papers/12th-class-computer-science-past-papers-mardan-board.aspx",
        "biology": "https://www.ilmkidunya.com/past_papers/12th-class-biology-past-papers-mardan-board.aspx"
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
            # Get the correct URL from the updated PAST_PAPER_URLS dictionary
            try:
                url = PAST_PAPER_URLS[class_name][subject]
                
                # Create a message with better formatting
                message_text = (
                    f"📂 *Past Papers for {class_name} Class - {subject.title()}*\n\n"
                    f"🔗 [Click here to view and download past papers]({url})\n\n"
                    f"📝 *Available Papers:* 2020-2025\n"
                    f"🎯 *Board:* Mardan Board\n"
                    f"📚 *Subject:* {subject.title()}\n\n"
                    f"💡 *Tip:* Bookmark this link for easy access!"
                )
                
                # Also add a back button
                keyboard = [
                    [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_start")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(
                    text=message_text,
                    reply_markup=reply_markup,
                    parse_mode="Markdown",
                    disable_web_page_preview=False
                )
                
            except KeyError:
                await query.edit_message_text(
                    text=f"❌ Sorry, past papers for {class_name} Class - {subject.title()} are not available yet.\n\n🔄 Please try generating a new paper instead.",
                    parse_mode="Markdown"
                )
                
        elif action == "generate":
            # Generate New Paper code
            qdata = QUESTION_BANK.get(subject, {})
            
            if not qdata:
                await query.edit_message_text(
                    text=f"❌ Questions for {subject.title()} are not available yet.",
                    parse_mode="Markdown"
                )
                return
            
            mcqs = random.sample(qdata.get("mcqs", []), min(5, len(qdata.get("mcqs", []))))
            shorts = random.sample(qdata.get("short", []), min(5, len(qdata.get("short", []))))
            longs = random.sample(qdata.get("long", []), min(2, len(qdata.get("long", []))))
            paper_text = f"📝 *Generated Paper – {class_name} Class ({subject.title()})*\n\n"
            
            if mcqs:
                paper_text += "📌 *MCQs:*\n"
                paper_text += "\n".join([f"{i+1}. {q}" for i, q in enumerate(mcqs)]) + "\n\n"
            
            if shorts:
                paper_text += "✏ *Short Questions:*\n"
                paper_text += "\n".join([f"{i+1}. {q}" for i, q in enumerate(shorts)]) + "\n\n"
            
            if longs:
                paper_text += "📖 *Long Questions:*\n"
                paper_text += "\n".join([f"{i+1}. {q}" for i, q in enumerate(longs)])
            # Add back button
            keyboard = [
                [InlineKeyboardButton("🔄 Generate Another", callback_data="action_generate")],
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                text=paper_text, 
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
    except (TimedOut, NetworkError):
        await asyncio.sleep(5)
        await query.edit_message_text("⌛ Timeout. Please try again.")
    except Exception as e:
        print(f"Error in action_handler: {e}")
        await query.edit_message_text("❌ An error occurred. Please try again with /start")
# ======================
# BACK TO START HANDLER
# ======================
async def back_to_start_handler(update: Update, context: CallbackContext):
    try:
        query = update.callback_query
        await query.answer()
        
        # Clear user data
        context.user_data.clear()
        
        # Show start menu again
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
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")
        
    except Exception as e:
        print(f"Error in back_to_start_handler: {e}")
        await query.edit_message_text("❌ Error occurred. Please use /start command.")
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
    app.add_handler(CallbackQueryHandler(back_to_start_handler, pattern="^back_to_start$"))
    
    print("✅ Bot running with improved timeout settings and fixed past paper links...")
    
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
