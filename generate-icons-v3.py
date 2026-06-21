#!/usr/bin/env python3
"""Generate v3 icons by resizing wimproved.png directly (no margins)."""
from PIL import Image
import os

SRC = 'wimproved.png'
OUT_DIR = 'icon'
SIZES = [16, 24, 32, 48, 64, 192, 512]

os.makedirs(OUT_DIR, exist_ok=True)

src = Image.open(SRC).convert('RGBA')

for size in SIZES:
    resized = src.resize((size, size), Image.LANCZOS)
    out_path = os.path.join(OUT_DIR, f'icon-{size}-v3.png')
    resized.save(out_path, 'PNG')
    print(f'Created {out_path}')

# ICO with multiple sizes
ico_sizes = [16, 24, 32, 48, 64]
ico_images = [src.resize((s, s), Image.LANCZOS) for s in ico_sizes]
ico_path = os.path.join(OUT_DIR, 'favicon-v3.ico')
ico_images[0].save(ico_path, format='ICO', sizes=[(s, s) for s in ico_sizes], append_images=ico_images[1:])
print(f'Created {ico_path}')
