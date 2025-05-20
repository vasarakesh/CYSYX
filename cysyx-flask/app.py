from flask import Flask, request, jsonify
from datetime import datetime
import uuid
import json
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization

app = Flask(__name__)

# RSA key pair for demonstration (for production, securely store the keys)
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

# sign a message with JSON serialization
def sign_message(message):
    """Signs the message using the private key with JSON serialization."""
    message_bytes = json.dumps(message, sort_keys=True).encode()
    signature = private_key.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return base64.b64encode(signature).decode()

# verify a signature with JSON serialization
def verify_signature(message, signature, public_key):
    """Verifies the message's signature using the provided public key with JSON serialization."""
    try:
        message_bytes = json.dumps(message, sort_keys=True).encode()
        signature_bytes = base64.b64decode(signature.encode())
        public_key.verify(
            signature_bytes,
            message_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print("Signature verification failed:", e)  # Debug log
        return False

@app.route('/send_transaction', methods=['POST'])
def send_transaction():
    data = request.json
    raw_data = data.get("raw_data")

    if not raw_data:
        return jsonify({"error": "Missing raw_data"}), 400

    txn_data = {
        "raw_data": raw_data,
        "timestamp": int(datetime.now().timestamp() * 1000)
    }

    message = {
        "txn": True,
        "txn_id": str(uuid.uuid4()),
        "txn_data": txn_data
    }

    # Sign the message
    signature = sign_message(message)
    transaction = {
        "from": public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode(),
        "message": message,
        "signature": signature
    }

    return jsonify(transaction)

@app.route('/')
def home():
    return "CYSYX Flask Server is Running"

@app.route('/receive_transaction', methods=['POST'])
def receive_transaction():
    data = request.json
    message = data.get("message")
    signature = data.get("signature")
    sender_public_key_pem = data.get("from").encode()
    
    # Load the sender's public key
    sender_public_key = serialization.load_pem_public_key(sender_public_key_pem)

    # Verify the signature
    is_valid = verify_signature(message, signature, sender_public_key)
    if not is_valid:
        return jsonify({"error": "Invalid signature"}), 400

    # Create a signed receipt
    receipt_message = {
        "txn": False,
        "txn_id": message["txn_id"],
        "receipt_data": {
            "status": 1,
            "timestamp": int(datetime.now().timestamp() * 1000)
        }
    }
    
    receipt_signature = sign_message(receipt_message)
    receipt = {
        "from": public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode(),
        "message": receipt_message,
        "signature": receipt_signature
    }

    return jsonify(receipt)

if __name__ == '__main__':
    app.run(port=8090)
