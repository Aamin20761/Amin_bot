import os
import logging
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/HooshvareLab/gpt2-fa"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من AminBot هستم. سوالی داری بپرس!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = query_huggingface(user_message)
    await update.message.reply_text(response)

def query_huggingface(payload):
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": payload})
    try:
        return response.json()[0]['generated_text']
    except:
        return "متأسفم، مشکلی پیش اومده!"

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
