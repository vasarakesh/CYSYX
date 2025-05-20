import uuid
import time
from utils import sign_data

def create_transaction(public_key, raw_data):
    """
    Create a transaction message with a unique ID, timestamp, and signature.
    """
    txn_id = str(uuid.uuid4())  # Generate a unique transaction ID
    timestamp = int(time.time())  # Current Unix timestamp

    # transaction data 
    txn_data = {
        "from": public_key,
        "message": {
            "txn": True,
            "txn_id": txn_id,
            "txn_data": {
                "raw_data": raw_data,
                "timestamp": timestamp
            }
        }
    }

    # Sign the transaction
    txn_data["signature"] = sign_data(txn_data)

    return txn_data
