import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_jmh_results(file_path, framework_name):
    with open(file_path, "r") as f:
        data = json.load(f)

    results = {}
    for entry in data:
        full_name = entry["benchmark"]
        # Extract short method name (e.g., 'average10000Class')
        method_name = full_name.split(".")[-1]

        score_ms = entry["primaryMetric"]["score"]
        # Convert ms/op to ops/sec (throughput)
        ops_sec = (
            1000.0 / score_ms if entry["mode"] == "avgt" else score_ms
        )

        results[method_name] = ops_sec

    return framework_name, results


# 1. Load data from both framework results
frameworks = {}
for file_path, name in [
    ("results/jmh-results-log4j2.json", "Log4j2 Async Appender"),
]:
    fw_name, data = load_jmh_results(file_path, name)
    frameworks[fw_name] = data

# Create DataFrame (Rows: Benchmarks/Scenarios, Columns: Frameworks)
df = pd.DataFrame(frameworks)

# 2. Setup Plot
fig, ax = plt.subplots(figsize=(10, 6))

categories = df.columns.tolist()  # ['Logback Async Appender', 'Log4j2 Async Appender']
benchmarks = df.index.tolist()  # Benchmark method names
num_groups = len(categories)
num_bars = len(benchmarks)

bar_width = 0.25
x = np.arange(num_groups)

# Colors matching Google Charts / target style
colors = ["#3366CC", "#FF9900", "#DC3912", "#109618", "#990099"]

# 3. Draw Grouped Bars
bars_list = []
for i, benchmark in enumerate(benchmarks):
    offset = (i - (num_bars - 1) / 2) * bar_width
    values = df.loc[benchmark].values
    rects = ax.bar(
        x + offset,
        values,
        bar_width,
        label=benchmark,
        color=colors[i % len(colors)],
    )
    bars_list.append(rects)

# 4. Styling & Y-Axis
ax.set_title(
    "Performance Impact of logging Caller-Information\n(higher is better)",
    fontsize=13,
    fontweight="bold",
    pad=20,
)
ax.set_ylabel("messages per second", fontsize=11, fontstyle="italic")
ax.grid(axis="y", linestyle="-", alpha=0.3)
ax.set_axisbelow(True)
ax.yaxis.set_major_formatter("{x:,.0f}")

# Remove default X-ticks (since table will act as X-axis labels)
ax.set_xticks([])

# 5. Create Data Table at the Bottom
table_data = []
for benchmark in benchmarks:
    row = [f"{val:,.0f}" for val in df.loc[benchmark]]
    table_data.append(row)

table = plt.table(
    cellText=table_data,
    rowLabels=benchmarks,
    colLabels=categories,
    cellLoc="center",
    loc="bottom",
)

# Style Table
table.scale(1, 1.8)
table.set_fontsize(10)

# Colors for row labels in legend table
for i, key in enumerate(table.get_celld().keys()):
    if key[1] == -1 and key[0] >= 0:
        table[key].set_text_props(
            color=colors[(key[0] - 1) % len(colors)], fontweight="bold"
        )

plt.subplots_adjust(bottom=0.28)
plt.tight_layout()

plt.savefig("benchmark_comparison.png", dpi=300)
plt.show()