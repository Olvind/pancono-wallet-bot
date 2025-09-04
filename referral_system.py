import json
from rpc import send_transaction, get_balance

DATABASE_FILE = "database.json"
SYSTEM_WALLET = {"address": "YOUR_SYSTEM_WALLET_ADDRESS", "private_key": "YOUR_SYSTEM_PRIVATE_KEY"}
REFERRAL_REWARD = 0.01  # PANCA

def generate_referral_code(user_id):
    return f"PANCO{str(user_id)[-4:]}"

def process_referral(user_id, args):
    referral_code = generate_referral_code(user_id)
    if args:
        ref_code = args[0]
        with open(DATABASE_FILE, "r") as f:
            db = json.load(f)
        for uid, data in db.items():
            if generate_referral_code(uid) == ref_code and user_id not in data["referrals"]:
                data["referrals"].append(user_id)
                db[uid] = data
                with open(DATABASE_FILE, "w") as f:
                    json.dump(db, f, indent=4)
                reward_referral(uid)
                break
    return referral_code

def reward_referral(referrer_id):
    with open(DATABASE_FILE, "r") as f:
        db = json.load(f)
    ref_user = db.get(referrer_id)
    if not ref_user:
        return
    tx_hash = send_transaction(
        SYSTEM_WALLET["address"],
        ref_user["address"],
        REFERRAL_REWARD,
        SYSTEM_WALLET["private_key"]
    )
    print(f"Referral reward sent: {tx_hash}")
