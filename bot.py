import os
import requests
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters
import threading

# ضع التوكن الخاص بك هنا
TOKEN = "8947234227:AAGdoUk5VpFyAVzjHKRMqwiio68mfshLDeU"

# قاعدة بيانات مؤقتة لتخزين نقاط المستخدمين واشتراكاتهم (يمكن ربطها بقاعدة بيانات حقيقية لاحقاً)
user_data_db = {}

# إنشاء تطبيق ويب لترضية سيرفرات Render وضمان استمرار التشغيل 24/7
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# أمر البداية /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_data_db:
        user_data_db[user_id] = {"points": 0, "vip": False}
    
    keyboard = [
        [InlineKeyboardButton("📺 مشاهدة فيديو وكسب نقاط", callback_data="choose_ads")],
        [InlineKeyboardButton("💎 إزالة الإعلانات (2$ شهرياً)", callback_data="buy_vip")],
        [InlineKeyboardButton("🏆 رصيدي ونقاطي", callback_data="my_profile")],
        [InlineKeyboardButton("💡 معلومة عشوائية", callback_data="get_fact")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "أهلاً بك في البوت الشامل! 🎉\n"
        "يمكنك تصفح الخدمات، مشاهدة الفيديوهات لاكتساب النقاط، أو ترقية حسابك لإزالة الإعلانات.",
        reply_markup=reply_markup
    )

# معالجة الأزرار التفاعلية (Callback Queries)
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if user_id not in user_data_db:
        user_data_db[user_id] = {"points": 0, "vip": False}

    if query.data == "choose_ads":
        # قائمة اختيار الفيديوهات/الإعلانات حسب المزاج
        keyboard = [
            [InlineKeyboardButton("🎬 إعلان ترفيهي (+10 نقاط)", callback_data="ad_fun")],
            [InlineKeyboardButton("📚 إعلان تعليمي وتطويري (+15 نقاط)", callback_data="ad_study")],
            [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]
        ]
        await query.edit_message_text("اختر نوع الفيديو/الإعلان الذي تفضله لمشاهدته وكسب النقاط:", reply_markup=InlineKeyboardMarkup([keyboard[0], keyboard[1], keyboard[2]]))

    elif query.data in ["ad_fun", "ad_study"]:
        # إضافة النقاط بناءً على الاختيار
        earned = 10 if query.data == "ad_fun" else 15
        user_data_db[user_id]["points"] += earned
        
        # التحقق مما إذا كان المستخدم مشتركاً (لديه VIP لإخفاء الإعلانات الترويجية الإضافية)
        is_vip = user_data_db[user_id]["vip"]
        ad_msg = "" if is_vip else "\n\n*(إعلان ترويجي: اشترك الآن بـ 2$ لتتخلص من هذه الإعلانات نهائياً!)*"
        
        await query.edit_message_text(
            f"✅ أتممت مشاهدة الفيديو بنجاح!\n"
            f"🎁 حصلت على {earned} نقطة.\n"
            f"💰 رصيدك الحالي: {user_data_db[user_id]['points']} نقطة{ad_msg}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة للقائمة", callback_data="main_menu")]])
        )

    elif query.data == "buy_vip":
        await query.edit_message_text(
            "💎 **الاشتراك الشهري لإزالة الإعلانات (2 دولار):**\n\n"
            "ميزات الاشتراك:\n"
            "- تصفح البوت بدون أي إعلانات نهائياً.\n"
            "- أولوية في الرد وسرعة الخدمة.\n\n"
            "لإتمام الدفع واكتساب العضوية، يرجى التواصل مع الإدارة أو تحويل المبلغ عبر وسائل الدفع المتاحة.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة للقائمة", callback_data="main_menu")]])
        )

    elif query.data == "my_profile":
        points = user_data_db[user_id]["points"]
        vip_status = "مشترك (بدون إعلانات) 💎" > 0 if user_data_db[user_id]["vip"] else "عضو عادي (تظهر لك إعلانات) 📺"
        await query.edit_message_text(
            f"👤 **حسابك الشخصي:**\n\n"
            f"🏆 النقاط: {points} نقطة\n"
            f"⭐ نوع الحساب: {vip_status}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة للقائمة", callback_data="main_menu")]])
        )

    elif query.data == "get_fact":
        try:
            response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
            fact = response.json().get("text") if response.status_code == 200 else "لا توجد معلومات حالياً."
        except:
            fact = "تعذر الاتصال بالخادم لجلب المعلومة."
            
        await query.edit_message_text(
            f"💡 **معلومة مفيدة:**\n{fact}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة للقائمة", callback_data="main_menu")]])
        )

    elif query.data == "main_menu":
        keyboard = [
            [InlineKeyboardButton("📺 مشاهدة فيديو وكسب نقاط", callback_data="choose_ads")],
            [InlineKeyboardButton("💎 إزالة الإعلانات (2$ شهرياً)", callback_data="buy_vip")],
            [InlineKeyboardButton("🏆 رصيدي ونقاطي", callback_data="my_profile")],
            [InlineKeyboardButton("💡 معلومة عشوائية", callback_data="get_fact")]
        ]
        await query.edit_message_text("القائمة الرئيسية:", reply_markup=InlineKeyboardMarkup(keyboard))

# الرد التلقائي على الرسائل النصية العادية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "سعر" in text or "اشتراك" in text:
        await update.message.reply_text("يمكنك الاشتراك لإزالة الإعلانات مقابل 2 دولار فقط شهرياً عبر الضغط على القائمة الرئيسية أو استخدام الأمر /start.")
    else:
        await update.message.reply_text(f"أهلاً بك! لقد استليمت رسالتك: '{text}'. استخدم الأمر /start للوصول إلى كافة الخدمات.")

def main():
    # تشغيل سيرفر الويب Flask في الخلفية
    t = threading.Thread(target=run_flask)
    t.start()

    # تشغيل بوت تليجرام
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()

if __name__ == '__main__':
    main()
