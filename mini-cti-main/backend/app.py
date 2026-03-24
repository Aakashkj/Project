from flask import Flask, jsonify, request
from web3 import Web3
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Connect to Hardhat node
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
print("Connected:", w3.is_connected())

# Hardhat Account #0 private key
private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
account = w3.eth.account.from_key(private_key)
print("Using wallet:", account.address)

# Contract address
cti_address = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512"

# Load ABI
with open("../artifacts/contracts/CTIRegistry.sol/CTIRegistry.json") as f:
    contract_json = json.load(f)

abi = contract_json["abi"]
cti_contract = w3.eth.contract(address=cti_address, abi=abi)

# ---------------- ROUTES ---------------- #

# GET count
@app.route("/count", methods=["GET"])
def get_count():
    count = cti_contract.functions.ctiCount().call()
    return jsonify({"cti_count": count})


# POST register organization
@app.route("/orgs", methods=["POST"])
def register_org():
    data = request.get_json()
    name = data.get("name")

    print("Received org:", name)

    return jsonify({"message": "Org registered"})


# POST register CTI
@app.route("/cti", methods=["POST"])
def register_cti():
    data = request.get_json()
    cti_text = data.get("cti_data")

    if not cti_text:
        return jsonify({"error": "No CTI data provided"}), 400

    # Hash CTI text
    hash_value = w3.keccak(text=cti_text)

    # Build transaction
    tx = cti_contract.functions.registerCTI(hash_value).build_transaction({
        "from": account.address,
        "nonce": w3.eth.get_transaction_count(account.address),
        "gas": 300000,
        "gasPrice": w3.to_wei("20", "gwei")
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    return jsonify({
        "message": "CTI registered",
        "tx_hash": tx_hash.hex()
    })


# GET CTI (for frontend display)
@app.route("/cti", methods=["GET"])
def get_cti():
    return jsonify([
        {"id": 1, "hash": "sample_hash"}
    ])


# POST rate
@app.route("/rate", methods=["POST"])
def rate_cti():
    data = request.get_json()
    print("Rating received:", data)

    return jsonify({"message": "Rating submitted"})


# ---------------- RUN APP ---------------- #

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)