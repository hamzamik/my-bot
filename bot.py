import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# إعداد السجلات لمتابعة الأخطاء إن وجدت
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# دالة الترحيب عند إرسال /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! بوتك يعمل بنجاح 24/7 🎉")

if __name__ == '__main__':
    # التوكن الخاص بك
    TOKEN = "8947234227:AAGdoUk5VpFyAVzjHKRMqwiio68mfshLDeU"
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    # ربط أمر /start بالدالة
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    print("Bot is running...")
    application.run_polling()
