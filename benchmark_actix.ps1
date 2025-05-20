# Path: benchmark_actix.ps1
echo "Benchmarking Actix Web (Rust) on http://127.0.0.1:8092/send_transaction"
wsl ab -n 10000 -c 400 -g actix_results.txt http://127.0.0.1:8092/send_transaction
echo "Results saved to actix_results.txt"
