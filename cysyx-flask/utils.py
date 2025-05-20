import json
import uuid
import time
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

# Generate an RSA private-public key pair 
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()

def sign_data(data):
    """
    Sign the data using the private key and return the signature in hex format.
    """
    # Convert data to JSON string with sorted keys 
    data_str = json.dumps(data, sort_keys=True)
    data_bytes = data_str.encode('utf-8')
    print("Signing JSON Data:", data_str)  # Debug log

    # Generate signature with PKCS1v15 padding
    signature = private_key.sign(
        data_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("Generated Signature (Hex):", signature.hex())  # Debug log
    return signature.hex()

def verify_signature(data, signature):
    """
    Verify the signature using the public key.
    Returns True if the signature is valid, False otherwise.
    """
    # Convert data to JSON string with sorted keys 
    data_str = json.dumps(data, sort_keys=True)
    data_bytes = data_str.encode('utf-8')
    print("Verifying Data:", data_str)  # Debug log

    try:
        public_key.verify(
            bytes.fromhex(signature),
            data_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("Signature is valid.")  # Debug log
        return True
    except Exception as e:
        print("Signature verification failed:", e)  # Debug log
        return False

def generate_transaction_id():
    """Generate a unique transaction ID using UUID v4."""
    return str(uuid.uuid4())

def get_current_timestamp():
    """Get the current Unix timestamp."""
    return int(time.time())
