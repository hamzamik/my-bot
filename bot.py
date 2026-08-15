import os
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import threading

TOKEN = "8947234227:AAGdoUk5VpFyAVzjHKRMqwiio68mfshLDeU"

# إنشاء تطبيق ويب بسيط لترضية سيرفرات Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! بوتك يعمل بنجاح تام 24/7 🎉")

def main():
    # تشغيل سيرفر الويب في الخلفية
    t = threading.Thread(target=run_flask)
    t.start()

    # تشغيل بوت تليجرام
    application = ApplicationBuilder().token(TOKEN).build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    application.run_polling()

if __name__ == '__main__':
    main()

