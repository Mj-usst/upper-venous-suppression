#!/usr/bin/env python
from __future__ import annotations

import importlib
import os
import shutil

REQUIRED_MODULES = ["numpy", "pandas", "nibabel", "SimpleITK", "scipy", "yaml"]
REQUIRED_COMMANDS = ["nnUNetv2_train", "nnUNetv2_predict"]
REQUIRED_ENV = ["nnUNet_raw", "nnUNet_preprocessed", "nnUNet_results"]


def main():
    print("Checking Python modules...")
    for mod in REQUIRED_MODULES:
        try:
            importlib.import_module(mod)
            print(f"  OK: {mod}")
        except Exception as e:
            print(f"  MISSING: {mod} ({e})")

    print("\nChecking nnU-Net commands...")
    for cmd in REQUIRED_COMMANDS:
        path = shutil.which(cmd)
        print(f"  {cmd}: {path or 'NOT FOUND'}")

    print("\nChecking nnU-Net environment variables...")
    for key in REQUIRED_ENV:
        print(f"  {key}: {os.environ.get(key, 'NOT SET')}")


if __name__ == "__main__":
    main()
