#!/usr/bin/env python3
"""
Plot GHC compilation phase timings from *.dump-timings files.
"""

import re
import glob
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

def parse_timings_file(filepath):
    """Parse a single .dump-timings file."""
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            # Match lines like: "Parser [T10]: alloc=557240 time=0.314"
            match = re.match(r'\s*(.+?)\s+\[(.+?)\]:\s+alloc=(\d+)\s+time=([\d.]+)', line)
            if match:
                phase = match.group(1)
                test_name = match.group(2)
                alloc = int(match.group(3))
                time = float(match.group(4))
                data.append({
                    'phase': phase,
                    'test_name': test_name,
                    'alloc': alloc,
                    'time': time
                })
    return data

def extract_size_from_filename(filename):
    """Extract the numeric size from filename like 'T10.dump-timings' -> 10"""
    match = re.match(r'T(\d+)\.dump-timings', filename)
    if match:
        return int(match.group(1))
    return None

def main():
    # Find all .dump-timings files
    timing_files = sorted(glob.glob('*.dump-timings'))

    if not timing_files:
        print("No .dump-timings files found in current directory")
        return

    print(f"Found {len(timing_files)} timing files")

    # Parse all files and organize by phase
    phase_data = {}  # phase -> list of (size, time, alloc)

    for filepath in timing_files:
        filename = Path(filepath).name
        size = extract_size_from_filename(filename)

        if size is None:
            print(f"Skipping {filename} - couldn't extract size")
            continue

        data = parse_timings_file(filepath)

        for entry in data:
            phase = entry['phase']
            if phase not in phase_data:
                phase_data[phase] = []
            phase_data[phase].append((size, entry['time'], entry['alloc']))

    # Sort data points by size for each phase
    for phase in phase_data:
        phase_data[phase].sort(key=lambda x: x[0])

    # Create plots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Plot 1: Time vs Size
    ax1.set_xlabel('Test Size')
    ax1.set_ylabel('Time (ms)')
    ax1.set_title('Compilation Phase Times vs Test Size')
    ax1.grid(True, alpha=0.3)

    # Plot 2: Allocation vs Size
    ax2.set_xlabel('Test Size')
    ax2.set_ylabel('Allocation (bytes)')
    ax2.set_title('Compilation Phase Allocations vs Test Size')
    ax2.grid(True, alpha=0.3)

    # Select interesting phases to plot (skip very fast ones)
    interesting_phases = []
    for phase, points in phase_data.items():
        if len(points) > 1:  # Need at least 2 points to plot
            max_time = max(p[1] for p in points)
            if max_time > 0.1:  # Only plot phases that take significant time
                interesting_phases.append(phase)

    # Plot each phase
    for phase in interesting_phases:
        points = phase_data[phase]
        sizes = [p[0] for p in points]
        times = [p[1] for p in points]
        allocs = [p[2] for p in points]

        ax1.plot(sizes, times, marker='o', label=phase, linewidth=2)
        ax2.plot(sizes, allocs, marker='o', label=phase, linewidth=2)

    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)

    plt.tight_layout()

    # Save the plot
    output_file = 'timings_plot.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Plot saved to {output_file}")

if __name__ == '__main__':
    main()
