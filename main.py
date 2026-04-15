from ml_layer.detector import get_prediction
from web3 import Web3
import ipfshttpclient
import json
import os
import time
from web3.middleware import ExtraDataToPOAMiddleware
from dotenv import load_dotenv
from cryptography.fernet import Fernet, InvalidToken

load_dotenv()

GANACHE_URL = os.getenv("GANACHE_URL")
CONTRACT_ADDRESS = Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS"))

w3 = Web3(Web3.HTTPProvider(GANACHE_URL, request_kwargs={'timeout': 60}))
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

ipfs = None
try:
    ipfs = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
except Exception as e:
    print(f"IPFS Connection Error: {e}")

with open('blockchain_layer/ABI.json') as f:
    CONTRACT_ABI = json.load(f)
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)


def get_node_cipher(sender_addr):
    """Fetches the unique AES key for the specific node from keystore."""
    with open('keystore.json', 'r') as f:
        keystore = json.load(f)
    key = keystore.get(sender_addr)
    if not key:
        raise ValueError(f"No encryption key found for {sender_addr}")
    return Fernet(key.encode())


def process_scan(img_path, sender_addr, private_key):
    try:
        sender_addr = Web3.to_checksum_address(sender_addr)
        verdict, conf = get_prediction(img_path)
        
        with open(img_path, "rb") as f:
            raw_data = f.read()

        unique_raw_data = raw_data + str(time.time()).encode()
        
        cipher = get_node_cipher(sender_addr)
        encrypted_data = cipher.encrypt(unique_raw_data)
        
        enc_path = img_path + ".enc"
        with open(enc_path, "wb") as f:
            f.write(encrypted_data)
            
        res = ipfs.add(enc_path)
        cid = res['Hash']

        if os.path.exists(enc_path):
            os.remove(enc_path)

        nonce = w3.eth.get_transaction_count(sender_addr)
        base_txn = contract.functions.addReport(cid, verdict, conf).build_transaction({
            'chainId': 1337,
            'from': sender_addr,
            'nonce': nonce,
        })

        estimated_gas = w3.eth.estimate_gas(base_txn)
        safe_gas = int(estimated_gas * 1.2) 
        
        txn = base_txn.copy()
        txn.update({
            'gas': safe_gas,
            'maxFeePerGas': w3.to_wei('2', 'gwei'), 
            'maxPriorityFeePerGas': w3.to_wei('1', 'gwei'),
        })

        signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        tx_hex = tx_hash.hex()
        
        time.sleep(0.1) 
        return verdict, conf, cid, tx_hex

    except Exception as e:
        print(f"Pipeline failed: {e}")
        return None, None, None, str(e)


def decrypt_scan(encrypted_bytes, sender_addr):
    """Decrypts bytes using the specific node's private AES key."""
    try:
        sender_addr = Web3.to_checksum_address(sender_addr)
        cipher = get_node_cipher(sender_addr)
        return cipher.decrypt(encrypted_bytes)
    except InvalidToken:

        print("Access Denied: Invalid cryptographic key.")
        return None
    except Exception as e:
        print(f"Decryption failed: {e}")
        return None


def process_ct_folder(root_dir):
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".npy"):
                npy_path = os.path.join(subdir, file)
                pass 

if __name__ == "__main__":
    print("Main pipeline ready. Run 'streamlit run app.py' to use the interface.")