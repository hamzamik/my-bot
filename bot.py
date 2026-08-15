import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# إعداد السجلات لمتابعة الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# توكن البوت الخاص بك (ضع التكن بين علامتي التنصيص)
TOKEN = "وضع_التوكن_الخاص_بك_هنا"

# دالة رسالة البداية /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # أزرار تفاعلية تحت الرسالة
    keyboard = [
        [InlineKeyboardButton("🎁 تجميع النقاط", callback_data="get_points")],
        [InlineKeyboardButton("💎 شحن الجواهر", callback_data="withdraw")],
        [InlineKeyboardButton("📢 قناة العروض", url="https://t.me/your_channel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = (
        f"مرحباً بك يا {user.first_name} في بوت شحن جواهر فري فاير!\n\n"
        "قم بدعوة أصدقائك أو تفاعل لتجميع النقاط، ثم استبدلها بجواهر حقيقية مجاناً."
    )
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# دالة التعامل مع الأزرار
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "get_points":
        await query.edit_message_text(
            text="لجمع النقاط، قم بمشاركة رابط الإحالة الخاص بك مع أصدقائك:\n(قريباً سيتم تفعيل نظام الإحالات تلقائياً)."
        )
    elif query.data == "withdraw":
        await query.edit_message_text(
            text="عذراً، رصيدك الحالي غير كافٍ للسحب. اجمع المزيد من النقاط لطلب شحن الجواهر!"
        )

def main():
    # بناء تطبيق البوت
    application = ApplicationBuilder().token(TOKEN).build()

    # ربط الأوامر بالدوال
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # بدء تشغيل البوت
    print("البوت يعمل الآن...")
    application.run_polling()

if __name__ == '__main__':
    main()
