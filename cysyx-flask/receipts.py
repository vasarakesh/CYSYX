import time
from utils import sign_data

def create_receipt(public_key, txn_id, status):
    """
    Create a receipt message with the specified transaction ID and status,
    signed by the transaction recipient's private key.
    """
    timestamp = int(time.time())  # Current Unix timestamp

    # Receipt message
    receipt_data = {
        "from": public_key,
        "message": {
            "txn": False,
            "txn_id": txn_id,
            "receipt_data": {
                "status": status,
                "timestamp": timestamp
            }
        }
    }

    # Sign the receipt
    receipt_data["signature"] = sign_data(receipt_data)

    return receipt_data
