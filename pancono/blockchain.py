import uuid

# In-memory wallet storage
# Example structure:
# wallets = {
#   "PANCAabcd1234": {"balance": 100.0, "private_key": "xyz123"}
# }
wallets = {}

# ---------------------- CREATE WALLET ----------------------
def create_wallet():
    address = "PANCA" + str(uuid.uuid4())[:8]
    private_key = str(uuid.uuid4()).replace("-", "")
    wallets[address] = {"balance": 0.0, "private_key": private_key}
    return {"address": address, "private_key": private_key}

# ---------------------- IMPORT WALLET ----------------------
def import_wallet(private_key):
    # 1. If private_key already exists → return existing wallet
    for addr, data in wallets.items():
        if data["private_key"] == private_key:
            return {"address": addr, "private_key": private_key}

    # 2. Otherwise → create a new address based on key
    address = "PANCA" + private_key[:8]
    wallets[address] = {"balance": 0.0, "private_key": private_key}
    return {"address": address, "private_key": private_key}

# ---------------------- BALANCE ----------------------
def get_balance(address):
    return wallets.get(address, {}).get("balance", 0.0)

# ---------------------- SEND ----------------------
def send(sender, recipient, amount):
    if sender not in wallets or recipient not in wallets:
        raise Exception("Invalid address")

    if wallets[sender]["balance"] < amount:
        raise Exception("Insufficient funds")

    wallets[sender]["balance"] -= amount
    wallets[recipient]["balance"] += amount
    return {"from": sender, "to": recipient, "amount": amount}
