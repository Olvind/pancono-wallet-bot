# rpc.py
import random

# Mock RPC for testing without a real blockchain
WALLETS = {}  # {address: balance}

def check_balance(address):
    # Return balance if exists, else initialize
    if address not in WALLETS:
        WALLETS[address] = 500  # default starting balance for testing
    return WALLETS[address]

def send_panca(from_address, to_address, amount):
    if from_address not in WALLETS:
        WALLETS[from_address] = 500
    if to_address not in WALLETS:
        WALLETS[to_address] = 500

    if WALLETS[from_address] >= amount:
        WALLETS[from_address] -= amount
        WALLETS[to_address] += amount
        txid = f"mock_txid_{random.randint(1000,9999)}"
        return txid
    else:
        return None

def get_deposit_address(address):
    # Simply return the same address for testing
    if address not in WALLETS:
        WALLETS[address] = 500
    return address
