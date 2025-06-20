import sys
import os

root = os.path.abspath(os.path.dirname(__file__))
for p in ["auth", "backend"]:
    path = os.path.join(root, p)
    if os.path.isdir(path) and path not in sys.path:
        sys.path.insert(0, path)
