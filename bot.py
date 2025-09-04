from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from wallet_ui import generate_wallet_card
from referral_system import generate_referral_code, register_referral

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

def start(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    args = context.args
    if args:
        code = args[0]
        referrer = register_referral(user_id, code)
        if referrer:
            update.message.reply_text(f"🎉 You were referred! Referrer ID: {referrer}")

    referral_code = generate_referral_code(user_id)
    update.message.reply_text(f"Welcome! Your referral code is: {referral_code}")

    keyboard = [
        [InlineKeyboardButton("💰 Check Balance", callback_data="balance")],
        [InlineKeyboardButton("📤 Send PANCA", callback_data="send")],
        [InlineKeyboardButton("📥 Deposit PANCA", callback_data="deposit")],
        [InlineKeyboardButton("🎁 Invite Friends", callback_data="referral")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Choose an action:", reply_markup=reply_markup)

def wallet_card(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    referral_code = generate_referral_code(user_id)
    balance = 500  # Example balance, fetch from blockchain later
    address = "PANCAxxxxxxxx"  # Example, fetch user wallet
    img_path = generate_wallet_card(address, balance, referral_code)
    update.message.reply_photo(photo=open(img_path, "rb"))

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("wallet", wallet_card))

app.run_polling()
