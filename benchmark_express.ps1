# Path: benchmark_express.ps1
echo "Benchmarking Express.js (Node.js) on http://127.0.0.1:8091/send_transaction"
wsl ab -n 10000 -c 400 -g express_results.txt http://127.0.0.1:8091/send_transaction
echo "Results saved to express_results.txt"
