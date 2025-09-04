import requests
import json

RPC_URL = "http://127.0.0.1:8545"  # Replace with your node endpoint

def rpc_call(method, params=[]):
    payload = {"jsonrpc":"2.0", "method":method, "params":params, "id":1}
    response = requests.post(RPC_URL, json=payload)
    return response.json().get("result")

def get_balance(address):
    return float(rpc_call("getBalance", [address]))

def send_transaction(from_addr, to_addr, amount, private_key):
    tx = rpc_call("sendTransaction", [{"from":from_addr,"to":to_addr,"value":str(amount),"private_key":private_key}])
    return tx

def generate_wallet():
    wallet = rpc_call("newWallet")
    # Expected response: {"address":"0x1234...","private_key":"abcd..."}
    return wallet
