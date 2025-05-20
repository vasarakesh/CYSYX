import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns

# Defining file paths
file_paths = {
    'actix_100': r'.\actix_results_100.txt',
    'actix_1000': r'.\actix_results_1000.txt',
    'actix_5000': r'.\actix_results_5000.txt',
    'express_100': r'.\express_results_100.txt',
    'express_1000': r'.\express_results_1000.txt',
    'express_5000': r'.\express_results_5000.txt',
    'flask_100': r'.\flask_results_100.txt',
    'flask_1000': r'.\flask_results_1000.txt',
    'flask_5000': r'.\flask_results_5000.txt'
}

# Function to extract metrics from each file
def extract_metrics(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        req_per_sec = re.search(r"Requests per second:\s+([\d.]+)", content)
        time_per_req = re.search(r"Time per request:\s+([\d.]+)", content)
        failed_requests = re.search(r"Failed requests:\s+(\d+)", content)
        
        return {
            'RequestsPerSec': float(req_per_sec.group(1)) if req_per_sec else None,
            'TimePerRequest': float(time_per_req.group(1)) if time_per_req else None,
            'FailedRequests': int(failed_requests.group(1)) if failed_requests else None
        }

# Collect data into a DataFrame
data = []
for method, path in file_paths.items():
    num_requests = method.split('_')[-1]  # Extract number of requests (100, 1000, 5000)
    method_name = method.split('_')[0]    # Extract method name (actix, express, flask)
    metrics = extract_metrics(path)
    metrics['Method'] = method_name
    metrics['NumRequests'] = int(num_requests)
    data.append(metrics)

df = pd.DataFrame(data)

# Display the DataFrame
print(df)

# Save to CSV for record-keeping or use
df.to_csv('benchmark_results.csv', index=False)

# Visualization using Seaborn and Matplotlib
sns.set(style="whitegrid")

# Plot Requests per Second
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='NumRequests', y='RequestsPerSec', hue='Method')
plt.title('Requests per Second by Method and Number of Requests')
plt.xlabel('Number of Requests')
plt.ylabel('Requests per Second')
plt.show()

# Plot Time per Request
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='NumRequests', y='TimePerRequest', hue='Method')
plt.title('Time per Request by Method and Number of Requests')
plt.xlabel('Number of Requests')
plt.ylabel('Time per Request (ms)')
plt.show()

# Plot Failed Requests
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='NumRequests', y='FailedRequests', hue='Method')
plt.title('Failed Requests by Method and Number of Requests')
plt.xlabel('Number of Requests')
plt.ylabel('Number of Failed Requests')
plt.show()

# Latency Analysis: Line chart showing average time per request
plt.figure(figsize=(12, 6))
for method in df['Method'].unique():
    subset = df[df['Method'] == method]
    plt.plot(subset['NumRequests'], subset['TimePerRequest'], marker='o', label=method)

plt.title('Latency Analysis: Time per Request for Each Framework at Different Load Levels')
plt.xlabel('Number of Requests')
plt.ylabel('Time per Request (ms)')
plt.grid(True)
plt.legend()
plt.show()
