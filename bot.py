from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackContext,
)
from wallet_ui import generate_wallet_card
from referral_system import (
    generate_referral_code,
    register_referral,
    get_all_users,
    get_user_referrals,
)
from rpc import check_balance, send_panca, get_deposit_address

# Replace with your bot token
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
# Replace with your Telegram user ID(s) as admin
ADMIN_IDS = ["123456789"]

# States for sending PANCA interactively
SEND_ADDRESS, SEND_AMOUNT = range(2)

# Start command
def start(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    args = context.args
    if args:
        code = args[0]
        referrer = register_referral(user_id, code)
        if referrer:
            update.message.reply_text(f"🎉 You were referred! Referrer ID: {referrer}")

    referral_code = generate_referral_code(user_id)
    keyboard = [
        [InlineKeyboardButton("💰 Check Balance", callback_data="balance")],
        [InlineKeyboardButton("📤 Send PANCA", callback_data="send")],
        [InlineKeyboardButton("📥 Deposit PANCA", callback_data="deposit")],
        [InlineKeyboardButton("🎁 Invite Friends", callback_data="referral")],
        [InlineKeyboardButton("👥 My Referrals", callback_data="myreferrals")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome! Choose an action:", reply_markup=reply_markup)

# Inline button handler
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = str(query.from_user.id)
    referral_code = generate_referral_code(user_id)
    address = "PANCAxxxxxxxx"  # fetch user's wallet from DB

    if query.data == "balance":
        bal = check_balance(address)
        query.message.reply_text(f"💰 Your balance: {bal} PANCA")
    elif query.data == "send":
        query.message.reply_text("Please send the recipient's address:")
        return SEND_ADDRESS
    elif query.data == "deposit":
        deposit_address = get_deposit_address(address)
        img_path = generate_wallet_card(deposit_address, check_balance(address), referral_code)
        query.message.reply_photo(photo=open(img_path, "rb"))
    elif query.data == "referral":
        query.message.reply_text(f"🎁 Your referral link: https://t.me/PanconoBot?start={referral_code}")
    elif query.data == "myreferrals":
        referrals = get_user_referrals(user_id)
        if referrals:
            msg = f"🎯 You have referred {len(referrals)} users:\n"
            for uid in referrals:
                msg += f"- {uid}\n"
        else:
            msg = "😕 You have not referred anyone yet."
        query.message.reply_text(msg)
    return ConversationHandler.END

# Interactive send PANCA
def send_address(update: Update, context: CallbackContext):
    context.user_data["to_address"] = update.message.text
    update.message.reply_text("Enter amount of PANCA to send:")
    return SEND_AMOUNT

def send_amount(update: Update, context: CallbackContext):
    from_address = "PANCAxxxxxxxx"  # fetch from DB
    to_address = context.user_data["to_address"]
    try:
        amount = float(update.message.text)
        txid = send_panca(from_address, to_address, amount)
        if txid:
            update.message.reply_text(f"✅ Sent {amount} PANCA!\nTxID: {txid}")
        else:
            update.message.reply_text("❌ Transaction failed.")
    except:
        update.message.reply_text("❌ Invalid amount entered.")
    return ConversationHandler.END

# Admin dashboard
def admin_dashboard(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    if user_id not in ADMIN_IDS:
        update.message.reply_text("❌ You are not authorized.")
        return
    users = get_all_users()
    msg = f"Total Users: {len(users)}\n\n"
    for uid, data in users.items():
        referrals = get_user_referrals(uid)
        msg += f"UserID: {uid}\nReferrals: {len(referrals)}\n\n"
    update.message.reply_text(msg)

# Create application
app = ApplicationBuilder().token(TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin_dashboard))

conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(button_handler)],
    states={
        SEND_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, send_address)],
        SEND_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, send_amount)],
    },
    fallbacks=[],
)

app.add_handler(conv_handler)
app.run_polling()
