import os
import requests
import threading
import time
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import load_dotenv
import claim_manager

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
RPC_URL = f"http://{os.getenv('RPC_HOST')}:{os.getenv('RPC_PORT')}"

# JSON-RPC helper
def rpc_call(method, params=[]):
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    r = requests.post(RPC_URL, json=payload)
    return r.json().get("result")

# ---------------------- BOT COMMANDS ----------------------

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🚀 Welcome to Pancono Wallet Bot!\n\n"
        "Commands:\n"
        "/createwallet → Make a new wallet\n"
        "/importwallet <private_key> → Import reserved wallet\n"
        "/balance <address> → Check balance\n"
        "/send <from> <to> <amount> → Send PANCA\n"
        "/startclaim <address> → Start auto-claim (24 hrs)"
    )

def createwallet(update: Update, context: CallbackContext):
    wallet = rpc_call("createwallet")
    update.message.reply_text(
        f"✅ Wallet created!\n\n"
        f"Address: {wallet['address']}\n"
        f"Private Key: {wallet['private_key']}"
    )

def importwallet(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        update.message.reply_text("Usage: /importwallet <private_key>")
        return
    wallet = rpc_call("importwallet", [context.args[0]])
    update.message.reply_text(
        f"✅ Wallet imported!\n\n"
        f"Address: {wallet['address']}"
    )

def balance(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Usage: /balance <address>")
        return
    bal = rpc_call("getbalance", [context.args[0]])
    update.message.reply_text(f"💰 Balance: {bal} PANCA")

def send(update: Update, context: CallbackContext):
    if len(context.args) != 3:
        update.message.reply_text("Usage: /send <from_address> <to_address> <amount>")
        return
    try:
        tx = rpc_call("send", [context.args[0], context.args[1], float(context.args[2])])
        update.message.reply_text(
            f"✅ Sent {tx['amount']} PANCA\n"
            f"From: {tx['from']}\n"
            f"To: {tx['to']}"
        )
    except Exception as e:
        update.message.reply_text(f"❌ Error: {e}")

def startclaim(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Usage: /startclaim <address>")
        return
    msg = claim_manager.start_claim(update.effective_user.id, context.args[0])
    update.message.reply_text(msg)

# ---------------------- AUTO CLAIM BACKGROUND ----------------------

def run_claim_checker():
    while True:
        claim_manager.check_claims()
        time.sleep(3600)  # check every hour

# ---------------------- MAIN ----------------------

if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERROR: Missing TELEGRAM_BOT_TOKEN. Set it in .env or Replit Secrets.")
        exit(1)

    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # Register bot commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("createwallet", createwallet))
    dp.add_handler(CommandHandler("importwallet", importwallet))
    dp.add_handler(CommandHandler("balance", balance))
    dp.add_handler(CommandHandler("send", send))
    dp.add_handler(CommandHandler("startclaim", startclaim))

    # Run background claim system
    threading.Thread(target=run_claim_checker, daemon=True).start()

    updater.start_polling()
    updater.idle()
