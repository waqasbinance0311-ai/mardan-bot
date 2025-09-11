import os
import random
from fpdf import FPDF
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# ======================
# CONFIG
# ======================
BOT_TOKEN = os.getenv("8023108538:AAE51wAdhjHSv6TQOYBBe7RS0jIrOTRoOcs")  # 🔥 Render me Environment Variable set karna hoga

# ======================
# SAMPLE DATASET (JSON inside code)
# ======================
DATASET = {
    "9th": {
        "english": {
            "old_papers": {
                "2022": {
                    "MCQs": ["Synonym of 'honest'?", "Antonym of 'bright'?", "Tense of 'I was going'?", "Meaning of 'optimistic'?", "Plural of 'child'?"],
                    "Short": ["Define a verb.", "What is a paragraph?", "Define an adjective.", "Difference between adverb and adjective?", "Write 5 forms of verb 'Go'."],
                    "Long": ["Essay on 'My Country'.", "Letter to your friend about exams.", "Application for sick leave.", "Story: Honesty is the best policy.", "Essay on 'Importance of Education'."]
                },
                "2021": {
                    "MCQs": ["Choose correct article: ___ apple.", "Synonym of 'brave'?", "Antonym of 'dark'?", "Past tense of 'run'?", "Preposition in 'He is fond ___ books'?"],
                    "Short": ["Define a noun.", "What is preposition?", "Difference between phrase and clause.", "What is conjunction?", "Write 5 irregular verbs."],
                    "Long": ["Essay on 'Education'.", "Letter to principal for fee concession.", "Application for character certificate.", "Story: Greedy Dog.", "Essay on 'My School'."]
                }
            }
        },
        "computer": {
            "old_papers": {
                "2022": {
                    "MCQs": ["CPU stands for?", "Which is input device? (a) Mouse (b) Printer", "Binary of 5 is?", "Which is system software?", "What is algorithm?"],
                    "Short": ["Define RAM.", "Differentiate hardware & software.", "What is a compiler?", "Define LAN.", "What is a flowchart?"],
                    "Long": ["Explain generations of computer.", "Describe MS Word features.", "Explain internet advantages.", "Discuss uses of computer in education.", "Explain programming languages."]
                },
                "2021": {
                    "MCQs": ["RAM stands for?", "Which is output device? (a) Monitor (b) Keyboard", "Binary of 10?", "MS Word is? (a) OS (b) App Software", "What is database?"],
                    "Short": ["Define ROM.", "What is operating system?", "Explain modem.", "What is network?", "What is software engineering?"],
                    "Long": ["Explain parts of computer system.", "Describe MS Excel uses.", "Explain computer in business.", "Discuss types of networks.", "Explain software development life cycle."]
                }
            }
        }
    },
    "10th": {
        "english": {
            "old_papers": {
                "2022": {
                    "MCQs": ["Synonym of 'happy'?", "Antonym of 'rich'?", "Correct tense: He ___ playing.", "Plural of 'tooth'?", "Meaning of 'generous'?"],
                    "Short": ["Define pronoun.", "What is subject?", "Write 5 irregular verbs.", "What is adverb?", "What is passive voice?"],
                    "Long": ["Essay on 'Patriotism'.", "Letter to friend about hobby.", "Application for urgent leave.", "Story: Lion and Mouse.", "Essay on 'Science and Technology'."]
                },
                "2021": {
                    "MCQs": ["Choose correct article: ___ umbrella.", "Synonym of 'wise'?", "Antonym of 'kind'?", "Past tense of 'eat'?", "Preposition in 'He is afraid ___ snakes'?"],
                    "Short": ["Define adjective.", "What is object?", "What is conjunction?", "Difference between phrase and clause.", "Write forms of 'Come'."],
                    "Long": ["Essay on 'Health'.", "Letter to principal for leave.", "Application for new books.", "Story: Hare and Tortoise.", "Essay on 'Computer'."]
                }
            }
        }
    }
}

# ======================
# PDF GENERATOR
# ======================
def generate_paper(data, output_file, mode="new"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, f"Mardan Board Paper ({mode.title()})", ln=True, align="C")
    pdf.ln(10)

    if mode == "old":
        for year, sections in data["old_papers"].items():
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, f"Year {year}", ln=True)
            pdf.set_font("Arial", "", 12)
            for sec, qs in sections.items():
                pdf.multi_cell(0, 10, f"{sec} Questions:")
                for i, q in enumerate(qs, 1):
                    pdf.multi_cell(0, 10, f"Q{i}. {q}")
            pdf.ln(5)
    else:
        all_mcqs, all_short, all_long = [], [], []
        for year, sections in data["old_papers"].items():
            all_mcqs.extend(sections.get("MCQs", []))
            all_short.extend(sections.get("Short", []))
            all_long.extend(sections.get("Long", []))

        # MCQs
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Section A: MCQs", ln=True)
        pdf.set_font("Arial", "", 12)
        for i, q in enumerate(random.sample(all_mcqs, min(5, len(all_mcqs))), 1):
            pdf.multi_cell(0, 10, f"Q{i}. {q}")
        pdf.ln(5)

        # Short
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Section B: Short Questions", ln=True)
        pdf.set_font("Arial", "", 12)
        for i, q in enumerate(random.sample(all_short, min(5, len(all_short))), 1):
            pdf.multi_cell(0, 10, f"Q{i}. {q}")
        pdf.ln(5)

        # Long
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Section C: Long Questions", ln=True)
        pdf.set_font("Arial", "", 12)
        for i, q in enumerate(random.sample(all_long, min(5, len(all_long))), 1):
            pdf.multi_cell(0, 10, f"Q{i}. {q}")
            pdf.ln(5)

    pdf.output(output_file)
    return output_file

# ======================
# BOT COMMANDS
# ======================
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "📘 *Welcome to Mardan Board Papers Bot!*\n\n"
        "Use commands:\n"
        "➡️ `/collect <class> <subject>` (Old Papers)\n"
        "➡️ `/generate <class> <subject>` (New Paper)\n\n"
        "⚡ Example: `/collect 9th english` or `/generate 10th computer`",
        parse_mode="Markdown"
    )

async def collect_cmd(update: Update, context: CallbackContext):
    if len(context.args) < 2:
        await update.message.reply_text("⚠ Example: `/collect 9th english`", parse_mode="Markdown")
        return
    class_name, subject = context.args[0], context.args[1]
    data = DATASET.get(class_name, {}).get(subject)
    if not data:
        await update.message.reply_text("❌ No papers found for this subject/class.")
        return
    output_pdf = f"{class_name}_{subject}_old.pdf"
    generate_paper(data, output_pdf, mode="old")
    with open(output_pdf, "rb") as f:
        await update.message.reply_document(f)
    await update.message.reply_text("✅ Old papers collected successfully!")

async def generate_cmd(update: Update, context: CallbackContext):
    if len(context.args) < 2:
        await update.message.reply_text("⚠ Example: `/generate 9th english`", parse_mode="Markdown")
        return
    class_name, subject = context.args[0], context.args[1]
    data = DATASET.get(class_name, {}).get(subject)
    if not data:
        await update.message.reply_text("❌ No papers found for this subject/class.")
        return
    output_pdf = f"{class_name}_{subject}_new.pdf"
    generate_paper(data, output_pdf, mode="new")
    with open(output_pdf, "rb") as f:
        await update.message.reply_document(f)
    await update.message.reply_text("✅ New paper generated successfully 📄")

# ======================
# MAIN
# ======================
def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not set in environment variables.")
        return
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("collect", collect_cmd))
    app.add_handler(CommandHandler("generate", generate_cmd))
    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

