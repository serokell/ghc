#!/usr/bin/env python3
"""
Generate test files T<N>.hs with N fields.
Usage: python3 gen_test.py <N>
"""

import sys

def generate_test_file(n):
    """Generate a test file with n fields."""

    header = f"""{{-# LANGUAGE DataKinds #-}}
{{-# OPTIONS -fno-opt-selectors #-}}
{{-# OPTIONS -ddump-to-file -ddump-timings #-}}
-- {{-# OPTIONS -ddump-to-file -ddump-stg-from-core -ddump-stg-final -ddump-cmm #-}}

module T{n} where

import GHC.TypeLits

data T (n :: Nat) = MkT Int

data D = MkD {{
"""

    # Generate field declarations
    fields = []
    for i in range(1, n + 1):
        field = "  field{i} :: T {i}".format(i=i)
        fields.append(field)

    fields_str = ",\n".join(fields)

    footer = "\n  }\n"

    return header + fields_str + footer

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 gen_test.py <N>")
        print("Example: python3 gen_test.py 20")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
        if n < 1:
            print("Error: N must be a positive integer")
            sys.exit(1)
    except ValueError:
        print("Error: N must be an integer")
        sys.exit(1)

    content = generate_test_file(n)
    filename = f"T{n}.hs"

    with open(filename, 'w') as f:
        f.write(content)

    print(f"Generated {filename} with {n} fields")

if __name__ == "__main__":
    main()
