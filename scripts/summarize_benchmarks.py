
import json
import matplotlib.pyplot as plt

def summarize_benchmarks(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)

    simplified = []
    for bench in data['benchmarks']:
        name = bench['name']
        mean = bench['stats']['mean']
        min_ = bench['stats']['min']
        ops = bench['stats']['ops']

        simplified.append({
            'name': name,
            'mean (ms)': round(mean * 1000, 3),
            'min (ms)': round(min_ * 1000, 3),
            'ops/sec': round(ops, 2)
        })

    return simplified

def bar_chart(summary):

    labels = [entry['name'] for entry in summary]
    times = [entry['mean (ms)'] for entry in summary]

    plt.figure(figsize=(10, 6))
    plt.barh(labels, times)
    plt.xlabel('Mean Time (ms)')
    plt.title('Benchmark Results')
    plt.tight_layout()
    #plt.savefig('benchmark_chart.png')  # or plt.show()
    plt.show()

def line_graph(summary):

    # Data from benchmark summary
    labels = [
        "test_list_comparison",
        "test_counter_comparison",
        "test_counters_only_comparison"
    ]
    times = [entry['mean (ms)'] for entry in summary]  # Mean times in ms

    # Optional: better labels for chart display
    display_labels = ["List Comparison", "Counter + Union", "Counter Only"]

    # Plot as line graph
    plt.figure(figsize=(10, 6))
    plt.plot(display_labels, times, marker='o', linestyle='-', linewidth=2)

    # Labels and title
    plt.ylabel("Mean Time (ms)")
    plt.title("Benchmark Comparison")
    plt.grid(True, linestyle='--', alpha=0.6)

    # Save or show
    plt.tight_layout()
    #plt.savefig("benchmark_line_chart.png")
    plt.show()  # Uncomment to display instead of saving

def plot_mean_times(summary):

    # Labels (benchmark names as shown in the summary table)
    labels = ["List Comparison", "Counter + Union", "Counter Only"]
    mean_times = [entry['mean (ms)'] for entry in summary]  # in milliseconds

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(labels, mean_times, marker='o', linestyle='-', linewidth=2, color='royalblue')
    plt.title("Mean Execution Time per Method")
    plt.ylabel("Mean Time (ms)")
    plt.xlabel("Comparison Method")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()

    # Save image
    plt.savefig("benchmark_mean_time.png")
    #plt.show()  # Optional if you want to view instead of saving


if __name__ == '__main__':
    try:
        summary = summarize_benchmarks('../output.json')

        print(f"| {'Benchmark':<35} | {'Mean (ms)':>10} | {'Min (ms)':>10} | {'Ops/sec':>10} |")
        print(f"| {'-'*35} | {'-'*10} | {'-'*10} | {'-'*10} |")
        for entry in summary:
            print(f"| {entry['name']:<35} | {entry['mean (ms)']:>10.3f} | {entry['min (ms)']:>10.3f} | {entry['ops/sec']:>10.2f} |")

        plot_mean_times(summary)
    except Exception as e:
        print(f'ERROR: {e}')

