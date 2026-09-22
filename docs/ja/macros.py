# Copyright (c) 2026 Noda Hiroyuki
"""Load the shared Zensical macros module for the Japanese documentation."""

# ruff: noqa: INP001

import importlib.util
from pathlib import Path

shared_macros_path = Path(__file__).resolve().parents[2] / "macros.py"
spec = importlib.util.spec_from_file_location("shared_macros", shared_macros_path)
if spec is None or spec.loader is None:
    raise ImportError from None

shared_macros = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared_macros)

define_env = shared_macros.define_env
