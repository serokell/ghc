import sys
import os
import csv
import matplotlib.pyplot as plt

def read_csv_data(csv_file):
    sizes = []
    times = []
    with open(csv_file, newline="") as cf:
        reader = csv.DictReader(cf)
        for row in reader:
            sizes.append(float(row["Count of fields"]))
            times.append(float(row["GHC Compilation Time (s)"]))
    return sizes, times

if len(sys.argv) < 2:
    print("Usage: python plot_from_csvs.py file1.csv file2.csv ...")
    sys.exit(1)

csv_files = sys.argv[1:]

plt.figure(figsize=(8, 5))

for csv_file in csv_files:
    sizes, compile_times = read_csv_data(csv_file)
    label = os.path.splitext(os.path.basename(csv_file))[0]
    plt.plot(sizes, compile_times, marker='o', label=label)

plt.xlabel('Count of fields')
plt.ylabel('GHC Compilation Time (s)')
plt.title('GHC Compilation Time vs Generated Source Size')
plt.grid(True)
plt.tight_layout()
plt.legend()
plt.savefig("compilation_time_vs_size.png")
plt.show()
