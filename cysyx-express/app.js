const express = require('express');
const crypto = require('crypto');
const app = express();
const port = 8091;

console.log("Starting the Express server...");

app.use(express.json());

// Generate RSA key pair for demonstration
const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', {
    modulusLength: 2048,
});

console.log("Public Key:", publicKey.export({ type: 'pkcs1', format: 'pem' }));

// Endpoint to send a transaction
app.post('/send_transaction', (req, res) => {
    const { raw_data } = req.body;

    if (!raw_data) {
        console.log("Error: Missing raw_data in request");
        return res.status(400).json({ error: 'Missing raw_data' });
    }

    const txn = createTransaction(publicKey.export({ type: 'pkcs1', format: 'pem' }), raw_data);
    console.log("Transaction created:", txn);
    res.json(txn);
});

// Endpoint to receive a transaction and respond with a receipt
app.post('/receive_transaction', (req, res) => {
    const txnData = req.body;
    console.log("Received transaction data:", txnData);

    // Verify the transaction
    const isValid = verifySignature(txnData, txnData.signature);
    if (!isValid) {
        console.log("Invalid signature:", txnData.signature);
        return res.status(400).json({ error: 'Invalid signature' });
    }

    const receipt = createReceipt(publicKey.export({ type: 'pkcs1', format: 'pem' }), txnData.message.txn_id, 1);
    console.log("Receipt generated:", receipt);
    res.json(receipt);
});

// Start server
app.listen(port, () => {
    console.log(`Express server listening on port ${port}`);
});

// Helper function to create a transaction with a real signature
function createTransaction(publicKey, rawData) {
    const message = {
        from: publicKey,
        message: {
            txn: true,
            txn_id: crypto.randomUUID(),
            txn_data: {
                raw_data: rawData,
                timestamp: Date.now()
            }
        }
    };
    
    // Create a digital signature for the transaction
    const sign = crypto.createSign('SHA256');
    sign.update(JSON.stringify(message.message));
    sign.end();
    const signature = sign.sign(privateKey, 'hex');

    return { ...message, signature };
}

// Helper function to verify the transaction signature
function verifySignature(data, signature) {
    const verify = crypto.createVerify('SHA256');
    verify.update(JSON.stringify(data.message));
    verify.end();
    return verify.verify(publicKey, signature, 'hex');
}

// Helper function to create a receipt with a real signature
function createReceipt(publicKey, txnId, status) {
    const receipt = {
        from: publicKey,
        message: {
            txn: false,
            txn_id: txnId,
            receipt_data: {
                status: status,
                timestamp: Date.now()
            }
        }
    };
    
    // Create a digital signature for the receipt
    const sign = crypto.createSign('SHA256');
    sign.update(JSON.stringify(receipt.message));
    sign.end();
    const signature = sign.sign(privateKey, 'hex');

    return { ...receipt, signature };
}
