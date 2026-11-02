"""Shared prototype generator loader for isolated page tests."""
import json
import os
import re
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]


def load_screens():
    ns = dict(json=json, os=os, re=re, sys=SimpleNamespace(argv=[]), ROOT='/tmp/illo-unused',
              DATA=str(ROOT / 'design/data'), HERE=str(ROOT / 'design/scripts'))
    for path in sorted((ROOT / 'design/screens').glob('*.py')):
        if path.name >= '40':
            break
        exec(compile(path.read_text(), str(path), 'exec'), ns)
    return ns
