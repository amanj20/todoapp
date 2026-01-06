import sys
from pathlib import Path

# Add project root (parent of /tests) to Python import path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
