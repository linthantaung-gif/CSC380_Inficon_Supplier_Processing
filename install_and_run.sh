#!/usr/bin/env bash
set -e

echo ""
echo " ========================================="
echo "  INFICON Form Filler"
echo " ========================================="
echo ""

# ── Check Python ─────────────────────────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
    echo " [!] Python 3 is not installed."
    echo "     Install it from: https://www.python.org/downloads/"
    echo ""
    read -rp " Press Enter to exit..." _
    exit 1
fi

PY_VER=$(python3 --version 2>&1 | awk '{print $2}')
echo " [OK] Python $PY_VER found."
echo ""

# ── Install dependencies ──────────────────────────────────────────────────────
echo " Installing required libraries (first run may take a few minutes)..."
echo " Please wait."
echo ""

python3 -m pip install --upgrade pip --quiet
python3 -m pip install \
    sentence-transformers \
    pandas \
    numpy \
    pymupdf \
    pypdf \
    python-docx \
    scikit-learn \
    torch \
    Pillow \
    --quiet

echo ""
echo " [OK] All libraries ready."
echo ""

# ── Launch ────────────────────────────────────────────────────────────────────
cd "$(dirname "$0")"
echo " Launching Form Filler..."
echo ""
python3 app.py