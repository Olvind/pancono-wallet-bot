import random, string

# Simple in-memory storage (replace with DB in production)
USER_REFERRALS = {}   # user_id -> referral_code
REFERRAL_TRACK = {}   # referral_code -> list of user_ids

def generate_referral_code(user_id):
    """Generate or return existing referral code for a user"""
    if user_id in USER_REFERRALS:
        return USER_REFERRALS[user_id]
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    USER_REFERRALS[user_id] = code
    REFERRAL_TRACK.setdefault(code, [])
    return code

def register_referral(new_user_id, ref_code):
    """Register a new user using someone else's referral code"""
    if ref_code in REFERRAL_TRACK:
        REFERRAL_TRACK[ref_code].append(new_user_id)
        # TODO: credit PANCA rewards to referrer
        return True
    return False

def get_referral_stats(user_id):
    """Return number of referrals for this user"""
    code = USER_REFERRALS.get(user_id)
    if not code: return 0
    return len(REFERRAL_TRACK.get(code, []))
