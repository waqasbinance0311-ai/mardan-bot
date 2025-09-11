import os
import random
from fpdf import FPDF
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# ======================
# CONFIG
# ======================
BOT_TOKEN = os.getenv("BOT_TOKEN")  # 🔥 Render me BOT_TOKEN Environment Variable set karo

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN not set in environment variables.")

# ======================
# DATASET (9th–12th, 5 Subjects, 5 Years)
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
                },
                "2020": {
                    "MCQs": ["Antonym of 'strong'?", "Synonym of 'fast'?", "What is pronoun?", "Past tense of 'eat'?", "Preposition in 'He lives ___ Lahore'."],
                    "Short": ["Define interjection.", "What is subject and predicate?", "Write 5 collective nouns.", "What is article?", "Explain present continuous tense."],
                    "Long": ["Essay on 'My Best Friend'.", "Letter to your father for money.", "Application for leave in advance.", "Story: Hare and Tortoise.", "Essay on 'Village Life'."]
                },
                "2019": {
                    "MCQs": ["Synonym of 'sad'?", "Antonym of 'poor'?", "What is adverb?", "Future tense of 'go'?", "Plural of 'man'?"],
                    "Short": ["Define clause.", "What is an idiom?", "Difference between active and passive voice.", "What is article?", "Write 5 modal verbs."],
                    "Long": ["Essay on 'My Hobby'.", "Letter to friend for invitation.", "Application for urgent work leave.", "Story: King and Spider.", "Essay on 'Sports'."]
                },
                "2018": {
                    "MCQs": ["Synonym of 'angry'?", "Antonym of 'rich'?", "What is conjunction?", "Past participle of 'write'?", "Meaning of 'courage'?"],
                    "Short": ["Define adverb.", "What is direct and indirect speech?", "Difference between phrase and idiom.", "What is preposition?", "Define tense."],
                    "Long": ["Essay on 'My School'.", "Letter to cousin for Eid.", "Application for readmission.", "Story: Thirsty Crow.", "Essay on 'Examination'."]
                }
            }
        },
        "computer": {
            "old_papers": {
                "2022": {
                    "MCQs": ["Binary of 8?", "Shortcut of Copy?", "Primary unit of computer?", "Who is father of computer?", "What is ALU?"],
                    "Short": ["Define RAM.", "Define ROM.", "What is MS Word?", "Explain Internet.", "What is Database?"],
                    "Long": ["Essay on 'Use of Computer in Education'.", "Write an application in C language.", "Explain parts of computer.", "Importance of Networking.", "Role of IT in modern world."]
                },
                "2021": {
                    "MCQs": ["Binary of 16?", "Shortcut of Paste?", "What is CPU?", "Full form of LAN?", "What is Software?"],
                    "Short": ["Define Hardware.", "Difference between input and output device.", "What is MS Excel?", "What is WWW?", "What is Algorithm?"],
                    "Long": ["Explain Operating System.", "Write program for sum of 2 numbers.", "Explain uses of MS PowerPoint.", "Essay: Internet Advantages.", "Role of Computer in Health."]
                }
            }
        }
    },
    "10th": {
        "math": {
            "old_papers": {
                "2022": {
                    "MCQs": ["Solve: 2+3*4?", "sin90°?", "Derivative of x^2?", "Log10(100)?", "Value of π?"],
                    "Short": ["Define Polynomial.", "What is Matrix?", "Find HCF of 24 and 36.", "Define Circle.", "Find roots of x^2-4=0."],
                    "Long": ["Solve Quadratic Equation.", "Explain Trigonometric ratios.", "Solve simultaneous equations.", "Essay on importance of Math.", "Problem of Geometry."]
                },
                "2021": {
                    "MCQs": ["cos0°?", "sin0°?", "Factorize x^2+5x+6.", "Solve log(1).", "Area of square?"],
                    "Short": ["Define Linear Equation.", "Find LCM of 15,20.", "What is Statistics?", "Define Angle.", "Difference between Radius and Diameter."],
                    "Long": ["Solve 2x+3=7.", "Explain probability with example.", "Construct triangle ABC.", "Essay on 'Math in daily life'.", "Algebra problem."]
                }
            }
        }
    },
    "11th": {
        "physics": {
            "old_papers": {
                "2022": {
                    "MCQs": ["Unit of Force?", "Speed formula?", "Newton’s 1st Law?", "Unit of Energy?", "Speed of light?"],
                    "Short": ["Define Acceleration.", "What is Work?", "What is Power?", "State Newton's 2nd law.", "Define Scalar."],
                    "Long": ["Explain Motion.", "Derive equation of Force.", "Essay on Energy conservation.", "Simple harmonic motion.", "Gravitation law."]
                }
            }
        }
    },
    "12th": {
        "chemistry": {
            "old_papers": {
                "2022": {
                    "MCQs": ["Atomic number of Oxygen?", "Symbol of Sodium?", "H2O formula?", "Molar mass of CO2?", "Valency of Carbon?"],
                    "Short": ["Define Acid.", "Define Base.", "Law of conservation of mass.", "What is Isotope?", "Define Chemical Reaction."],
                    "Long": ["Essay on Chemistry role in daily life.", "Explain Organic Chemistry.", "Derive Gas laws.", "Importance of Chemistry.", "Write on Environmental Chemistry."]
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
        "Example: `/collect 9th english` or `/generate 10th math`"
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
