import os
from pathlib import Path

# dir structure
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / 'data'

# Tesseract 
TESSERACT_CMD = r'/usr/local/Cellar/tesseract/5.3.0/bin/tesseract'