# Path: benchmark_flask.ps1
echo "Benchmarking Flask (Python) on http://127.0.0.1:8090/send_transaction"
wsl ab -n 10000 -c 400 -g flask_results.txt http://127.0.0.1:8090/send_transaction
echo "Results saved to flask_results.txt"
