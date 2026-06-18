#!/usr/bin/env python3
"""Generate placeholder PNG icons for PWA manifest."""
import struct, zlib, os

def create_png(size, bg=(52, 73, 94), fg=(255, 255, 255)):
    def chunk(ctype, data):
        c = ctype + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

    header = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0))

    raw = b''
    for y in range(size):
        raw += b'\x00'
        for x in range(size):
            cx, cy = x - size // 2, y - size // 2
            dist = (cx * cx + cy * cy) ** 0.5
            if dist < size * 0.35:
                raw += bytes(fg)
            else:
                raw += bytes(bg)

    idat = chunk(b'IDAT', zlib.compress(raw))
    iend = chunk(b'IEND', b'')
    return header + ihdr + idat + iend

os.makedirs('icon', exist_ok=True)
for sz in [192, 512]:
    with open(f'icon/icon-{sz}.png', 'wb') as f:
        f.write(create_png(sz))
    print(f'Created icon/icon-{sz}.png')
