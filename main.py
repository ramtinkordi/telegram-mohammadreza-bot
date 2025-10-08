import os
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

WELCOME_TEXT = "🌟 به ربات «محمدرضا » خوش آمدید.👺"
HELP_TEXT = (
    "راهنمای پیگیری_سفارشات_و_واریزی_ها : "
    "به بخش پیگیری سفارشات بروید سپس یکی از گزینه هارو انتخاب کنید و کد پی‌گیری رو وارد کنید "
    "در این بخش اگر تراکنش موفق داشته باشید یا سفارشی داشته باشید وضعیت سفارش که در حال انجام یا تکمیل شده هست "
    "به شما نشان داده میشود"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("راهنما 📖", callback_data="help")]
    ])
    if update.message:
        await update.message.reply_html(WELCOME_TEXT, reply_markup=keyboard)
    elif update.callback_query:
        await update.callback_query.message.reply_html(WELCOME_TEXT, reply_markup=keyboard)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT)

async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "help":
        await q.edit_message_text(HELP_TEXT)
    else:
        await q.edit_message_text("این بخش به‌زودی فعال می‌شود.")

async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

def main():
    if not BOT_TOKEN:
        raise RuntimeError("❌ BOT_TOKEN تنظیم نشده!")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CallbackQueryHandler(on_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))
    logging.info("🤖 MohammadReza bot via Polling is running…")
    app.run_polling()

if __name__ == "__main__":
    main()
