import json
import os
import random
import string

DB_FILE = os.path.join(os.path.dirname(__file__), "database.json")

# Initialize DB
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({"users": {}, "referrals": {}}, f)

def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

def generate_referral_code(user_id):
    db = load_db()
    if user_id in db["users"]:
        return db["users"][user_id]["referral_code"]

    # Random 6-character code
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    db["users"][user_id] = {"referral_code": code, "balance": 0}
    db["referrals"][code] = []
    save_db(db)
    return code

def register_referral(new_user_id, code):
    db = load_db()
    if code in db["referrals"]:
        db["referrals"][code].append(new_user_id)
        referrer_id = None
        for uid, data in db["users"].items():
            if data["referral_code"] == code:
                referrer_id = uid
                break
        if referrer_id:
            # Reward example: +50 PANCA
            db["users"][referrer_id]["balance"] += 50
            db["users"][new_user_id] = {"referral_code": generate_referral_code(new_user_id), "balance": 50}
        save_db(db)
        return referrer_id
    return None
