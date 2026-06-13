from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8210101180:AAGntRylOhBrnETmNs37uNB5Q0O7S5kDP7c"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🐉 Welcome to Ultimate Dragon!\n\n"
        "⚔️ Battle\n"
        "🎲 Gacha\n"
        "👥 Team\n"
        "🌍 Travel\n"
        "🔍 Explore\n"
        "🏆 Quests\n"
        "🛒 Shop\n"
        "👤 Profile"
    )

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👤 Profile System")

async def explore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Exploring New Areas")

async def travel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌍 Traveling To A New World")

async def team(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👥 Team Management")

async def gacha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎲 Summoning Characters")

async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛒 Welcome To The Shop")

async def battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚔️ Battle Started")

async def quests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏆 Quest System")

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("profile", profile))
app.add_handler(CommandHandler("explore", explore))
app.add_handler(CommandHandler("travel", travel))
app.add_handler(CommandHandler("team", team))
app.add_handler(CommandHandler("gacha", gacha))
app.add_handler(CommandHandler("shop", shop))
app.add_handler(CommandHandler("battle", battle))
app.add_handler(CommandHandler("quests", quests))

print("🐉 Ultimate Dragon Started Successfully")

app.run_polling()
