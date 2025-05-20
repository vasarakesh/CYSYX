use actix_web::{post, web, App, HttpServer, HttpResponse, Responder};
use serde::{Deserialize, Serialize};
use rand::Rng;
use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Serialize, Deserialize)]
struct Transaction {
    from: String,
    message: TransactionMessage,
    signature: String,
}

#[derive(Serialize, Deserialize)]
struct TransactionMessage {
    txn: bool,
    txn_id: String,
    txn_data: TransactionData,
}

#[derive(Serialize, Deserialize)]
struct TransactionData {
    raw_data: String,
    timestamp: u64,
}

#[derive(Serialize, Deserialize)]
struct Receipt {
    from: String,
    message: ReceiptMessage,
    signature: String,
}

#[derive(Serialize, Deserialize)]
struct ReceiptMessage {
    txn: bool,
    txn_id: String,
    receipt_data: ReceiptData,
}

#[derive(Serialize, Deserialize)]
struct ReceiptData {
    status: u8,
    timestamp: u64,
}

#[post("/send_transaction")]
async fn send_transaction(data: web::Json<TransactionData>) -> impl Responder {
    let txn_id = format!("{}", rand::thread_rng().gen::<u64>());
    let message = TransactionMessage {
        txn: true,
        txn_id: txn_id.clone(),
        txn_data: data.into_inner(),
    };

    let transaction = Transaction {
        from: "sample-public-key".to_string(),
        message,
        signature: "dummy-signature".to_string(), 
    };

    HttpResponse::Ok().json(transaction)
}

#[post("/receive_transaction")]
async fn receive_transaction(data: web::Json<Transaction>) -> impl Responder {
    let transaction = data.into_inner();

    // Generate receipt 
    let receipt_message = ReceiptMessage {
        txn: false,
        txn_id: transaction.message.txn_id.clone(),
        receipt_data: ReceiptData {
            status: 1,
            timestamp: current_timestamp(),
        },
    };

    let receipt = Receipt {
        from: "sample-public-key".to_string(),
        message: receipt_message,
        signature: "receipt-signature".to_string(), 
    };

    HttpResponse::Ok().json(receipt)
}

fn current_timestamp() -> u64 {
    SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_secs()
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .service(send_transaction)
            .service(receive_transaction)
    })
    .bind("127.0.0.1:8092")?
    .run()
    .await
}
