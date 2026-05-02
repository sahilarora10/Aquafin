import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from config import TELEGRAM_TOKEN
from advisor import get_response, reset_conversation

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! 👋 I'm your personal finance advisor.\n\n"
        "Tell me what's on your mind — planning to invest, reviewing your portfolio, "
        "or just curious about something like REITs or bonds?\n\n"
        "I'll keep it simple and jargon-free unless you tell me otherwise. Let's go!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Here's what you can do:\n\n"
        "💬 Just chat — tell me about your money situation and I'll guide you\n"
        "🔄 /reset — start a fresh conversation\n"
        "❓ /help — see this message\n\n"
        "Try starting with something like:\n"
        "• 'I have ₹10 lakhs to invest safely'\n"
        "• 'What are REITs?'\n"
        "• 'Should I move money from equity to bonds now?'"
    )

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reset_conversation(update.effective_chat.id)
    await update.message.reply_text("Fresh start! 🔄 What's on your mind?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_text = update.message.text
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    reply = get_response(chat_id, user_text)
    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()