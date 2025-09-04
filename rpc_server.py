import requests, json

RPC_URL = "http://localhost:8332"  # replace with your RPC server URL
RPC_USER = "rpcuser"
RPC_PASS = "rpcpass"

def rpc_request(method, params=None):
    headers = {"Content-Type": "application/json"}
    payload = {"jsonrpc": "2.0","id":1,"method":method,"params":params or []}
    response = requests.post(RPC_URL, auth=(RPC_USER, RPC_PASS), headers=headers, data=json.dumps(payload))
    return response.json()

def check_balance(address):
    result = rpc_request("getbalance", [address])
    return result.get("result", 0)

def send_panca(from_address, to_address, amount):
    result = rpc_request("sendtoaddress", [from_address, to_address, amount])
    return result.get("result", None)

def get_deposit_address(address):
    return address
