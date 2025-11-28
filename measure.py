import subprocess
import time
import os
import argparse
import shlex

parser = argparse.ArgumentParser(description="Measure compilation time for generated Haskell files.")
parser.add_argument("--prefix", type=str, default="", help="Path prefix for GHC command (e.g., '_build/stage1/bin/'). Use '' for none.")
parser.add_argument("--ghc-options", type=str, default="", help="Additional options to pass to GHC compiler (e.g., '-O2 -Werror')")
parser.add_argument("--output", type=str, default="", help="Output file for measurements")
args = parser.parse_args()

PREFIX = args.prefix
GHC = os.path.join(PREFIX, "ghc") if PREFIX else "ghc"

ghc_options = shlex.split(args.ghc_options) if args.ghc_options else []

csv_filename = args.output if args.output else "compile_times.csv"

# sizes = [10, 100, 500, 750, 1000, 1500, 2000]

sizes = [5,10,15,20, 30, 40]

compile_times = []
filenames = []

def generate_module(count: int) -> str:
    header = "{-# LANGUAGE DataKinds #-}\n"
    module_line = f"module T{count} where\n\n"
    imports = "import GHC.TypeLits\n\n"
    data_t = "data T (n :: Nat) = MkT Int\n\n"
    fields = []
    for ix in range(1, count + 1):
        fields.append(f"field{ix} :: T {ix}")
    fields_str = ",\n  ".join(fields)
    data_d = f"data D = MkD {{\n  {fields_str}\n  }}"
    return header + module_line + imports + data_t + data_d

def generate_module_quadratic(count: int) -> str:
    header = "{-# LANGUAGE DataKinds #-}\n"
    module_line = f"module T{count} where\n\n"
    imports = "import GHC.TypeLits\n\n"
    data_t = "data T (n :: Nat) = MkT Int\n\n"
    fields = []
    for ix in range(1, count + 1):
        fields.append(f"field{ix} :: T {ix}")
    fields_str = ",\n  ".join(fields)
    ctors = []
    for ix in range(1, count + 1):
        ctors.append(f"MkD{ix} {{\n  {fields_str}\n  }}")
    ctors_str = "\n  | ".join(ctors)
    data_d = f"data D = {ctors_str}"
    return header + module_line + imports + data_t + data_d

for n in sizes:
    hs_filename = f"T{n}.hs"
    hi_filename = f"T{n}.hi"
    o_filename = f"T{n}.o"

    with open(hs_filename, "w") as f:
        f.write(generate_module_quadratic(n))

    ghc_cmd = [GHC, hs_filename] + ghc_options
    start = time.time()
    result = subprocess.run(ghc_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    end = time.time()
    compile_time = end - start
    compile_times.append(compile_time)
    filenames.append(hs_filename)

    if result.returncode != 0:
        print(f"Compilation failed for size {n}:\n", result.stderr.decode())
    print(f"Compiled {hs_filename} in {compile_time:.3f}s")

    for fname in [hs_filename, hi_filename, o_filename]:
        if os.path.exists(fname):
            os.remove(fname)

import csv

with open(csv_filename, mode="w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Count of fields", "GHC Compilation Time (s)"])
    for sz, t in zip(sizes, compile_times):
        writer.writerow([sz, t])

print(f"Data dumped to {csv_filename}")
