import os
import random
from fpdf import FPDF
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# ======================
# CONFIG
# ======================
BOT_TOKEN = os.getenv("BOT_TOKEN")  # 🔥 Render Environment Variables me BOT_TOKEN set karo

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN not set in environment variables.")

# ======================
# SAMPLE DATASET
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

        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Section A: MCQs", ln=True)
        pdf.set_font("Arial", "", 12)
        for i, q in enumerate(random.sample(all_mcqs, min(5, len(all_mcqs))), 1):
            pdf.multi_cell(0, 10, f"Q{i}. {q}")
        pdf.ln(5)

        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Section B: Short Questions", ln=True)
        pdf.set_font("Arial", "", 12)
        for i, q in enumerate(random.sample(all_short, min(5, len(all_short))), 1):
            pdf.multi_cell(0, 10, f"Q{i}. {q}")
        pdf.ln(5)

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
        "📘 Welcome to *Mardan Board Papers Bot*!\n\n"
        "Commands:\n"
        "➡️ /collect <class> <subject>\n"
        "➡️ /generate <class> <subject>\n"
        "Example: `/collect 9th english` or `/generate 9th english`"
    )

async def collect_cmd(update: Update, context: CallbackContext):
    if len(context.args) < 2:
        await update.message.reply_text("⚠️ Example: `/collect 9th english`")
        return
    class_name, subject = context.args[0], context.args[1]
    data = DATASET.get(class_name, {}).get(subject)
    if not data:
        await update.message.reply_text("❌ No papers found for this subject/class.")
        return
    output_pdf = f"{class_name}_{subject}_old.pdf"
    generate_paper(data, output_pdf, mode="old")
    await update.message.reply_document(open(output_pdf, "rb"))
    await update.message.reply_text("✅ Here are old papers.")

async def generate_cmd(update: Update, context: CallbackContext):
    if len(context.args) < 2:
        await update.message.reply_text("⚠️ Example: `/generate 9th english`")
        return
    class_name, subject = context.args[0], context.args[1]
    data = DATASET.get(class_name, {}).get(subject)
    if not data:
        await update.message.reply_text("❌ No papers found for this subject/class.")
        return
    output_pdf = f"{class_name}_{subject}_new.pdf"
    generate_paper(data, output_pdf, mode="new")
    await update.message.reply_document(open(output_pdf, "rb"))
    await update.message.reply_text("✅ Here is your generated paper 📄")

# ======================
# MAIN
# ======================
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("collect", collect_cmd))
    app.add_handler(CommandHandler("generate", generate_cmd))
    print("✅ Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
