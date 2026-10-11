#!/bin/sh
set -e
D="$HOME/.mediameta"; mkdir -p "$D"
cp mediameta.py "$D/mediameta.py"; chmod +x "$D/mediameta.py"
echo "installed: $D/mediameta.py"
echo "run: python3 $D/mediameta.py"